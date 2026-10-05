import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import db_manager
from app.services.seed_data import seed_database
from app.routers import analytics, inventory, purchases, alerts, upload, settings as settings_router, export

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("citimart.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Citimart Retail Analytics Backend...")
    await db_manager.connect()
    # Seed initial demo retail dataset if collections are empty
    try:
        await seed_database(force=False)
    except Exception as e:
        logger.error(f"Error during database startup seed: {e}")
    yield
    logger.info("Shutting down Citimart Retail Analytics Backend...")
    if db_manager.client:
        db_manager.client.close()

app = FastAPI(
    title=settings.APP_NAME,
    description="Retail analytics web API for Citimart. Answers What, Where, Why, and Action.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during development or configurable via settings.cors_origins_list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "error": str(exc)}
    )

# Include Routers
app.include_router(analytics.router)
app.include_router(inventory.router)
app.include_router(purchases.router)
app.include_router(alerts.router)
app.include_router(upload.router)
app.include_router(settings_router.router)
app.include_router(export.router)

@app.get("/api/health")
async def health_check():
    status = await db_manager.get_status()
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "database": status
    }
