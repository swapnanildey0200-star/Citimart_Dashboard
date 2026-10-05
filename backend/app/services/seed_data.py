import random
from datetime import datetime, timedelta
import logging
from app.database import db_manager

logger = logging.getLogger("citimart.seed")

STORES = [
    {"store_id": "STR_CHOWRINGHEE", "name": "Citimart - Chowringhee", "region": "Central Kolkata", "store_type": "Flagship", "opening_date": "2018-05-15", "status": "Active"},
    {"store_id": "STR_GARIAHAT", "name": "Citimart - Gariahat", "region": "South Kolkata", "store_type": "Flagship", "opening_date": "2019-09-20", "status": "Active"},
    {"store_id": "STR_HATIBAGAN", "name": "Citimart - Hatibagan", "region": "North Kolkata", "store_type": "Regular", "opening_date": "2020-11-10", "status": "Active"},
    {"store_id": "STR_NEWMARKET", "name": "Citimart - New Market", "region": "Central Kolkata", "store_type": "Regular", "opening_date": "2021-03-01", "status": "Active"},
    {"store_id": "STR_BEHALA", "name": "Citimart - Behala", "region": "South West Kolkata", "store_type": "Outlet", "opening_date": "2022-08-15", "status": "Active"}
]

VENDORS = [
    {"vendor_id": "VEND_7144", "name": "IGS Apparels Pvt Ltd (Raphaaa)", "category": "Apparel", "contact": "igs@apparels.com", "lead_time_days": 12},
    {"vendor_id": "VEND_AVJP", "name": "Big Sky Fashion (Kartick Rajbanshi)", "category": "Menswear", "contact": "bigsky@textiles.com", "lead_time_days": 15},
    {"vendor_id": "VEND_7170", "name": "R D Fashion Kolkata", "category": "Ethnic Wear", "contact": "rdfashion@kolkata.in", "lead_time_days": 10},
    {"vendor_id": "VEND_6720", "name": "Mittal Fabrics Ltd", "category": "Textiles", "contact": "mittalfabrics@delhi.com", "lead_time_days": 20},
    {"vendor_id": "VEND_6310", "name": "Nandkishore Pannalal Household", "category": "Household", "contact": "nkpannalal@appliances.com", "lead_time_days": 18}
]

PRODUCTS = [
    # Raphaaa Menswear
    {"sku": "C880157", "name": "Raphaaa Crew Neck T-Shirt Slim", "division": "Raphaaa", "section": "Mens(R)", "department": "T-Shirts (Rm)", "category": "Casual", "brand": "Raphaaa", "style": "Polo", "color": "Navy Blue", "size": "L", "vendor_id": "VEND_7144", "mrp": 799.0, "cost_price": 380.0},
    {"sku": "C769273", "name": "Raphaaa Formal Oxford Cotton Shirt", "division": "Raphaaa", "section": "Mens(R)", "department": "Formal Shirts (Rm)", "category": "Formal", "brand": "Raphaaa", "style": "Button-down", "color": "Sky Blue", "size": "40", "vendor_id": "VEND_AVJP", "mrp": 1299.0, "cost_price": 590.0},
    {"sku": "C774102", "name": "Raphaaa Stretch Slim Fit Jeans", "division": "Raphaaa", "section": "Mens(R)", "department": "Jeans (Rm)", "category": "Denim", "brand": "Raphaaa", "style": "Mid-Rise", "color": "Dark Indigo", "size": "32", "vendor_id": "VEND_7144", "mrp": 1899.0, "cost_price": 890.0},
    # Ladies Ethnic
    {"sku": "C652190", "name": "Chanderi Silk Anarkali Kurti", "division": "Ladies Ethnic", "section": "Ethnic Wear", "department": "Kurtis", "category": "Festive", "brand": "Nilotpala", "style": "Anarkali", "color": "Maroon", "size": "M", "vendor_id": "VEND_7170", "mrp": 1599.0, "cost_price": 720.0},
    {"sku": "C658941", "name": "Handloom Pure Cotton Daily Kurti", "division": "Ladies Ethnic", "section": "Ethnic Wear", "department": "Kurtis", "category": "Casual", "brand": "Nilotpala", "style": "Straight Cut", "color": "Mustard Yellow", "size": "L", "vendor_id": "VEND_7170", "mrp": 999.0, "cost_price": 420.0},
    {"sku": "C661004", "name": "Banarasi Art Silk Zari Saree", "division": "Ladies Ethnic", "section": "Ethnic Wear", "department": "Sarees", "category": "Wedding", "brand": "Mittal", "style": "Traditional", "color": "Royal Crimson", "size": "Free", "vendor_id": "VEND_6720", "mrp": 3499.0, "cost_price": 1650.0},
    # Kids Department
    {"sku": "C540112", "name": "Boys Graphic Printed Cotton Tee", "division": "Kids", "section": "Boys Wear", "department": "Kids Casual", "category": "Tees", "brand": "Junior Citimart", "style": "Round Neck", "color": "Red", "size": "8Y", "vendor_id": "VEND_AVJP", "mrp": 499.0, "cost_price": 210.0},
    {"sku": "C543209", "name": "Girls Floral Frill Frock", "division": "Kids", "section": "Girls Wear", "department": "Kids Partywear", "category": "Dresses", "brand": "Junior Citimart", "style": "A-Line", "color": "Pink", "size": "6Y", "vendor_id": "VEND_AVJP", "mrp": 1199.0, "cost_price": 520.0},
    # Household Appliances
    {"sku": "C582453", "name": "Insulated Stainless Steel Lunch Box 3T", "division": "Household", "section": "Plasticware", "department": "Lunchware", "category": "Storage", "brand": "FreshMeal", "style": "Max", "color": "Silver/Blue", "size": "1.2L", "vendor_id": "VEND_6310", "mrp": 845.0, "cost_price": 410.0},
    {"sku": "C589320", "name": "Hard Anodized Non-Stick Kadhai with Lid", "division": "Household", "section": "Cookware", "department": "Pots & Pans", "category": "Kitchenware", "brand": "KitchenPro", "style": "Induction Base", "color": "Black", "size": "2.5L", "vendor_id": "VEND_6310", "mrp": 1450.0, "cost_price": 680.0}
]

ALERT_RULES = [
    {"rule_id": "RUL_SALES_DECLINE", "name": "Department Sales Decline (>15%)", "metric": "growth_pct", "condition": "drop_percentage", "threshold": -15.0, "severity": "critical", "is_active": True},
    {"rule_id": "RUL_STOCKOUT_RISK", "name": "Fast Moving Low Stock Cover (<7 days)", "metric": "stock_cover_days", "condition": "threshold_min", "threshold": 7.0, "severity": "critical", "is_active": True},
    {"rule_id": "RUL_OVERSTOCKED", "name": "Slow Moving Overstocked (>90 days cover)", "metric": "stock_cover_days", "condition": "threshold_max", "threshold": 90.0, "severity": "warning", "is_active": True},
    {"rule_id": "RUL_HIGH_AGING", "name": "Dead Stock / Aging (>120 days)", "metric": "age_days", "condition": "aging_days", "threshold": 120.0, "severity": "warning", "is_active": True},
    {"rule_id": "RUL_OVERPURCHASING", "name": "High Purchases with Weak Sell-Through (<25%)", "metric": "sell_through_pct", "condition": "threshold_min", "threshold": 25.0, "severity": "warning", "is_active": True}
]

async def seed_database(force: bool = False):
    """Populates realistic Citimart data for TY and LY."""
    stores_coll = db_manager.get_collection("stores")
    products_coll = db_manager.get_collection("products")
    vendors_coll = db_manager.get_collection("vendors")
    sales_coll = db_manager.get_collection("sales_transactions")
    inv_coll = db_manager.get_collection("inventory_snapshots")
    purch_coll = db_manager.get_collection("purchase_transactions")
    rules_coll = db_manager.get_collection("alert_rules")
    alerts_coll = db_manager.get_collection("generated_alerts")
    jobs_coll = db_manager.get_collection("import_jobs")

    count = await stores_coll.count_documents({})
    if count > 0 and not force:
        logger.info(f"Database already contains {count} stores. Skipping seed.")
        return

    logger.info("Seeding realistic retail master data and transactions...")
    await stores_coll.delete_many({})
    await products_coll.delete_many({})
    await vendors_coll.delete_many({})
    await sales_coll.delete_many({})
    await inv_coll.delete_many({})
    await purch_coll.delete_many({})
    await rules_coll.delete_many({})
    await alerts_coll.delete_many({})
    await jobs_coll.delete_many({})

    # Insert Masters
    await stores_coll.insert_many(STORES)
    await products_coll.insert_many(PRODUCTS)
    await vendors_coll.insert_many(VENDORS)
    await rules_coll.insert_many(ALERT_RULES)

    # Generate Sales Transactions for 90 days of TY (This Year: 2026) and comparable LY (2025)
    random.seed(42)
    sales_records = []
    base_ty_date = datetime(2026, 9, 30)
    base_ly_date = datetime(2025, 9, 30)

    for day_offset in range(90):
        ty_date = (base_ty_date - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        ly_date = (base_ly_date - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        
        for store in STORES:
            # Vary sales by store size
            store_mult = 1.3 if "Flagship" in store["store_type"] else 0.8
            
            for prod in PRODUCTS:
                # Specific retail scenario: Kids department drops 21% in TY due to supply gap in festive season!
                # Raphaaa T-Shirts surge 28% in TY!
                dept = prod["department"]
                is_kids = "Kids" in dept
                is_raphaaa_tee = prod["sku"] == "C880157"
                
                # TY base qty
                if is_kids:
                    ty_qty = max(0, int(random.gauss(3, 1.2) * store_mult * 0.75))
                    ly_qty = max(1, int(random.gauss(4, 1.2) * store_mult * 1.0))
                elif is_raphaaa_tee:
                    ty_qty = max(1, int(random.gauss(8, 2.0) * store_mult * 1.3))
                    ly_qty = max(1, int(random.gauss(6, 1.5) * store_mult * 1.0))
                else:
                    ty_qty = max(0, int(random.gauss(4, 1.5) * store_mult))
                    ly_qty = max(0, int(random.gauss(4, 1.4) * store_mult))

                discount_rate = 0.10 if random.random() > 0.6 else 0.0
                mrp = prod["mrp"]
                cost = prod["cost_price"]

                if ty_qty > 0:
                    net_ty = round(ty_qty * mrp * (1 - discount_rate), 2)
                    gross_ty = round(ty_qty * mrp, 2)
                    disc_ty = round(gross_ty - net_ty, 2)
                    cogs_ty = round(ty_qty * cost, 2)
                    sales_records.append({
                        "transaction_id": f"TX_TY_{ty_date}_{store['store_id']}_{prod['sku']}",
                        "date": ty_date,
                        "store_id": store["store_id"],
                        "sku": prod["sku"],
                        "quantity": ty_qty,
                        "selling_price": mrp,
                        "gross_sales": gross_ty,
                        "discount": disc_ty,
                        "net_sales": net_ty,
                        "rsp": mrp,
                        "cogs": cogs_ty,
                        "is_void": False,
                        "period_type": "TY",
                        "import_job_id": "INIT_SEED"
                    })

                if ly_qty > 0:
                    net_ly = round(ly_qty * mrp * (1 - discount_rate), 2)
                    gross_ly = round(ly_qty * mrp, 2)
                    disc_ly = round(gross_ly - net_ly, 2)
                    cogs_ly = round(ly_qty * cost, 2)
                    sales_records.append({
                        "transaction_id": f"TX_LY_{ly_date}_{store['store_id']}_{prod['sku']}",
                        "date": ly_date,
                        "store_id": store["store_id"],
                        "sku": prod["sku"],
                        "quantity": ly_qty,
                        "selling_price": mrp,
                        "gross_sales": gross_ly,
                        "discount": disc_ly,
                        "net_sales": net_ly,
                        "rsp": mrp,
                        "cogs": cogs_ly,
                        "is_void": False,
                        "period_type": "LY",
                        "import_job_id": "INIT_SEED"
                    })

    await sales_coll.insert_many(sales_records)

    # Generate Inventory Snapshots (Current stock as on 2026-09-30)
    inventory_records = []
    for store in STORES:
        for prod in PRODUCTS:
            # Raphaaa T-Shirt has very low stock (fast moving stockout risk)
            # Banarasi Art Silk Saree has high stock (aging >120 days)
            if prod["sku"] == "C880157":
                stock_qty = random.randint(8, 22)
                age_days = random.randint(10, 25)
            elif prod["sku"] == "C661004":
                stock_qty = random.randint(75, 120)
                age_days = random.randint(110, 210)
            elif "Kids" in prod["department"]:
                stock_qty = random.randint(15, 35)
                age_days = random.randint(40, 85)
            else:
                stock_qty = random.randint(30, 80)
                age_days = random.randint(15, 75)

            cost = prod["cost_price"]
            stock_val = round(stock_qty * cost, 2)
            rcpt_date = (base_ty_date - timedelta(days=age_days)).strftime("%Y-%m-%d")

            inventory_records.append({
                "snapshot_date": "2026-09-30",
                "store_id": store["store_id"],
                "sku": prod["sku"],
                "stock_qty": stock_qty,
                "unit_cost": cost,
                "stock_value": stock_val,
                "last_sale_date": "2026-09-29",
                "receipt_date": rcpt_date,
                "age_days": age_days,
                "import_job_id": "INIT_SEED"
            })

    await inv_coll.insert_many(inventory_records)

    # Generate Purchases (GRN records over past 90 days)
    purchase_records = []
    for i in range(40):
        po_date = (base_ty_date - timedelta(days=random.randint(5, 80))).strftime("%Y-%m-%d")
        store = random.choice(STORES)
        prod = random.choice(PRODUCTS)
        qty = random.randint(40, 150)
        cost = prod["cost_price"]
        purch_val = round(qty * cost, 2)
        purchase_records.append({
            "po_id": f"PO_{1000 + i}",
            "date": po_date,
            "store_id": store["store_id"],
            "vendor_id": prod["vendor_id"],
            "sku": prod["sku"],
            "quantity": qty,
            "unit_cost": cost,
            "purchase_value": purch_val,
            "grc_no": f"GRC/0000{200 + i}/26-27",
            "import_job_id": "INIT_SEED"
        })

    await purch_coll.insert_many(purchase_records)

    # Pre-generate Initial Decision Support Alerts (What, Where, Why, Action)
    initial_alerts = [
        {
            "alert_id": "ALT_001",
            "rule_id": "RUL_SALES_DECLINE",
            "severity": "critical",
            "title": "Kids Department Sales Drop (-21.4%)",
            "what_happened": "Kids Department sales declined by 21.4% (TY ₹6.82L vs LY ₹8.68L).",
            "where_happened": "Kids Department across all stores, led by Gariahat & New Market.",
            "why_happened": "Stock gap in fast-moving Boys Graphic Printed Cotton Tees (C540112) leading to unfulfilled demand.",
            "action_recommended": "Expedite vendor delivery from Big Sky Fashion (VEND_AVJP) and replenish 250 units to Gariahat.",
            "metric_value": -21.4,
            "threshold_value": -15.0,
            "status": "new",
            "target_page": "sales",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "alert_id": "ALT_002",
            "rule_id": "RUL_STOCKOUT_RISK",
            "severity": "critical",
            "title": "Fast-Moving Stockout Risk: Raphaaa Slim Polo (C880157)",
            "what_happened": "Stock cover dropped to 4.2 days (Current Stock: 14 units, Daily Run Rate: 3.3 units/day).",
            "where_happened": "Citimart - Chowringhee (Flagship).",
            "why_happened": "High sales velocity surge (+32% TY growth) without corresponding mid-month replenishment.",
            "action_recommended": "Transfer 35 units from Central Warehouse or place emergency PO with IGS Apparels (VEND_7144).",
            "metric_value": 4.2,
            "threshold_value": 7.0,
            "status": "new",
            "target_page": "inventory",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "alert_id": "ALT_003",
            "rule_id": "RUL_HIGH_AGING",
            "severity": "warning",
            "title": "High Ageing Stock: Banarasi Art Silk Saree (C661004)",
            "what_happened": "98 units exceeding 150+ days in stock with tied-up capital of ₹1.62 Lakhs.",
            "where_happened": "Citimart - Hatibagan & Behala stores.",
            "why_happened": "High retail price point (₹3,499) with zero promotional discount during non-wedding quarter.",
            "action_recommended": "Run 20% festive clearance bundle promotion or initiate vendor return/credit note with Mittal Fabrics.",
            "metric_value": 155.0,
            "threshold_value": 120.0,
            "status": "new",
            "target_page": "inventory",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "alert_id": "ALT_004",
            "rule_id": "RUL_OVERPURCHASING",
            "severity": "warning",
            "title": "Over-Purchasing Alert: Handloom Daily Kurti (C658941)",
            "what_happened": "Purchase volume exceeds quarterly sales rate by 2.4x; Sell-Through is only 18.5%.",
            "where_happened": "Central Procurement / Citimart - Gariahat.",
            "why_happened": "Advance bulk ordering without monitoring existing 45-day warehouse inventory.",
            "action_recommended": "Pause next week's PO delivery with R D Fashion and reallocate existing stock to high-traffic stores.",
            "metric_value": 18.5,
            "threshold_value": 25.0,
            "status": "new",
            "target_page": "purchases",
            "created_at": datetime.utcnow().isoformat()
        }
    ]

    await alerts_coll.insert_many(initial_alerts)

    # Initial Import Job record
    await jobs_coll.insert_one({
        "job_id": "INIT_SEED",
        "data_type": "sales",
        "file_name": "Citimart_Historical_90D_Seed.xlsx",
        "file_size_bytes": 1048576,
        "total_rows": len(sales_records),
        "valid_rows": len(sales_records),
        "invalid_rows": 0,
        "duplicate_rows": 0,
        "warning_count": 0,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
        "error_summary": "Initial system seed data loaded successfully."
    })

    logger.info(f"Database seeded successfully with {len(sales_records)} sales rows, {len(inventory_records)} stock snapshots, and {len(initial_alerts)} alerts!")
