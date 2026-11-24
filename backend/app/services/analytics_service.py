import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database import db_manager

def calculate_growth_pct(ty: float, ly: float) -> Optional[float]:
    """Calculate percentage growth safely, handling LY=0 without division error."""
    if ly and ly > 0:
        return round(((ty - ly) / ly) * 100, 2)
    elif ty > 0 and (ly is None or ly == 0):
        return None  # New item / entry
    return 0.0

def shift_date_years(date_str: str, years: int = -1) -> str:
    """Shifts a YYYY-MM-DD date by N years, safely handling Feb 29 leap years."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        try:
            new_dt = dt.replace(year=dt.year + years)
        except ValueError:
            new_dt = dt.replace(year=dt.year + years, day=28)
        return new_dt.strftime("%Y-%m-%d")
    except Exception:
        return date_str

NON_STORE_LOCATION = re.compile(r"warehouse|godown|package", re.IGNORECASE)


def is_warehouse_location(store_id: str) -> bool:
    """Warehouse / godown / package stock is a supply source, not shop-floor stock."""
    return bool(NON_STORE_LOCATION.search(store_id or ""))


HIERARCHY_FIELDS = ("division", "section", "department", "brand")


def enrich_product_lookup(prod_lookup: Dict[str, Dict[str, Any]], records: List[Dict[str, Any]]) -> None:
    """Fills gaps in the product master from division/section/department carried on sales and stock rows."""
    for r in records:
        sku = r.get("sku")
        if not sku or not any(r.get(f) for f in HIERARCHY_FIELDS):
            continue
        p = prod_lookup.get(sku)
        if p is None:
            prod_lookup[sku] = {"sku": sku, "name": sku, **{f: r[f] for f in HIERARCHY_FIELDS if r.get(f)}}
        else:
            for f in HIERARCHY_FIELDS:
                if not p.get(f) and r.get(f):
                    p[f] = r[f]


class AnalyticsService:
    @staticmethod
    async def get_filtered_data(filters: Dict[str, Any]):
        """Fetch and join sales, inventory, purchases, and products according to filters."""
        sales_coll = db_manager.get_collection("sales_transactions")
        inv_coll = db_manager.get_collection("inventory_snapshots")
        purch_coll = db_manager.get_collection("purchase_transactions")
        prod_coll = db_manager.get_collection("products")
        store_coll = db_manager.get_collection("stores")

        # Load masters for lookup
        products = await prod_coll.find({})
        prod_lookup = {p["sku"]: p for p in products}

        stores = await store_coll.find({})
        store_lookup = {s["store_id"]: s for s in stores}

        # Resolve TY and LY date ranges
        ty_from = filters.get("ty_date_from") or filters.get("date_from")
        ty_to = filters.get("ty_date_to") or filters.get("date_to")
        ly_from = filters.get("ly_date_from")
        ly_to = filters.get("ly_date_to")

        # If user gave TY dates but didn't specify LY dates, default LY to exact same duration 1 year prior
        if ty_from and not ly_from:
            ly_from = shift_date_years(ty_from, -1)
        if ty_to and not ly_to:
            ly_to = shift_date_years(ty_to, -1)

        # Query sales
        sales_query: Dict[str, Any] = {}
        if filters.get("stores"):
            sales_query["store_id"] = {"$in": filters["stores"]}
        
        # Date range filtering across both TY and LY
        if ty_from and ty_to and ly_from and ly_to:
            sales_query["$or"] = [
                {"date": {"$gte": ty_from, "$lte": ty_to}},
                {"date": {"$gte": ly_from, "$lte": ly_to}}
            ]
        elif ty_from and ty_to:
            sales_query["date"] = {"$gte": ty_from, "$lte": ty_to}

        all_sales = await sales_coll.find(sales_query)
        all_inv = await inv_coll.find({})
        # Stock is a position, not a flow: use only the latest snapshot of each store/site
        latest_snap: Dict[str, str] = {}
        for i in all_inv:
            if i.get("snapshot_date", "") > latest_snap.get(i["store_id"], ""):
                latest_snap[i["store_id"]] = i.get("snapshot_date", "")
        all_inv = [i for i in all_inv if i.get("snapshot_date", "") == latest_snap[i["store_id"]]]
        enrich_product_lookup(prod_lookup, all_sales)
        enrich_product_lookup(prod_lookup, all_inv)

        # Apply product hierarchy filtering and classify into TY/LY dynamically
        filtered_sales = []
        for s in all_sales:
            p = prod_lookup.get(s["sku"], {})
            if filters.get("divisions") and p.get("division") not in filters["divisions"]:
                continue
            if filters.get("sections") and p.get("section") not in filters["sections"]:
                continue
            if filters.get("departments") and p.get("department") not in filters["departments"]:
                continue
            if filters.get("categories") and p.get("category") not in filters["categories"]:
                continue
            if filters.get("brands") and p.get("brand") not in filters["brands"]:
                continue
            if filters.get("vendors") and p.get("vendor_id") not in filters["vendors"]:
                continue

            d = s.get("date", "")
            s_copy = dict(s)
            if ty_from and ty_to and ty_from <= d <= ty_to:
                s_copy["period_type"] = "TY"
                filtered_sales.append(s_copy)
            elif ly_from and ly_to and ly_from <= d <= ly_to:
                s_copy["period_type"] = "LY"
                filtered_sales.append(s_copy)
            elif not ty_from and not ty_to:
                filtered_sales.append(s)

        # Inventory: the store filter applies to shop stock only; warehouse stock stays visible
        filtered_inv = []
        for i in all_inv:
            if filters.get("stores") and not is_warehouse_location(i["store_id"]) and i["store_id"] not in filters["stores"]:
                continue
            p = prod_lookup.get(i["sku"], {})
            if filters.get("divisions") and p.get("division") not in filters["divisions"]:
                continue
            if filters.get("sections") and p.get("section") not in filters["sections"]:
                continue
            if filters.get("departments") and p.get("department") not in filters["departments"]:
                continue
            filtered_inv.append(i)

        warehouse_inv = [i for i in filtered_inv if is_warehouse_location(i["store_id"])]
        filtered_inv = [i for i in filtered_inv if not is_warehouse_location(i["store_id"])]

        # Query purchases
        purch_query: Dict[str, Any] = {}
        if filters.get("stores"):
            purch_query["store_id"] = {"$in": filters["stores"]}
        if filters.get("vendors"):
            purch_query["vendor_id"] = {"$in": filters["vendors"]}
        all_purch = await purch_coll.find(purch_query)

        return {
            "sales": filtered_sales,
            "inventory": filtered_inv,
            "warehouse_inventory": warehouse_inv,
            "purchases": all_purch,
            "products": prod_lookup,
            "stores": store_lookup
        }

    @classmethod
    async def get_kpi_summary(cls, filters: Dict[str, Any]) -> Dict[str, Any]:
        data = await cls.get_filtered_data(filters)
        sales = data["sales"]
        inventory = data["inventory"]
        purchases = data["purchases"]

        # Sales TY and LY
        ty_sales = sum(s["net_sales"] for s in sales if s.get("period_type") == "TY")
        ly_sales = sum(s["net_sales"] for s in sales if s.get("period_type") == "LY")
        ty_qty = sum(s["quantity"] for s in sales if s.get("period_type") == "TY")
        ly_qty = sum(s["quantity"] for s in sales if s.get("period_type") == "LY")
        cogs_ty = sum(s.get("cogs", 0) for s in sales if s.get("period_type") == "TY")

        growth_pct = calculate_growth_pct(ty_sales, ly_sales)
        growth_val = round(ty_sales - ly_sales, 2)
        qty_growth_pct = calculate_growth_pct(ty_qty, ly_qty)

        asp = round(ty_sales / ty_qty, 2) if ty_qty > 0 else 0.0
        ly_asp = round(ly_sales / ly_qty, 2) if ly_qty > 0 else 0.0

        gross_margin = round(ty_sales - cogs_ty, 2)
        gross_margin_pct = round((gross_margin / ty_sales) * 100, 2) if ty_sales > 0 else 0.0

        # Inventory
        stock_qty = sum(i["stock_qty"] for i in inventory)
        stock_value = sum(i["stock_value"] for i in inventory)
        warehouse_qty = sum(i["stock_qty"] for i in data["warehouse_inventory"])
        warehouse_value = sum(i["stock_value"] for i in data["warehouse_inventory"])

        # Stock cover days (Daily run rate = ty_qty / days)
        # Approximate period days as 90 (or distinct dates in TY)
        distinct_dates = len(set(s["date"] for s in sales if s.get("period_type") == "TY")) or 30
        daily_run_rate = ty_qty / distinct_dates if distinct_dates > 0 else 0.0
        stock_cover_days = round(stock_qty / daily_run_rate, 1) if daily_run_rate > 0 else None

        # Purchases
        purchase_qty = sum(p["quantity"] for p in purchases)
        purchase_val = sum(p["purchase_value"] for p in purchases)

        # Sell-Through % = Sales Qty / (Beginning Stock Qty + Purchase Qty)
        # Approximate Beginning Stock = Current Stock + TY Sales - Purchase
        denom = stock_qty + purchase_qty
        sell_through_pct = round((ty_qty / denom) * 100, 2) if denom > 0 else 0.0

        return {
            "total_sales": round(ty_sales, 2),
            "ly_sales": round(ly_sales, 2),
            "growth_pct": growth_pct,
            "growth_val": growth_val,
            "sales_qty": round(ty_qty, 0),
            "ly_sales_qty": round(ly_qty, 0),
            "sales_qty_growth_pct": qty_growth_pct,
            "asp": asp,
            "ly_asp": ly_asp,
            "gross_margin": gross_margin,
            "gross_margin_pct": gross_margin_pct,
            "stock_qty": stock_qty,
            "stock_value": round(stock_value, 2),
            "warehouse_qty": warehouse_qty,
            "warehouse_value": round(warehouse_value, 2),
            "stock_cover_days": stock_cover_days,
            "sell_through_pct": sell_through_pct,
            "purchase_qty": purchase_qty,
            "purchase_value": round(purchase_val, 2)
        }

    @classmethod
    async def get_sales_trend(cls, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = await cls.get_filtered_data(filters)
        sales = data["sales"]

        ty_from = filters.get("ty_date_from") or filters.get("date_from")
        ty_to = filters.get("ty_date_to") or filters.get("date_to")
        ly_from = filters.get("ly_date_from") or (shift_date_years(ty_from, -1) if ty_from else None)
        ly_to = filters.get("ly_date_to") or (shift_date_years(ty_to, -1) if ty_to else None)

        # Aggregate daily sales by period type
        ty_by_date: Dict[str, float] = {}
        ly_by_date: Dict[str, float] = {}
        for s in sales:
            d = s["date"]
            amt = s.get("net_sales", 0.0)
            if s.get("period_type") == "TY":
                ty_by_date[d] = ty_by_date.get(d, 0.0) + amt
            else:
                ly_by_date[d] = ly_by_date.get(d, 0.0) + amt

        trend_result = []
        if ty_from and ty_to:
            try:
                start_dt = datetime.strptime(ty_from, "%Y-%m-%d")
                end_dt = datetime.strptime(ty_to, "%Y-%m-%d")
                num_days = (end_dt - start_dt).days + 1

                ly_start_dt = datetime.strptime(ly_from, "%Y-%m-%d") if ly_from else None

                # For large ranges, sample or step to keep max ~45 points for clean display
                step = max(1, num_days // 45) if num_days > 45 else 1

                for i in range(0, num_days, step):
                    curr_ty = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
                    curr_ly = (ly_start_dt + timedelta(days=i)).strftime("%Y-%m-%d") if ly_start_dt else ""
                    
                    val_ty = round(ty_by_date.get(curr_ty, 0.0), 2)
                    val_ly = round(ly_by_date.get(curr_ly, 0.0), 2) if curr_ly else 0.0
                    
                    trend_result.append({
                        "date": curr_ty,
                        "short_date": curr_ty[5:],
                        "full_date": curr_ty,
                        "ty_date": curr_ty,
                        "ly_date": curr_ly,
                        "ty_sales": val_ty,
                        "ly_sales": val_ly,
                        "growth_pct": calculate_growth_pct(val_ty, val_ly)
                    })
            except Exception:
                pass

        if not trend_result:
            # Fallback
            daily: Dict[str, Dict[str, float]] = {}
            for s in sales:
                d = s["date"]
                ptype = s.get("period_type", "TY")
                if d not in daily:
                    daily[d] = {"date": d, "short_date": d[5:], "full_date": d, "ty_sales": 0.0, "ly_sales": 0.0}
                if ptype == "TY":
                    daily[d]["ty_sales"] += s["net_sales"]
                else:
                    daily[d]["ly_sales"] += s["net_sales"]

            sorted_daily = sorted(daily.values(), key=lambda x: x["full_date"])
            for item in sorted_daily:
                item["ty_sales"] = round(item["ty_sales"], 2)
                item["ly_sales"] = round(item["ly_sales"], 2)
                item["growth_pct"] = calculate_growth_pct(item["ty_sales"], item["ly_sales"])
            trend_result = sorted_daily[-30:] if len(sorted_daily) > 30 else sorted_daily

        return trend_result

    @classmethod
    async def get_department_performance(cls, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = await cls.get_filtered_data(filters)
        sales = data["sales"]
        prod_lookup = data["products"]

        depts: Dict[str, Dict[str, Any]] = {}
        total_ty = 0.0

        for s in sales:
            sku = s["sku"]
            p = prod_lookup.get(sku, {})
            dept_name = p.get("department", "Other")
            division = p.get("division", "Other")

            if dept_name not in depts:
                depts[dept_name] = {
                    "department": dept_name,
                    "division": division,
                    "ty_sales": 0.0,
                    "ly_sales": 0.0,
                    "ty_qty": 0.0,
                    "ly_qty": 0.0,
                    "cogs": 0.0
                }

            if s.get("period_type") == "TY":
                depts[dept_name]["ty_sales"] += s["net_sales"]
                depts[dept_name]["ty_qty"] += s["quantity"]
                depts[dept_name]["cogs"] += s.get("cogs", 0)
                total_ty += s["net_sales"]
            else:
                depts[dept_name]["ly_sales"] += s["net_sales"]
                depts[dept_name]["ly_qty"] += s["quantity"]

        result = []
        for d in depts.values():
            ty = d["ty_sales"]
            ly = d["ly_sales"]
            growth = calculate_growth_pct(ty, ly)
            margin = ty - d["cogs"]
            margin_pct = round((margin / ty) * 100, 2) if ty > 0 else 0.0
            contrib_pct = round((ty / total_ty) * 100, 2) if total_ty > 0 else 0.0
            asp = round(ty / d["ty_qty"], 2) if d["ty_qty"] > 0 else 0.0

            result.append({
                "department": d["department"],
                "division": d["division"],
                "ty_sales": round(ty, 2),
                "ly_sales": round(ly, 2),
                "growth_pct": growth,
                "growth_val": round(ty - ly, 2),
                "contribution_pct": contrib_pct,
                "gross_margin": round(margin, 2),
                "gross_margin_pct": margin_pct,
                "asp": asp,
                "ty_qty": d["ty_qty"]
            })

        return sorted(result, key=lambda x: x["ty_sales"], reverse=True)

    @classmethod
    async def get_store_performance(cls, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = await cls.get_filtered_data(filters)
        sales = data["sales"]
        inv = data["inventory"]
        purch = data["purchases"]
        store_lookup = data["stores"]

        stores_agg: Dict[str, Dict[str, Any]] = {}
        total_ty = sum(s["net_sales"] for s in sales if s.get("period_type") == "TY")

        for s in sales:
            st_id = s["store_id"]
            if st_id not in stores_agg:
                st_info = store_lookup.get(st_id, {})
                stores_agg[st_id] = {
                    "store_id": st_id,
                    "store_name": st_info.get("name", st_id),
                    "region": st_info.get("region", "East"),
                    "store_type": st_info.get("store_type", "Standard"),
                    "ty_sales": 0.0,
                    "ly_sales": 0.0,
                    "ty_qty": 0.0,
                    "cogs": 0.0,
                    "stock_qty": 0.0,
                    "stock_val": 0.0,
                    "purchase_val": 0.0
                }
            if s.get("period_type") == "TY":
                stores_agg[st_id]["ty_sales"] += s["net_sales"]
                stores_agg[st_id]["ty_qty"] += s["quantity"]
                stores_agg[st_id]["cogs"] += s.get("cogs", 0)
            else:
                stores_agg[st_id]["ly_sales"] += s["net_sales"]

        for i in inv:
            st_id = i["store_id"]
            if st_id in stores_agg:
                stores_agg[st_id]["stock_qty"] += i["stock_qty"]
                stores_agg[st_id]["stock_val"] += i["stock_value"]

        for p in purch:
            st_id = p["store_id"]
            if st_id in stores_agg:
                stores_agg[st_id]["purchase_val"] += p["purchase_value"]

        result = []
        for s in stores_agg.values():
            ty = s["ty_sales"]
            ly = s["ly_sales"]
            margin = ty - s["cogs"]
            result.append({
                "store_id": s["store_id"],
                "store_name": s["store_name"],
                "region": s["region"],
                "store_type": s["store_type"],
                "ty_sales": round(ty, 2),
                "ly_sales": round(ly, 2),
                "growth_pct": calculate_growth_pct(ty, ly),
                "contribution_pct": round((ty / total_ty) * 100, 2) if total_ty > 0 else 0.0,
                "asp": round(ty / s["ty_qty"], 2) if s["ty_qty"] > 0 else 0.0,
                "gross_margin_pct": round((margin / ty) * 100, 2) if ty > 0 else 0.0,
                "stock_qty": s["stock_qty"],
                "stock_value": round(s["stock_val"], 2),
                "purchase_value": round(s["purchase_val"], 2)
            })

        return sorted(result, key=lambda x: x["ty_sales"], reverse=True)

    @classmethod
    async def get_product_rankings(cls, filters: Dict[str, Any], limit: int = 10) -> Dict[str, Any]:
        data = await cls.get_filtered_data(filters)
        sales = data["sales"]
        prod_lookup = data["products"]

        prods_agg: Dict[str, Dict[str, Any]] = {}
        for s in sales:
            sku = s["sku"]
            p = prod_lookup.get(sku, {})
            if sku not in prods_agg:
                prods_agg[sku] = {
                    "sku": sku,
                    "name": p.get("name", sku),
                    "division": p.get("division", ""),
                    "department": p.get("department", ""),
                    "brand": p.get("brand", ""),
                    "mrp": p.get("mrp", 0.0),
                    "ty_sales": 0.0,
                    "ly_sales": 0.0,
                    "ty_qty": 0.0,
                    "cogs": 0.0
                }
            if s.get("period_type") == "TY":
                prods_agg[sku]["ty_sales"] += s["net_sales"]
                prods_agg[sku]["ty_qty"] += s["quantity"]
                prods_agg[sku]["cogs"] += s.get("cogs", 0)
            else:
                prods_agg[sku]["ly_sales"] += s["net_sales"]

        result = []
        for p in prods_agg.values():
            ty = p["ty_sales"]
            ly = p["ly_sales"]
            margin = ty - p["cogs"]
            result.append({
                "sku": p["sku"],
                "name": p["name"],
                "division": p["division"],
                "department": p["department"],
                "brand": p["brand"],
                "mrp": p["mrp"],
                "ty_sales": round(ty, 2),
                "ly_sales": round(ly, 2),
                "growth_pct": calculate_growth_pct(ty, ly),
                "ty_qty": p["ty_qty"],
                "gross_margin": round(margin, 2),
                "gross_margin_pct": round((margin / ty) * 100, 2) if ty > 0 else 0.0
            })

        sorted_by_sales = sorted(result, key=lambda x: x["ty_sales"], reverse=True)
        return {
            "top_products": sorted_by_sales[:limit],
            "bottom_products": sorted_by_sales[-limit:][::-1]
        }

    @classmethod
    async def get_inventory_analytics(cls, filters: Dict[str, Any]) -> Dict[str, Any]:
        data = await cls.get_filtered_data(filters)
        inventory = data["inventory"]
        sales = data["sales"]
        prod_lookup = data["products"]

        # Compute sales run rate per SKU for movement classification
        ty_sales_by_sku: Dict[str, float] = {}
        for s in sales:
            if s.get("period_type") == "TY":
                ty_sales_by_sku[s["sku"]] = ty_sales_by_sku.get(s["sku"], 0.0) + s["quantity"]

        # Aging buckets
        aging_buckets = {
            "0-30 days": {"qty": 0, "val": 0.0, "skus": 0},
            "31-60 days": {"qty": 0, "val": 0.0, "skus": 0},
            "61-90 days": {"qty": 0, "val": 0.0, "skus": 0},
            "91-180 days": {"qty": 0, "val": 0.0, "skus": 0},
            ">180 days": {"qty": 0, "val": 0.0, "skus": 0},
            "Unknown": {"qty": 0, "val": 0.0, "skus": 0}
        }

        # Movement classification
        movement = {
            "fast_moving": [],
            "normal_moving": [],
            "slow_moving": [],
            "non_moving": [],
            "out_of_stock": []
        }

        item_details = []
        for i in inventory:
            sku = i["sku"]
            p = prod_lookup.get(sku, {})
            age = i.get("age_days")
            stock_qty = i.get("stock_qty", 0)
            stock_val = i.get("stock_value", 0.0)

            # Assign aging bucket
            if age is None:
                b = "Unknown"
            elif age <= 30:
                b = "0-30 days"
            elif age <= 60:
                b = "31-60 days"
            elif age <= 90:
                b = "61-90 days"
            elif age <= 180:
                b = "91-180 days"
            else:
                b = ">180 days"

            aging_buckets[b]["qty"] += stock_qty
            aging_buckets[b]["val"] += stock_val
            aging_buckets[b]["skus"] += 1

            # Movement velocity
            sku_qty_sold = ty_sales_by_sku.get(sku, 0.0)
            daily_run_rate = sku_qty_sold / 90.0 if sku_qty_sold > 0 else 0.0
            cover_days = round(stock_qty / daily_run_rate, 1) if daily_run_rate > 0 else (999.0 if stock_qty > 0 else 0.0)

            classification = "normal_moving"
            if stock_qty <= 0:
                classification = "out_of_stock"
            elif daily_run_rate == 0:
                classification = "non_moving"
            elif cover_days < 15:
                classification = "fast_moving"
            elif cover_days > 75:
                classification = "slow_moving"

            movement_info = {
                "sku": sku,
                "name": p.get("name", sku),
                "store_id": i["store_id"],
                "stock_qty": stock_qty,
                "stock_value": round(stock_val, 2),
                "cover_days": cover_days,
                "age_days": age,
                "daily_run_rate": round(daily_run_rate, 2),
                "classification": classification
            }
            movement[classification].append(movement_info)
            item_details.append(movement_info)

        # Format aging bucket output for chart
        bucket_chart = [
            {"bucket": k, "stock_qty": v["qty"], "stock_value": round(v["val"], 2), "sku_count": v["skus"]}
            for k, v in aging_buckets.items()
        ]

        movement_summary = {
            "fast_moving_count": len(movement["fast_moving"]),
            "normal_moving_count": len(movement["normal_moving"]),
            "slow_moving_count": len(movement["slow_moving"]),
            "non_moving_count": len(movement["non_moving"]),
            "out_of_stock_count": len(movement["out_of_stock"]),
        }

        return {
            "aging_buckets": [b for b in bucket_chart if b["bucket"] != "Unknown" or b["sku_count"]],
            "warehouse": {
                "stock_qty": sum(i["stock_qty"] for i in data["warehouse_inventory"]),
                "stock_value": round(sum(i["stock_value"] for i in data["warehouse_inventory"]), 2),
                "sku_count": len({i["sku"] for i in data["warehouse_inventory"] if i["stock_qty"] > 0}),
            },
            "movement_summary": movement_summary,
            "items": item_details[:50]
        }

    @classmethod
    async def get_stock_gap(cls, filters: Dict[str, Any], target_cover_days: int = 30, limit: int = 200) -> Dict[str, Any]:
        """Stock gap = units short of the target cover, per store + SKU.

        Required stock = daily run rate x target cover days; gap = max(0, required - on-hand).
        Run rate comes from this-period sales of the same store + SKU over the selected date range.
        """
        target_cover_days = max(1, int(target_cover_days or 30))
        data = await cls.get_filtered_data(filters)
        inventory = data["inventory"]
        sales = [s for s in data["sales"] if s.get("period_type", "TY") == "TY"]
        prod_lookup = data["products"]

        empty = {
            "target_cover_days": target_cover_days, "has_inventory": bool(inventory), "period_days": 0,
            "summary": {"stockout_count": 0, "critical_count": 0, "low_count": 0, "gap_qty": 0, "gap_value": 0.0, "lines_checked": 0},
            "by_store": [], "items": [],
        }
        if not inventory or not sales:
            return empty

        # Days in the sales window: the selected range, else the span actually seen in the data
        d_from = filters.get("ty_date_from") or filters.get("date_from")
        d_to = filters.get("ty_date_to") or filters.get("date_to")
        if not (d_from and d_to):
            dates = [s["date"] for s in sales if s.get("date")]
            d_from, d_to = min(dates), max(dates)
        try:
            period_days = max(1, (datetime.strptime(d_to, "%Y-%m-%d") - datetime.strptime(d_from, "%Y-%m-%d")).days + 1)
        except ValueError:
            period_days = 90

        # Sales per store + SKU
        sold: Dict[tuple, Dict[str, float]] = {}
        for s in sales:
            agg = sold.setdefault((s["store_id"], s["sku"]), {"qty": 0.0, "net": 0.0})
            agg["qty"] += s.get("quantity", 0) or 0
            agg["net"] += s.get("net_sales", 0) or 0

        # Latest on-hand per store + SKU
        latest: Dict[tuple, Dict[str, Any]] = {}
        for i in inventory:
            key = (i["store_id"], i["sku"])
            if key not in latest or i.get("snapshot_date", "") >= latest[key].get("snapshot_date", ""):
                latest[key] = i

        warehouse_by_sku: Dict[str, float] = {}
        for w in data["warehouse_inventory"]:
            warehouse_by_sku[w["sku"]] = warehouse_by_sku.get(w["sku"], 0.0) + max(0.0, w.get("stock_qty", 0) or 0)

        items = []
        by_store: Dict[str, Dict[str, float]] = {}
        counts = {"stockout": 0, "critical": 0, "low": 0}
        for (store_id, sku), agg in sold.items():
            if agg["qty"] <= 0:
                continue
            on_hand = max(0.0, (latest.get((store_id, sku)) or {}).get("stock_qty", 0) or 0)
            run_rate = agg["qty"] / period_days
            cover = on_hand / run_rate
            required = run_rate * target_cover_days
            gap = max(0.0, required - on_hand)
            if gap <= 0:
                continue
            status = "stockout" if on_hand <= 0 else ("critical" if cover < 7 else "low")
            asp = agg["net"] / agg["qty"] if agg["qty"] else 0.0
            counts[status] += 1
            gap_qty = int(round(gap + 0.4999))  # round up to whole units
            gap_value = round(gap_qty * asp, 2)
            st = by_store.setdefault(store_id, {"store_id": store_id, "gap_qty": 0, "gap_value": 0.0, "lines": 0})
            st["gap_qty"] += gap_qty
            st["gap_value"] += gap_value
            st["lines"] += 1
            items.append({
                "sku": sku,
                "name": prod_lookup.get(sku, {}).get("name", sku),
                "store_id": store_id,
                "stock_qty": on_hand,
                "daily_run_rate": round(run_rate, 2),
                "cover_days": round(cover, 1),
                "required_qty": int(round(required + 0.4999)),
                "gap_qty": gap_qty,
                "gap_value": gap_value,
                "warehouse_qty": warehouse_by_sku.get(sku, 0),
                "status": status,
            })

        items.sort(key=lambda r: r["gap_value"], reverse=True)
        stores_out = sorted(by_store.values(), key=lambda r: r["gap_value"], reverse=True)
        for st in stores_out:
            st["gap_value"] = round(st["gap_value"], 2)

        return {
            "target_cover_days": target_cover_days,
            "has_inventory": True,
            "period_days": period_days,
            "summary": {
                "stockout_count": counts["stockout"],
                "critical_count": counts["critical"],
                "low_count": counts["low"],
                "gap_qty": sum(r["gap_qty"] for r in items),
                "gap_value": round(sum(r["gap_value"] for r in items), 2),
                "lines_checked": len(sold),
            },
            "by_store": stores_out[:15],
            "items": items[:limit],
        }

    @classmethod
    async def get_purchase_analytics(cls, filters: Dict[str, Any]) -> Dict[str, Any]:
        data = await cls.get_filtered_data(filters)
        purchases = data["purchases"]
        sales = data["sales"]
        vendor_coll = db_manager.get_collection("vendors")
        vendors = await vendor_coll.find({})
        vendor_lookup = {v["vendor_id"]: v for v in vendors}

        # Vendor aggregate
        vend_agg: Dict[str, Dict[str, Any]] = {}
        for p in purchases:
            vid = p["vendor_id"]
            vinfo = vendor_lookup.get(vid, {})
            if vid not in vend_agg:
                vend_agg[vid] = {
                    "vendor_id": vid,
                    "vendor_name": vinfo.get("name", vid),
                    "category": vinfo.get("category", "General"),
                    "po_count": 0,
                    "total_qty": 0,
                    "total_val": 0.0
                }
            vend_agg[vid]["po_count"] += 1
            vend_agg[vid]["total_qty"] += p["quantity"]
            vend_agg[vid]["total_val"] += p["purchase_value"]

        total_purch_val = sum(v["total_val"] for v in vend_agg.values())
        vendors_list = []
        for v in vend_agg.values():
            share = round((v["total_val"] / total_purch_val) * 100, 2) if total_purch_val > 0 else 0.0
            vendors_list.append({
                "vendor_id": v["vendor_id"],
                "vendor_name": v["vendor_name"],
                "category": v["category"],
                "po_count": v["po_count"],
                "purchase_qty": v["total_qty"],
                "purchase_value": round(v["total_val"], 2),
                "concentration_pct": share
            })

        # Purchase vs Sales comparison
        ty_sales_val = sum(s["net_sales"] for s in sales if s.get("period_type") == "TY")
        ty_sales_qty = sum(s["quantity"] for s in sales if s.get("period_type") == "TY")
        tot_purch_qty = sum(p["quantity"] for p in purchases)

        return {
            "vendor_performance": sorted(vendors_list, key=lambda x: x["purchase_value"], reverse=True),
            "purchase_vs_sales": {
                "purchase_value": round(total_purch_val, 2),
                "sales_value": round(ty_sales_val, 2),
                "purchase_qty": tot_purch_qty,
                "sales_qty": ty_sales_qty,
                "value_ratio": round(total_purch_val / ty_sales_val, 2) if ty_sales_val > 0 else 0.0,
                "qty_ratio": round(tot_purch_qty / ty_sales_qty, 2) if ty_sales_qty > 0 else 0.0
            },
            "recent_pos": purchases[-15:]
        }
