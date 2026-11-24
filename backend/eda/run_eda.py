"""Exploratory data analysis for the Citimart sales and stock exports.

Usage (from backend/):
    venv/Scripts/python eda/run_eda.py [--data ../Data] [--out eda/output]

Writes eda/output/eda_report.md plus one CSV per table. Needs only pandas + openpyxl.
It applies the same cleaning rules as the importer (drop total rows, void bills, negative stock).
"""
import argparse
import re
from pathlib import Path

import pandas as pd

SALES_COLS = {
    "date": ["bill date"], "store": ["store"], "division": ["division"], "section": ["section"],
    "department": ["department"], "vendor": ["vendor"], "sku": ["item code"], "is_void": ["isvoid"],
    "brand": ["cat-2 (brand)"], "style": ["cat-3 (style)"], "size": ["cat-5 (size)"],
    "received_month": ["ageing"], "unit_cost": ["std rate"], "mrp": ["mrp"], "promo_type": ["promo type"],
    "qty": ["bill qty"], "gross": ["gr amt"], "promo_amt": ["promo amt"], "discount": ["discount amt"],
    "net": ["net amt"], "bill_no": ["bill no."], "bill_time": ["bill time"],
}
STOCK_COLS = {
    "site": ["source site"], "location": ["locname"], "division": ["division"], "section": ["section"],
    "department": ["department"], "vendor": ["vendor"], "sku": ["item_code"], "brand": ["category2"],
    "style": ["category3"], "size": ["category5"], "received_month": ["category6"],
    "unit_cost": ["standard_rate"], "mrp": ["mrp"], "qty": ["closing_qty"], "value": ["closing_amt"],
}
NUMERIC_SALES = ["qty", "gross", "promo_amt", "discount", "net", "unit_cost", "mrp"]
NUMERIC_STOCK = ["qty", "value", "unit_cost", "mrp"]


def read_table(path: Path, columns: dict, anchor: str) -> pd.DataFrame:
    """Finds the header row (the one containing `anchor`), maps columns by name and returns the table."""
    raw = pd.read_excel(path, header=None, dtype=object)
    header_idx = next(i for i in range(min(15, len(raw)))
                      if anchor in {str(v).strip().lower() for v in raw.iloc[i].values})
    names = [str(v).strip().lower() for v in raw.iloc[header_idx].values]
    df = raw.iloc[header_idx + 1:].reset_index(drop=True)
    df.columns = names
    out = {}
    for field, aliases in columns.items():
        col = next((a for a in aliases if a in names), None)
        if col is not None:
            out[field] = df[col]
    return pd.DataFrame(out)


def clean_sales(df: pd.DataFrame):
    n0 = len(df)
    df = df[df["date"].notna() & df["sku"].notna()]
    df = df[~df["date"].astype(str).str.lower().str.contains("total")]  # report total rows
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()].copy()
    for c in NUMERIC_SALES:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    n_void = int((df["is_void"].astype(str).str.lower() == "yes").sum())
    df = df[df["is_void"].astype(str).str.lower() != "yes"].copy()
    df["cogs"] = df["qty"] * df["unit_cost"]
    df["margin"] = df["net"] - df["cogs"]
    df["is_return"] = df["qty"] < 0
    df["dow"] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df, {"raw_rows": n0, "total_rows_dropped": n0 - len(df) - n_void, "void_dropped": n_void}


def clean_stock(df: pd.DataFrame):
    df = df[df["sku"].notna()].copy()
    for c in NUMERIC_STOCK:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    neg = int((df["qty"] < 0).sum())
    df["qty_clean"] = df["qty"].clip(lower=0)
    df["value_clean"] = df["value"].where(df["qty"] >= 0, 0)
    rm = pd.to_datetime(df["received_month"].astype(str).str.strip(), format="%m/%y", errors="coerce")
    df["age_days"] = (pd.Timestamp("2026-11-13") - rm).dt.days
    return df, {"negative_stock_rows": neg}


def profile(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "non_null_pct": (df.notna().mean() * 100).round(1),
        "unique": df.nunique(),
        "dtype": df.dtypes.astype(str),
        "example": df.apply(lambda s: str(s.dropna().iloc[0])[:30] if s.notna().any() else ""),
    })


def top(df, by, value, n=15, agg="sum"):
    return df.groupby(by, dropna=False)[value].agg(agg).sort_values(ascending=False).head(n).round(0)


def md(title: str, obj) -> str:
    return f"\n### {title}\n\n```\n{obj.to_string()}\n```\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="../Data")
    ap.add_argument("--out", default="eda/output")
    args = ap.parse_args()
    data, out = Path(args.data), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    sales_file = next(data.glob("DAY WISE SALE*.xlsx"))
    stock_file = next(data.glob("STOCK AS ON*.xlsx"))
    sales, s_info = clean_sales(read_table(sales_file, SALES_COLS, "bill date"))
    stock, k_info = clean_stock(read_table(stock_file, STOCK_COLS, "item_code"))

    tables = {}
    # ---- Sales
    tables["sales_profile"] = profile(sales)
    daily = sales.groupby("date").agg(net=("net", "sum"), qty=("qty", "sum"), bills=("bill_no", "nunique"))
    daily["atv"] = (daily["net"] / daily["bills"]).round(0)
    tables["sales_daily"] = daily.round(0)
    tables["sales_by_month"] = sales.groupby("month").agg(net=("net", "sum"), qty=("qty", "sum"), margin=("margin", "sum")).round(0)
    tables["sales_by_dow"] = sales.groupby("dow")["net"].sum().round(0)
    tables["sales_by_store"] = sales.groupby("store").agg(
        net=("net", "sum"), qty=("qty", "sum"), bills=("bill_no", "nunique"),
        discount=("discount", "sum"), promo=("promo_amt", "sum"), margin=("margin", "sum")).round(0)
    tables["sales_by_division"] = top(sales, "division", "net")
    tables["sales_by_section"] = top(sales, "section", "net", 20)
    tables["sales_by_department"] = top(sales, "department", "net", 25)
    tables["sales_by_vendor"] = top(sales, "vendor", "net", 20)
    tables["sales_by_brand"] = top(sales, "brand", "net", 20)
    tables["sales_by_size"] = top(sales, "size", "net", 20)
    tables["sales_by_ageing"] = top(sales, "received_month", "net", 20)
    tables["promo_split"] = sales.assign(promo=sales["promo_type"].fillna("None")).groupby("promo").agg(
        net=("net", "sum"), qty=("qty", "sum"), discount=("discount", "sum"), promo_amt=("promo_amt", "sum")).round(0)
    sku = sales.groupby("sku").agg(net=("net", "sum"), qty=("qty", "sum")).sort_values("net", ascending=False)
    sku["cum_share_pct"] = (sku["net"].cumsum() / sku["net"].sum() * 100).round(1)
    tables["sku_pareto_top"] = sku.head(30).round(0)
    basket = sales.groupby("bill_no").agg(lines=("sku", "size"), units=("qty", "sum"), value=("net", "sum"))
    tables["basket_stats"] = basket.describe().round(1)
    tables["returns_by_store"] = sales[sales["is_return"]].groupby("store").agg(rows=("qty", "size"), value=("net", "sum")).round(0)
    if "bill_time" in sales:
        hours = pd.to_datetime(sales["bill_time"], errors="coerce").dt.hour
        tables["sales_by_hour"] = sales.groupby(hours)["net"].sum().round(0)

    # ---- Stock
    tables["stock_profile"] = profile(stock)
    tables["stock_by_site"] = stock.groupby("site").agg(
        skus=("sku", "nunique"), qty=("qty_clean", "sum"), value=("value_clean", "sum")).round(0)
    tables["stock_by_division"] = top(stock, "division", "value_clean")
    tables["stock_by_department"] = top(stock, "department", "value_clean", 25)
    bins = [-1, 90, 180, 365, 730, 10**6]
    labels = ["0-90d", "91-180d", "181-365d", "1-2y", ">2y"]
    stock["age_bucket"] = pd.cut(stock["age_days"], bins=bins, labels=labels)
    tables["stock_ageing"] = stock.groupby("age_bucket", observed=False).agg(
        rows=("sku", "size"), qty=("qty_clean", "sum"), value=("value_clean", "sum")).round(0)

    # ---- Sales vs stock join (sell-through, cover, dead stock)
    days = max((sales["date"].max() - sales["date"].min()).days + 1, 1)
    sold = sales.groupby("sku").agg(sold_qty=("qty", "sum"), sold_net=("net", "sum"))
    held = stock.groupby("sku").agg(stock_qty=("qty_clean", "sum"), stock_value=("value_clean", "sum"))
    j = held.join(sold, how="outer").fillna(0)
    j["daily_rate"] = j["sold_qty"] / days
    j["cover_days"] = (j["stock_qty"] / j["daily_rate"]).where(j["daily_rate"] > 0)
    j["sell_through_pct"] = (j["sold_qty"] / (j["sold_qty"] + j["stock_qty"]) * 100).where(j["sold_qty"] + j["stock_qty"] > 0)
    tables["sku_stock_sales"] = j.round(2).sort_values("stock_value", ascending=False)
    cov = {
        "skus_sold": int((j["sold_qty"] > 0).sum()),
        "skus_in_stock": int((j["stock_qty"] > 0).sum()),
        "sold_but_no_stock": int(((j["sold_qty"] > 0) & (j["stock_qty"] <= 0)).sum()),
        "stock_no_sale_in_period (dead)": int(((j["stock_qty"] > 0) & (j["sold_qty"] <= 0)).sum()),
        "dead_stock_value": round(float(j.loc[(j["stock_qty"] > 0) & (j["sold_qty"] <= 0), "stock_value"].sum())),
    }
    tables["stock_vs_sales_summary"] = pd.Series(cov, name="value")

    # ---- Outputs
    for name, t in tables.items():
        t.to_csv(out / f"{name}.csv")
    summary = pd.Series({
        "sales_period": f"{sales['date'].min().date()} to {sales['date'].max().date()} ({days} days)",
        "sales_rows_clean": len(sales), **s_info,
        "stores": sales["store"].nunique(), "skus_sold": sales["sku"].nunique(),
        "bills": sales["bill_no"].nunique(), "net_sales": round(float(sales["net"].sum())),
        "est_margin_pct": round(float(sales["margin"].sum() / sales["net"].sum() * 100), 1),
        "stock_rows": len(stock), "stock_skus": stock["sku"].nunique(), **k_info,
        "stock_value_clean": round(float(stock["value_clean"].sum())),
    }, name="value")
    report = ["# Citimart EDA report", md("Summary", summary)]
    report += [md(n, t) for n, t in tables.items() if n != "sku_stock_sales"]
    (out / "eda_report.md").write_text("".join(report), encoding="utf-8")
    print(summary.to_string())
    print(f"\nReport and {len(tables)} CSVs written to {out.resolve()}")


if __name__ == "__main__":
    main()
