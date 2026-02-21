#!/usr/bin/env python3
"""
financials.py
-------------
Tracks gross revenue, ad spend, tool costs, and net profit by week.
Projects when you'll hit $10K/week.
Calculates break-even on paid ad campaigns.
Generates a comprehensive weekly financial dashboard.

Usage:
    python financials.py log-week      # Log a week's financials
    python financials.py dashboard     # Full weekly dashboard
    python financials.py project       # $10K/week projection
    python financials.py breakeven     # Ad campaign break-even calculator
    python financials.py history       # Historical weekly performance
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
FINANCIALS_FILE = DATA_DIR / "financials.json"

# Fixed monthly tool costs (update as you add/remove tools)
TOOL_COSTS_MONTHLY = {
    "CapCut Pro": 7.99,
    "Canva Pro": 12.99,
    "ConvertKit (Creator)": 29.00,
    "Beacons.ai Pro": 10.00,
    "VidIQ Pro": 16.58,
    "Notion": 0.00,
    "RedTrack (scale phase)": 0.00,   # add $149/mo when you hit week 9+
    "Voluum (optional)": 0.00,
}

WEEKLY_TOOL_COST = sum(TOOL_COSTS_MONTHLY.values()) / 4.33

# Milestones to track progress against
MILESTONES = [
    {"week": 2,  "target_net": 475,    "label": "First Sale"},
    {"week": 4,  "target_net": 2425,   "label": "$2,500/week"},
    {"week": 8,  "target_net": 4925,   "label": "$5K/week"},
    {"week": 12, "target_net": 7675,   "label": "$7,500/week"},
    {"week": 20, "target_net": 10000,  "label": "$10K/week NET"},
]

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_financials():
    if not FINANCIALS_FILE.exists():
        return {"weeks": [], "start_date": datetime.now().isoformat()}
    with open(FINANCIALS_FILE) as f:
        return json.load(f)


def save_financials(data):
    with open(FINANCIALS_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

# ---------------------------------------------------------------------------
# Core calculations
# ---------------------------------------------------------------------------

def log_week(
    week_number: int,
    gross_revenue: float,
    ad_spend: float,
    total_clicks: int,
    total_conversions: int,
    avg_order_value: float,
    top_video_id: str,
    top_video_views: int,
    top_product: str,
    notes: str = "",
    extra_costs: float = 0.0,
) -> dict:
    """Log a week's financial performance."""
    financials = load_financials()

    net_profit = gross_revenue - ad_spend - WEEKLY_TOOL_COST - extra_costs
    avg_commission = gross_revenue / total_conversions if total_conversions > 0 else 0
    roas = gross_revenue / ad_spend if ad_spend > 0 else None
    cvr_pct = total_conversions / total_clicks * 100 if total_clicks > 0 else 0
    epc = gross_revenue / total_clicks if total_clicks > 0 else 0

    week_entry = {
        "week_number": week_number,
        "date_logged": datetime.now().isoformat(),
        "gross_revenue_usd": round(gross_revenue, 2),
        "ad_spend_usd": round(ad_spend, 2),
        "tool_cost_usd": round(WEEKLY_TOOL_COST, 2),
        "extra_costs_usd": round(extra_costs, 2),
        "total_costs_usd": round(ad_spend + WEEKLY_TOOL_COST + extra_costs, 2),
        "net_profit_usd": round(net_profit, 2),
        "profit_margin_pct": round(net_profit / gross_revenue * 100, 1) if gross_revenue > 0 else 0,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "cvr_pct": round(cvr_pct, 3),
        "avg_order_value_usd": round(avg_order_value, 2),
        "avg_commission_usd": round(avg_commission, 2),
        "epc_usd": round(epc, 4),
        "roas": round(roas, 2) if roas is not None else "N/A (organic)",
        "top_video_id": top_video_id,
        "top_video_views": top_video_views,
        "top_product": top_product,
        "notes": notes,
    }

    # Remove existing entry for this week if re-logging
    financials["weeks"] = [w for w in financials["weeks"] if w["week_number"] != week_number]
    financials["weeks"].append(week_entry)
    financials["weeks"].sort(key=lambda w: w["week_number"])
    save_financials(financials)
    return week_entry


def project_to_10k(current_weekly_net: float, growth_rate: float = 0.20) -> dict:
    """Project weeks to $10K/week at a given weekly growth rate."""
    if current_weekly_net <= 0:
        return {"error": "Log at least one week with positive net profit first."}

    target = 10_000
    if current_weekly_net >= target:
        return {"message": "Already at $10K/week!", "weeks_remaining": 0}

    revenue = current_weekly_net
    week = 0
    trajectory = []
    while revenue < target and week < 200:
        week += 1
        revenue *= (1 + growth_rate)
        if week % 4 == 0 or revenue >= target:
            trajectory.append({
                "week": week,
                "projected_net": round(revenue, 2),
                "projected_date": (datetime.now() + timedelta(weeks=week)).strftime("%Y-%m-%d"),
            })

    return {
        "current_weekly_net": round(current_weekly_net, 2),
        "growth_rate_pct": growth_rate * 100,
        "weeks_to_10k": week,
        "projected_date": (datetime.now() + timedelta(weeks=week)).strftime("%Y-%m-%d"),
        "trajectory": trajectory,
    }


def break_even_calculator(
    ad_spend_daily: float,
    avg_commission: float,
    cvr: float = 0.025,
    cpc: float = 0.50,
) -> dict:
    """
    Calculate break-even point for a paid ad campaign.

    Args:
        ad_spend_daily:  Daily budget ($)
        avg_commission:  Average commission per sale ($)
        cvr:             Expected conversion rate (e.g., 0.025 = 2.5%)
        cpc:             Cost per click ($)

    Returns:
        Break-even analysis dict
    """
    daily_clicks = ad_spend_daily / cpc if cpc > 0 else 0
    daily_conversions = daily_clicks * cvr
    daily_revenue = daily_conversions * avg_commission
    daily_profit = daily_revenue - ad_spend_daily
    roas = daily_revenue / ad_spend_daily if ad_spend_daily > 0 else 0

    # Break-even CPC: the max you can pay per click and still profit
    breakeven_cpc = avg_commission * cvr  # max CPC = commission × CVR

    # Required ROAS to profit
    required_roas = 1.0 + (ad_spend_daily / daily_revenue) if daily_revenue > 0 else float("inf")

    return {
        "daily_ad_spend": round(ad_spend_daily, 2),
        "cost_per_click": round(cpc, 4),
        "daily_clicks": round(daily_clicks, 1),
        "daily_conversions": round(daily_conversions, 2),
        "daily_gross_revenue": round(daily_revenue, 2),
        "daily_net_profit": round(daily_profit, 2),
        "roas": round(roas, 2),
        "breakeven_cpc_max": round(breakeven_cpc, 4),
        "weekly_profit_projection": round(daily_profit * 7, 2),
        "monthly_profit_projection": round(daily_profit * 30.4, 2),
        "is_profitable": daily_profit > 0,
        "note": f"You break even at CPC = ${breakeven_cpc:.4f}. Keep CPC below this.",
    }


def weekly_dashboard(week_number: int = None) -> dict:
    """Return dashboard data for a specific week (or most recent)."""
    financials = load_financials()
    weeks = financials.get("weeks", [])

    if not weeks:
        return {"error": "No weeks logged. Use `log-week` first."}

    if week_number:
        week = next((w for w in weeks if w["week_number"] == week_number), None)
        if not week:
            return {"error": f"Week {week_number} not found."}
    else:
        week = weeks[-1]

    # Week-over-week change
    prev_week = next((w for w in weeks if w["week_number"] == week["week_number"] - 1), None)
    wow_net = None
    if prev_week:
        prev = prev_week["net_profit_usd"]
        curr = week["net_profit_usd"]
        wow_net = round((curr - prev) / abs(prev) * 100, 1) if prev != 0 else None

    # Milestone progress
    next_milestone = None
    for m in MILESTONES:
        if week["net_profit_usd"] < m["target_net"]:
            gap = m["target_net"] - week["net_profit_usd"]
            next_milestone = {**m, "gap_usd": round(gap, 2)}
            break

    # All-time totals
    all_time_gross = sum(w["gross_revenue_usd"] for w in weeks)
    all_time_net = sum(w["net_profit_usd"] for w in weeks)

    return {
        "week_number": week["week_number"],
        "date_logged": week["date_logged"][:10],
        "gross_revenue": week["gross_revenue_usd"],
        "ad_spend": week["ad_spend_usd"],
        "tool_cost": week["tool_cost_usd"],
        "net_profit": week["net_profit_usd"],
        "profit_margin_pct": week["profit_margin_pct"],
        "total_clicks": week["total_clicks"],
        "total_conversions": week["total_conversions"],
        "cvr_pct": week["cvr_pct"],
        "avg_commission": week["avg_commission_usd"],
        "epc": week["epc_usd"],
        "roas": week["roas"],
        "top_video": week["top_video_id"],
        "top_video_views": week["top_video_views"],
        "top_product": week["top_product"],
        "wow_growth_pct": wow_net,
        "next_milestone": next_milestone,
        "all_time_gross": round(all_time_gross, 2),
        "all_time_net": round(all_time_net, 2),
        "weeks_logged": len(weeks),
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_log_week(_args):
    print("\n=== Log Weekly Financials ===")
    week_number = int(input("Week number (1, 2, 3...): ").strip())
    gross = float(input("Gross revenue (total commissions earned) $: ").strip() or 0)
    ad_spend = float(input("Ad spend this week $: ").strip() or 0)
    clicks = int(input("Total link clicks: ").strip() or 0)
    conversions = int(input("Total conversions (sales): ").strip() or 0)
    aov = float(input("Avg order value $: ").strip() or 0)
    top_video = input("Top performing video ID: ").strip()
    top_video_views = int(input("Top video views: ").strip() or 0)
    top_product = input("Top product this week: ").strip()
    extra_costs = float(input("Extra costs (freelancer, equipment, etc.) $: ").strip() or 0)
    notes = input("Notes: ").strip()

    entry = log_week(
        week_number, gross, ad_spend, clicks, conversions,
        aov, top_video, top_video_views, top_product, notes, extra_costs
    )

    print(f"\n{'='*50}")
    print(f"WEEK {week_number} LOGGED")
    print(f"{'='*50}")
    print(f"Gross Revenue:   ${entry['gross_revenue_usd']:,.2f}")
    print(f"Ad Spend:        ${entry['ad_spend_usd']:,.2f}")
    print(f"Tools:           ${entry['tool_cost_usd']:,.2f}")
    print(f"NET PROFIT:      ${entry['net_profit_usd']:,.2f}  ({entry['profit_margin_pct']}% margin)")
    print(f"CVR:             {entry['cvr_pct']}%")
    print(f"ROAS:            {entry['roas']}")


def cmd_dashboard(_args):
    week_number = input("Week number (leave blank for latest): ").strip()
    dash = weekly_dashboard(int(week_number) if week_number else None)

    if "error" in dash:
        print(f"\n{dash['error']}")
        return

    print(f"\n{'='*60}")
    print(f"WEEKLY FINANCIAL DASHBOARD — Week {dash['week_number']} ({dash['date_logged']})")
    print(f"{'='*60}")
    print(f"Gross Revenue:          ${dash['gross_revenue']:>10,.2f}")
    print(f"Ad Spend:               ${dash['ad_spend']:>10,.2f}")
    print(f"Tool Costs:             ${dash['tool_cost']:>10,.2f}")
    print(f"NET PROFIT:             ${dash['net_profit']:>10,.2f}  ({dash['profit_margin_pct']}% margin)")

    if dash["wow_growth_pct"] is not None:
        direction = "+" if dash["wow_growth_pct"] >= 0 else ""
        print(f"Week-over-Week:         {direction}{dash['wow_growth_pct']}%")

    print(f"\n--- Traffic & Conversion ---")
    print(f"Total Clicks:           {dash['total_clicks']:,}")
    print(f"Total Conversions:      {dash['total_conversions']:,}")
    print(f"CVR:                    {dash['cvr_pct']}%")
    print(f"Avg Commission:         ${dash['avg_commission']}")
    print(f"EPC:                    ${dash['epc']}")
    print(f"ROAS:                   {dash['roas']}")

    print(f"\n--- Top Performers ---")
    print(f"Top Video:              {dash['top_video']} ({dash['top_video_views']:,} views)")
    print(f"Top Product:            {dash['top_product']}")

    if dash["next_milestone"]:
        m = dash["next_milestone"]
        print(f"\n--- Next Milestone ---")
        print(f"Target:                 {m['label']} (Week {m['week']})")
        print(f"Gap:                    ${m['gap_usd']:,.2f}")

    print(f"\n--- All-Time ---")
    print(f"Weeks Logged:           {dash['weeks_logged']}")
    print(f"All-Time Gross:         ${dash['all_time_gross']:,.2f}")
    print(f"All-Time Net:           ${dash['all_time_net']:,.2f}")


def cmd_project(_args):
    financials = load_financials()
    weeks = financials.get("weeks", [])
    if not weeks:
        print("No weeks logged yet. Log a week first with `log-week`.")
        return

    current_net = weeks[-1]["net_profit_usd"]
    growth_input = input(f"Weekly growth rate % (default 20%): ").strip()
    growth_rate = float(growth_input) / 100 if growth_input else 0.20

    proj = project_to_10k(current_net, growth_rate)

    if "error" in proj:
        print(f"\n{proj['error']}")
        return

    print(f"\n{'='*60}")
    print(f"$10K/WEEK PROJECTION")
    print(f"{'='*60}")
    print(f"Current Weekly Net:     ${proj['current_weekly_net']:,.2f}")
    print(f"Growth Rate:            {proj['growth_rate_pct']}%/week")
    print(f"Weeks to $10K/week:     {proj['weeks_to_10k']}")
    print(f"Projected Date:         {proj['projected_date']}")
    print(f"\n{'Week':<8} {'Projected Net':<20} {'Date'}")
    print(f"{'-'*45}")
    for t in proj.get("trajectory", []):
        marker = " <-- $10K!" if t["projected_net"] >= 10000 else ""
        print(f"{t['week']:<8} ${t['projected_net']:<19,.2f} {t['projected_date']}{marker}")


def cmd_breakeven(_args):
    print("\n=== Ad Campaign Break-Even Calculator ===")
    daily_budget = float(input("Daily ad budget ($): ").strip())
    avg_commission = float(input("Avg commission per sale ($): ").strip())
    cvr = float(input("Expected CVR % (e.g., 2.5 for 2.5%): ").strip()) / 100
    cpc = float(input("Expected cost per click ($, e.g., 0.50): ").strip())

    result = break_even_calculator(daily_budget, avg_commission, cvr, cpc)

    print(f"\n{'='*55}")
    print(f"BREAK-EVEN ANALYSIS")
    print(f"{'='*55}")
    print(f"Daily Ad Spend:         ${result['daily_ad_spend']}")
    print(f"Cost Per Click:         ${result['cost_per_click']}")
    print(f"Daily Clicks:           {result['daily_clicks']}")
    print(f"Daily Conversions:      {result['daily_conversions']}")
    print(f"Daily Revenue:          ${result['daily_gross_revenue']}")
    print(f"Daily Net Profit:       ${result['daily_net_profit']}")
    print(f"ROAS:                   {result['roas']}x")
    print(f"\nWeekly Profit:          ${result['weekly_profit_projection']:,.2f}")
    print(f"Monthly Profit:         ${result['monthly_profit_projection']:,.2f}")
    print(f"\nMax Profitable CPC:     ${result['breakeven_cpc_max']}")
    print(f"Profitable:             {'YES' if result['is_profitable'] else 'NO — reduce CPC or increase CVR'}")
    print(f"\n{result['note']}")


def cmd_history(_args):
    financials = load_financials()
    weeks = financials.get("weeks", [])
    if not weeks:
        print("No weeks logged.")
        return
    print(f"\n{'='*90}")
    print(f"HISTORICAL PERFORMANCE")
    print(f"{'='*90}")
    print(f"{'Wk':<4} {'Gross':<12} {'AdSpend':<10} {'Tools':<8} {'Net':<12} {'Margin':<8} {'Sales':<7} {'CVR%':<7} {'ROAS'}")
    print(f"{'-'*90}")
    for w in weeks:
        roas = str(w.get("roas", "N/A"))
        print(
            f"{w['week_number']:<4} ${w['gross_revenue_usd']:<11,.2f} "
            f"${w['ad_spend_usd']:<9,.2f} ${w['tool_cost_usd']:<7,.2f} "
            f"${w['net_profit_usd']:<11,.2f} {w['profit_margin_pct']:<8} "
            f"{w['total_conversions']:<7} {w['cvr_pct']:<7} {roas}"
        )
    total_net = sum(w["net_profit_usd"] for w in weeks)
    total_gross = sum(w["gross_revenue_usd"] for w in weeks)
    print(f"{'-'*90}")
    print(f"{'TOTAL':<4} ${total_gross:<11,.2f} {'':10} {'':8} ${total_net:<11,.2f}")


def main():
    ensure_data_dir()
    parser = argparse.ArgumentParser(description="Affiliate Business Financial Tracker")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("log-week", help="Log a week's financials")
    subparsers.add_parser("dashboard", help="Weekly financial dashboard")
    subparsers.add_parser("project", help="Project path to $10K/week")
    subparsers.add_parser("breakeven", help="Ad campaign break-even calculator")
    subparsers.add_parser("history", help="View all historical weeks")

    args = parser.parse_args()
    commands = {
        "log-week": cmd_log_week,
        "dashboard": cmd_dashboard,
        "project": cmd_project,
        "breakeven": cmd_breakeven,
        "history": cmd_history,
    }
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
