import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING, IndexModel
from app.config import settings

logger = logging.getLogger("citimart.db")

class ResilientInMemoryCollection:
    """In-memory collection fallback when MongoDB is unreachable."""
    def __init__(self, name: str):
        self.name = name
        self.docs: List[Dict[str, Any]] = []

    async def insert_one(self, doc: Dict[str, Any]):
        doc_copy = dict(doc)
        if "_id" not in doc_copy:
            doc_copy["_id"] = str(len(self.docs) + 1)
        self.docs.append(doc_copy)
        return doc_copy

    async def insert_many(self, docs: List[Dict[str, Any]]):
        for d in docs:
            await self.insert_one(d)
        return docs

    async def find_one(self, query: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        results = await self.find(query)
        return results[0] if results else None

    async def find(self, query: Dict[str, Any] = None, sort=None, limit: int = 0) -> List[Dict[str, Any]]:
        query = query or {}
        matches = []
        for d in self.docs:
            match = True
            for k, v in query.items():
                if isinstance(v, dict):
                    if "$in" in v and d.get(k) not in v["$in"]:
                        match = False
                        break
                    if "$gte" in v and d.get(k, "") < v["$gte"]:
                        match = False
                        break
                    if "$lte" in v and d.get(k, "") > v["$lte"]:
                        match = False
                        break
                    if "$eq" in v and d.get(k) != v["$eq"]:
                        match = False
                        break
                    if "$ne" in v and d.get(k) == v["$ne"]:
                        match = False
                        break
                elif d.get(k) != v:
                    match = False
                    break
            if match:
                matches.append(d)
        if limit > 0:
            matches = matches[:limit]
        return matches

    async def count_documents(self, query: Dict[str, Any] = None) -> int:
        res = await self.find(query)
        return len(res)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        for d in self.docs:
            match = all(d.get(k) == v for k, v in query.items())
            if match:
                if "$set" in update:
                    d.update(update["$set"])
                return True
        return False

    async def delete_many(self, query: Dict[str, Any] = None):
        if not query:
            count = len(self.docs)
            self.docs.clear()
            return count
        orig_len = len(self.docs)
        self.docs = [d for d in self.docs if not all(d.get(k) == v for k, v in query.items())]
        return orig_len - len(self.docs)

    async def create_index(self, *args, **kwargs):
        pass

class DatabaseManager:
    def __init__(self):
        self.client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self.db = None
        self.is_connected: bool = False
        self.connection_mode: str = "disconnected"
        self.fallback_collections: Dict[str, ResilientInMemoryCollection] = {}

    def get_collection(self, name: str):
        if self.is_connected and self.db is not None:
            return self.db[name]
        if name not in self.fallback_collections:
            self.fallback_collections[name] = ResilientInMemoryCollection(name)
        return self.fallback_collections[name]

    async def connect(self):
        logger.info(f"Connecting to database with URI: {settings.MONGODB_URI.split('@')[-1]}")
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=2000
            )
            # Test connectivity
            await self.client.admin.command('ping')
            self.db = self.client[settings.DATABASE_NAME]
            self.is_connected = True
            if "mongodb.net" in settings.MONGODB_URI:
                self.connection_mode = "mongodb_atlas"
            else:
                self.connection_mode = "mongodb_local"
            logger.info(f"Successfully connected to MongoDB ({self.connection_mode})!")
            await self.ensure_indexes()
        except Exception as e:
            logger.warning(f"Could not connect to external MongoDB ({e}). Falling back to resilient embedded mode.")
            self.is_connected = False
            self.connection_mode = "embedded_resilient"
            self.db = None

    async def ensure_indexes(self):
        if not self.is_connected or self.db is None:
            return
        try:
            await self.db.stores.create_index([("store_id", ASCENDING)], unique=True)
            await self.db.products.create_index([("sku", ASCENDING)], unique=True)
            await self.db.products.create_index([("division", ASCENDING), ("department", ASCENDING)])
            await self.db.vendors.create_index([("vendor_id", ASCENDING)], unique=True)
            await self.db.sales_transactions.create_index([("store_id", ASCENDING), ("date", ASCENDING)])
            await self.db.sales_transactions.create_index([("sku", ASCENDING), ("date", ASCENDING)])
            await self.db.sales_transactions.create_index([("period_type", ASCENDING), ("date", ASCENDING)])
            await self.db.inventory_snapshots.create_index([("store_id", ASCENDING), ("snapshot_date", ASCENDING)])
            await self.db.purchase_transactions.create_index([("store_id", ASCENDING), ("date", ASCENDING)])
            await self.db.import_jobs.create_index([("created_at", DESCENDING)])
            await self.db.generated_alerts.create_index([("severity", ASCENDING), ("status", ASCENDING)])
            logger.info("MongoDB indexes verified and ready.")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")

    async def get_status(self) -> Dict[str, Any]:
        coll_counts = {}
        for c in ["stores", "products", "vendors", "sales_transactions", "inventory_snapshots", "purchase_transactions", "import_jobs", "generated_alerts"]:
            coll = self.get_collection(c)
            if hasattr(coll, "count_documents"):
                try:
                    coll_counts[c] = await coll.count_documents({})
                except Exception:
                    coll_counts[c] = 0
            else:
                coll_counts[c] = len(coll.docs)

        return {
            "status": "connected" if self.is_connected else "resilient_fallback",
            "mode": self.connection_mode,
            "database_name": settings.DATABASE_NAME,
            "counts": coll_counts,
            "timestamp": datetime.utcnow().isoformat()
        }

db_manager = DatabaseManager()

def get_db():
    return db_manager
