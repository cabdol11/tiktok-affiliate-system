#!/usr/bin/env python3
"""
affiliate_tracker.py
--------------------
Tracks affiliate links across multiple networks.
Monitors CTR, conversion rates, EPC, and generates weekly P&L reports.
Alerts when a product's conversion rate drops below threshold.

Usage:
    python affiliate_tracker.py add-product      # Register a new affiliate product
    python affiliate_tracker.py log-click        # Record a click event
    python affiliate_tracker.py log-sale         # Record a sale/conversion
    python affiliate_tracker.py report           # Weekly P&L report
    python affiliate_tracker.py health           # Check for underperforming products
    python affiliate_tracker.py dashboard        # Full dashboard view
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
PRODUCTS_FILE = DATA_DIR / "affiliate_products.json"
CLICKS_FILE = DATA_DIR / "clicks_log.json"
SALES_FILE = DATA_DIR / "sales_log.json"

# Alert threshold: if CVR drops below this, flag the product
CVR_ALERT_THRESHOLD = 0.02  # 2%
# Minimum clicks before CVR alert fires (avoid false positives on new products)
MIN_CLICKS_FOR_ALERT = 50

NETWORKS = [
    "TikTok Shop",
    "Amazon Associates",
    "ClickBank",
    "ShareASale",
    "Impact",
    "CJ Affiliate",
    "Rakuten",
    "FlexOffers",
    "Direct",
]

# Monthly tool/overhead costs — adjust to your actual stack
MONTHLY_OVERHEAD = {
    "CapCut Pro": 7.99,
    "Canva Pro": 12.99,
    "ConvertKit": 29.00,
    "Beacons.ai Pro": 10.00,
    "VidIQ Pro": 16.58,
    "Notion": 0.00,  # free tier
    "RedTrack": 149.00,  # advanced tracking (add at scale)
}

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_products():
    return load_json(PRODUCTS_FILE, {})


def save_products(data):
    save_json(PRODUCTS_FILE, data)


def load_clicks():
    return load_json(CLICKS_FILE, [])


def save_clicks(data):
    save_json(CLICKS_FILE, data)


def load_sales():
    return load_json(SALES_FILE, [])


def save_sales(data):
    save_json(SALES_FILE, data)

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def add_product(product_id: str, name: str, network: str, commission: float,
                affiliate_url: str, niche: str, avg_order_value: float = 0.0) -> dict:
    """Register a new affiliate product."""
    products = load_products()
    if product_id in products:
        raise ValueError(f"Product {product_id} already exists.")

    product = {
        "id": product_id,
        "name": name,
        "network": network,
        "commission_usd": commission,
        "avg_order_value": avg_order_value,
        "affiliate_url": affiliate_url,
        "niche": niche,
        "status": "active",
        "added_at": datetime.now().isoformat(),
        "tags": [],
    }
    products[product_id] = product
    save_products(products)
    return product


def record_click(product_id: str, source_video_id: str = "",
                 source_platform: str = "tiktok") -> dict:
    """Record a click event for a product."""
    products = load_products()
    if product_id not in products:
        raise ValueError(f"Product {product_id} not found. Add it first.")

    click = {
        "id": f"clk_{int(datetime.now().timestamp() * 1000)}",
        "product_id": product_id,
        "source_video_id": source_video_id,
        "source_platform": source_platform,
        "timestamp": datetime.now().isoformat(),
    }
    clicks = load_clicks()
    clicks.append(click)
    save_clicks(clicks)
    return click


def record_sale(product_id: str, commission_earned: float,
                order_value: float = 0.0, source_video_id: str = "",
                network_transaction_id: str = "") -> dict:
    """Record a confirmed sale/conversion."""
    products = load_products()
    if product_id not in products:
        raise ValueError(f"Product {product_id} not found.")

    sale = {
        "id": f"sale_{int(datetime.now().timestamp() * 1000)}",
        "product_id": product_id,
        "commission_earned_usd": commission_earned,
        "order_value_usd": order_value,
        "source_video_id": source_video_id,
        "network_transaction_id": network_transaction_id,
        "timestamp": datetime.now().isoformat(),
    }
    sales = load_sales()
    sales.append(sale)
    save_sales(sales)
    return sale


def compute_product_stats(product_id: str, since: datetime = None,
                           until: datetime = None) -> dict:
    """Compute CTR, CVR, EPC for a product over a time range."""
    clicks = load_clicks()
    sales = load_sales()

    def in_range(ts_str):
        ts = datetime.fromisoformat(ts_str)
        if since and ts < since:
            return False
        if until and ts >= until:
            return False
        return True

    product_clicks = [c for c in clicks if c["product_id"] == product_id and in_range(c["timestamp"])]
    product_sales = [s for s in sales if s["product_id"] == product_id and in_range(s["timestamp"])]

    total_clicks = len(product_clicks)
    total_sales = len(product_sales)
    total_commission = sum(s["commission_earned_usd"] for s in product_sales)
    total_order_value = sum(s["order_value_usd"] for s in product_sales)

    cvr = total_sales / total_clicks if total_clicks > 0 else 0.0
    epc = total_commission / total_clicks if total_clicks > 0 else 0.0
    aov = total_order_value / total_sales if total_sales > 0 else 0.0

    return {
        "product_id": product_id,
        "total_clicks": total_clicks,
        "total_sales": total_sales,
        "total_commission_usd": round(total_commission, 2),
        "cvr_pct": round(cvr * 100, 3),
        "epc_usd": round(epc, 4),
        "avg_order_value_usd": round(aov, 2),
        "cvr_alert": (total_clicks >= MIN_CLICKS_FOR_ALERT and cvr < CVR_ALERT_THRESHOLD),
    }


def weekly_pnl(weeks_back: int = 0, weekly_ad_spend: float = 0.0) -> dict:
    """Generate a weekly P&L report."""
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday(), weeks=weeks_back)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=7)

    sales = load_sales()
    week_sales = [
        s for s in sales
        if week_start <= datetime.fromisoformat(s["timestamp"]) < week_end
    ]

    gross_revenue = sum(s["commission_earned_usd"] for s in week_sales)
    weekly_overhead = sum(MONTHLY_OVERHEAD.values()) / 4.33  # monthly → weekly
    net_profit = gross_revenue - weekly_ad_spend - weekly_overhead

    # Breakdown by product
    product_breakdown = {}
    for s in week_sales:
        pid = s["product_id"]
        product_breakdown[pid] = product_breakdown.get(pid, 0) + s["commission_earned_usd"]

    top_product = max(product_breakdown, key=product_breakdown.get) if product_breakdown else "N/A"

    # Breakdown by network
    products = load_products()
    network_breakdown = {}
    for s in week_sales:
        pid = s["product_id"]
        network = products.get(pid, {}).get("network", "Unknown")
        network_breakdown[network] = network_breakdown.get(network, 0) + s["commission_earned_usd"]

    return {
        "week_of": str(week_start.date()),
        "total_sales": len(week_sales),
        "gross_revenue_usd": round(gross_revenue, 2),
        "ad_spend_usd": round(weekly_ad_spend, 2),
        "overhead_usd": round(weekly_overhead, 2),
        "net_profit_usd": round(net_profit, 2),
        "profit_margin_pct": round(net_profit / gross_revenue * 100, 1) if gross_revenue > 0 else 0,
        "top_product_id": top_product,
        "top_product_revenue": round(product_breakdown.get(top_product, 0), 2),
        "by_product": {k: round(v, 2) for k, v in sorted(product_breakdown.items(), key=lambda x: -x[1])},
        "by_network": {k: round(v, 2) for k, v in sorted(network_breakdown.items(), key=lambda x: -x[1])},
    }


def health_check() -> list:
    """Return list of products with CVR alerts or inactivity."""
    products = load_products()
    alerts = []
    for pid, product in products.items():
        if product.get("status") != "active":
            continue
        stats = compute_product_stats(pid)
        if stats["cvr_alert"]:
            alerts.append({
                "product_id": pid,
                "name": product["name"],
                "network": product["network"],
                "clicks": stats["total_clicks"],
                "cvr_pct": stats["cvr_pct"],
                "alert": f"CVR {stats['cvr_pct']}% is below {CVR_ALERT_THRESHOLD*100}% threshold",
                "recommendation": "Pause this product. Test new hook or swap to competing product.",
            })
    return alerts


def projection_to_10k(current_weekly_net: float,
                       weekly_growth_rate: float = 0.20) -> dict:
    """Project weeks until $10,000/week net at current growth rate."""
    if current_weekly_net <= 0:
        return {"error": "Current weekly net must be positive to project growth."}
    target = 10000
    if current_weekly_net >= target:
        return {"weeks_to_target": 0, "message": "Already at target!"}

    week = 0
    revenue = current_weekly_net
    while revenue < target and week < 200:
        revenue *= (1 + weekly_growth_rate)
        week += 1

    return {
        "current_weekly_net": round(current_weekly_net, 2),
        "weekly_growth_rate_pct": weekly_growth_rate * 100,
        "weeks_to_10k": week,
        "projected_date": (datetime.now() + timedelta(weeks=week)).strftime("%Y-%m-%d"),
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_add_product(_args):
    print("\n=== Add Affiliate Product ===")
    product_id = input("Product ID (short slug, e.g. jasper-ai): ").strip()
    name = input("Product name: ").strip()
    print("Networks: " + ", ".join(f"{i+1}. {n}" for i, n in enumerate(NETWORKS)))
    net_idx = int(input("Network number: ").strip()) - 1
    network = NETWORKS[net_idx] if 0 <= net_idx < len(NETWORKS) else "Direct"
    commission = float(input("Commission per sale ($): ").strip())
    avg_order_value = float(input("Avg order value ($ or 0 if unknown): ").strip() or 0)
    affiliate_url = input("Affiliate URL: ").strip()
    niche = input("Niche: ").strip()

    product = add_product(product_id, name, network, commission, affiliate_url, niche, avg_order_value)
    print(f"\n✓ Product registered: {product['id']} — {product['name']} ({product['network']})")
    print(f"  Commission: ${product['commission_usd']}")


def cmd_log_click(_args):
    print("\n=== Log Click ===")
    product_id = input("Product ID: ").strip()
    source_video_id = input("Source video ID (optional): ").strip()
    click = record_click(product_id, source_video_id)
    print(f"✓ Click recorded: {click['id']}")


def cmd_log_sale(_args):
    print("\n=== Log Sale ===")
    product_id = input("Product ID: ").strip()
    commission = float(input("Commission earned ($): ").strip())
    order_value = float(input("Order value ($, or 0 if unknown): ").strip() or 0)
    source_video = input("Source video ID (optional): ").strip()
    txn_id = input("Network transaction ID (optional): ").strip()
    sale = record_sale(product_id, commission, order_value, source_video, txn_id)
    print(f"✓ Sale recorded: {sale['id']} — ${commission:.2f} commission")


def cmd_report(_args):
    weeks_back = int(input("Weeks back (0 = current week): ").strip() or 0)
    ad_spend = float(input("Ad spend this week ($, or 0): ").strip() or 0)
    pnl = weekly_pnl(weeks_back, ad_spend)

    print(f"\n{'='*60}")
    print(f"WEEKLY P&L REPORT — Week of {pnl['week_of']}")
    print(f"{'='*60}")
    print(f"Total Sales:            {pnl['total_sales']}")
    print(f"Gross Revenue:          ${pnl['gross_revenue_usd']:,.2f}")
    print(f"Ad Spend:               ${pnl['ad_spend_usd']:,.2f}")
    print(f"Overhead:               ${pnl['overhead_usd']:,.2f}")
    print(f"NET PROFIT:             ${pnl['net_profit_usd']:,.2f}  ({pnl['profit_margin_pct']}% margin)")
    print(f"\nTop Product:            {pnl['top_product_id']} (${pnl['top_product_revenue']:,.2f})")

    print(f"\n--- Revenue by Network ---")
    for network, rev in pnl["by_network"].items():
        print(f"  {network:<25} ${rev:,.2f}")

    print(f"\n--- Revenue by Product ---")
    for pid, rev in pnl["by_product"].items():
        print(f"  {pid:<25} ${rev:,.2f}")

    current_net = pnl["net_profit_usd"]
    if current_net > 0:
        proj = projection_to_10k(current_net)
        if "weeks_to_10k" in proj:
            print(f"\n--- $10K/Week Projection ---")
            print(f"  At 20% weekly growth: {proj['weeks_to_10k']} weeks ({proj['projected_date']})")


def cmd_health(_args):
    alerts = health_check()
    if not alerts:
        print("\n✓ All active products are performing above CVR threshold.")
        return
    print(f"\n{'='*60}")
    print(f"HEALTH ALERTS — {len(alerts)} product(s) need attention")
    print(f"{'='*60}")
    for a in alerts:
        print(f"\n[ALERT] {a['name']} ({a['network']})")
        print(f"  Clicks: {a['clicks']}  |  CVR: {a['cvr_pct']}%")
        print(f"  Issue: {a['alert']}")
        print(f"  Action: {a['recommendation']}")


def cmd_dashboard(_args):
    """Full dashboard: all active products with stats."""
    products = load_products()
    if not products:
        print("No products registered. Use `add-product` to start.")
        return

    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    print(f"\n{'='*90}")
    print(f"AFFILIATE DASHBOARD — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*90}")
    print(f"{'Product':<20} {'Network':<18} {'Clicks':<8} {'Sales':<7} {'CVR%':<8} {'EPC':<8} {'Revenue':<12} {'Alert'}")
    print(f"{'-'*90}")

    total_clicks = total_sales = total_revenue = 0
    for pid, product in products.items():
        if product.get("status") != "active":
            continue
        stats = compute_product_stats(pid)
        alert_flag = "⚠ LOW CVR" if stats["cvr_alert"] else ""
        print(
            f"{product['name'][:19]:<20} {product['network'][:17]:<18} "
            f"{stats['total_clicks']:<8} {stats['total_sales']:<7} "
            f"{stats['cvr_pct']:<8} ${stats['epc_usd']:<7} "
            f"${stats['total_commission_usd']:<11,.2f} {alert_flag}"
        )
        total_clicks += stats["total_clicks"]
        total_sales += stats["total_sales"]
        total_revenue += stats["total_commission_usd"]

    print(f"{'-'*90}")
    overall_cvr = round(total_sales / total_clicks * 100, 3) if total_clicks > 0 else 0
    overall_epc = round(total_revenue / total_clicks, 4) if total_clicks > 0 else 0
    print(f"{'TOTALS':<20} {'':<18} {total_clicks:<8} {total_sales:<7} {overall_cvr:<8} ${overall_epc:<7} ${total_revenue:,.2f}")


def main():
    ensure_data_dir()

    parser = argparse.ArgumentParser(description="Affiliate Link & Revenue Tracker")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("add-product", help="Register a new affiliate product")
    subparsers.add_parser("log-click", help="Record a click event")
    subparsers.add_parser("log-sale", help="Record a confirmed sale")
    subparsers.add_parser("report", help="Weekly P&L report")
    subparsers.add_parser("health", help="Check for underperforming products")
    subparsers.add_parser("dashboard", help="Full affiliate dashboard")

    args = parser.parse_args()
    commands = {
        "add-product": cmd_add_product,
        "log-click": cmd_log_click,
        "log-sale": cmd_log_sale,
        "report": cmd_report,
        "health": cmd_health,
        "dashboard": cmd_dashboard,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
