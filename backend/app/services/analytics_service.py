from typing import Dict, Any, List, Optional
from datetime import datetime
from app.database import db_manager

def calculate_growth_pct(ty: float, ly: float) -> Optional[float]:
    """Calculate percentage growth safely, handling LY=0 without division error."""
    if ly and ly > 0:
        return round(((ty - ly) / ly) * 100, 2)
    elif ty > 0 and (ly is None or ly == 0):
        return None  # New item / entry
    return 0.0

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

        # Query sales
        sales_query: Dict[str, Any] = {}
        if filters.get("stores"):
            sales_query["store_id"] = {"$in": filters["stores"]}
        
        # Date range filtering
        if filters.get("date_from") and filters.get("date_to"):
            sales_query["date"] = {"$gte": filters["date_from"], "$lte": filters["date_to"]}

        all_sales = await sales_coll.find(sales_query)

        # Apply product hierarchy filtering in memory
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
            filtered_sales.append(s)

        # Query inventory
        inv_query: Dict[str, Any] = {}
        if filters.get("stores"):
            inv_query["store_id"] = {"$in": filters["stores"]}
        all_inv = await inv_coll.find(inv_query)
        filtered_inv = []
        for i in all_inv:
            p = prod_lookup.get(i["sku"], {})
            if filters.get("divisions") and p.get("division") not in filters["divisions"]:
                continue
            if filters.get("departments") and p.get("department") not in filters["departments"]:
                continue
            filtered_inv.append(i)

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
            "stock_cover_days": stock_cover_days,
            "sell_through_pct": sell_through_pct,
            "purchase_qty": purchase_qty,
            "purchase_value": round(purchase_val, 2)
        }

    @classmethod
    async def get_sales_trend(cls, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = await cls.get_filtered_data(filters)
        sales = data["sales"]

        # Aggregate daily sales
        daily: Dict[str, Dict[str, float]] = {}
        for s in sales:
            d = s["date"]
            ptype = s.get("period_type", "TY")
            if d not in daily:
                daily[d] = {"date": d, "ty_sales": 0.0, "ly_sales": 0.0, "ty_qty": 0.0, "ly_qty": 0.0}
            if ptype == "TY":
                daily[d]["ty_sales"] += s["net_sales"]
                daily[d]["ty_qty"] += s["quantity"]
            else:
                daily[d]["ly_sales"] += s["net_sales"]
                daily[d]["ly_qty"] += s["quantity"]

        # Sort chronologically and take recent 30-day window for compact display
        sorted_daily = sorted(daily.values(), key=lambda x: x["date"])
        # Format values
        for item in sorted_daily:
            item["ty_sales"] = round(item["ty_sales"], 2)
            item["ly_sales"] = round(item["ly_sales"], 2)
            item["growth_pct"] = calculate_growth_pct(item["ty_sales"], item["ly_sales"])

        return sorted_daily[-30:] if len(sorted_daily) > 30 else sorted_daily

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
            ">180 days": {"qty": 0, "val": 0.0, "skus": 0}
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
            age = i.get("age_days", 0)
            stock_qty = i.get("stock_qty", 0)
            stock_val = i.get("stock_value", 0.0)

            # Assign aging bucket
            if age <= 30:
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
            "aging_buckets": bucket_chart,
            "movement_summary": movement_summary,
            "items": item_details[:50]
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
