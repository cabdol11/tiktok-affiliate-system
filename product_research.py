#!/usr/bin/env python3
"""
product_research.py
-------------------
Researches and scores affiliate products by:
  - Commission rate
  - Conversion potential (based on price point & category benchmarks)
  - Trend velocity (manually entered or fetched via public signals)
  - Competition level

Tracks competitor creators and outputs weekly Top 10 product recommendations.

Note: TikTok does not provide a public API for trending products.
This tool uses manual data entry + category-level benchmarks from
TikTok Creative Center public data. For automated scraping, use
a headless browser (Playwright) with TikTok Creative Center at
ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en

Usage:
    python product_research.py add          # Add a product to research
    python product_research.py score        # Score and rank all products
    python product_research.py top10        # Show this week's top 10
    python product_research.py competitor   # Track a competitor creator
    python product_research.py trends       # Show category trend data
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
RESEARCH_FILE = DATA_DIR / "product_research.json"
COMPETITORS_FILE = DATA_DIR / "competitors.json"

# Commission rate benchmarks by network (used to normalize scoring)
COMMISSION_BENCHMARKS = {
    "TikTok Shop": {"excellent": 20, "good": 12, "average": 7},
    "ClickBank": {"excellent": 60, "good": 40, "average": 25},
    "ShareASale": {"excellent": 25, "good": 15, "average": 8},
    "Amazon Associates": {"excellent": 10, "good": 6, "average": 3},
    "Impact": {"excellent": 30, "good": 15, "average": 8},
    "CJ Affiliate": {"excellent": 15, "good": 8, "average": 4},
    "Direct": {"excellent": 40, "good": 20, "average": 10},
}

# Category-level CVR benchmarks on TikTok (based on public industry data)
CATEGORY_CVR_BENCHMARKS = {
    "beauty_skincare": 0.038,
    "fitness_supplements": 0.029,
    "ai_tools": 0.045,
    "home_gadgets": 0.031,
    "pet_products": 0.027,
    "fashion": 0.022,
    "electronics": 0.018,
    "food_beverage": 0.033,
    "baby_kids": 0.030,
    "other": 0.025,
}

CATEGORIES = list(CATEGORY_CVR_BENCHMARKS.keys())

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


def load_research():
    return load_json(RESEARCH_FILE, {})


def save_research(data):
    save_json(RESEARCH_FILE, data)


def load_competitors():
    return load_json(COMPETITORS_FILE, {})


def save_competitors(data):
    save_json(COMPETITORS_FILE, data)

# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def score_commission(commission_pct: float, network: str) -> float:
    """Score 0-10 based on commission rate relative to network benchmarks."""
    bench = COMMISSION_BENCHMARKS.get(network, COMMISSION_BENCHMARKS["Direct"])
    if commission_pct >= bench["excellent"]:
        return 10.0
    elif commission_pct >= bench["good"]:
        return 7.0 + 3.0 * (commission_pct - bench["good"]) / (bench["excellent"] - bench["good"])
    elif commission_pct >= bench["average"]:
        return 4.0 + 3.0 * (commission_pct - bench["average"]) / (bench["good"] - bench["average"])
    else:
        return max(1.0, 4.0 * commission_pct / bench["average"])


def score_conversion_potential(category: str, price_usd: float) -> float:
    """
    Score 0-10 based on category CVR benchmark + price point.
    Sweet spot: $30-$100 for TikTok audiences.
    """
    base_cvr = CATEGORY_CVR_BENCHMARKS.get(category, 0.025)
    cvr_score = min(10.0, base_cvr / 0.05 * 10)  # normalize to 0-10

    # Price penalty: very cheap (<$15) or very expensive (>$300) converts worse
    if price_usd < 15:
        price_multiplier = 0.7
    elif price_usd <= 30:
        price_multiplier = 0.85
    elif price_usd <= 100:
        price_multiplier = 1.0   # sweet spot
    elif price_usd <= 200:
        price_multiplier = 0.90
    elif price_usd <= 500:
        price_multiplier = 0.80
    else:
        price_multiplier = 0.70  # high ticket needs trust-building

    return round(cvr_score * price_multiplier, 2)


def score_trend_velocity(trend_score: int) -> float:
    """
    trend_score: 1-10 manually entered (based on TikTok Creative Center, Google Trends).
    1 = declining, 5 = stable, 10 = viral/exploding
    """
    return float(min(10, max(1, trend_score)))


def score_competition(competition_level: str) -> float:
    """
    competition_level: 'low', 'medium', 'high', 'saturated'
    Lower competition = higher score (easier to rank)
    """
    mapping = {
        "low": 10.0,
        "medium": 7.0,
        "high": 4.0,
        "saturated": 2.0,
    }
    return mapping.get(competition_level.lower(), 5.0)


def compute_composite_score(product: dict) -> float:
    """
    Weighted composite score (0-10):
      - Commission:           30%
      - Conversion potential: 25%
      - Trend velocity:       25%
      - Competition:          20%
    """
    s_commission = score_commission(
        product.get("commission_pct", 0),
        product.get("network", "Direct")
    )
    s_conversion = score_conversion_potential(
        product.get("category", "other"),
        product.get("price_usd", 50)
    )
    s_trend = score_trend_velocity(product.get("trend_score", 5))
    s_competition = score_competition(product.get("competition_level", "medium"))

    composite = (
        s_commission * 0.30 +
        s_conversion * 0.25 +
        s_trend * 0.25 +
        s_competition * 0.20
    )

    return round(composite, 2)


def estimated_weekly_epc(product: dict) -> float:
    """Estimate EPC based on commission, CVR, and price."""
    commission_usd = product.get("price_usd", 50) * product.get("commission_pct", 10) / 100
    cvr = CATEGORY_CVR_BENCHMARKS.get(product.get("category", "other"), 0.025)
    return round(commission_usd * cvr, 4)

# ---------------------------------------------------------------------------
# Product operations
# ---------------------------------------------------------------------------

def add_product(product: dict) -> dict:
    """Add a product to the research database and score it."""
    research = load_research()
    pid = product["id"]
    if pid in research:
        raise ValueError(f"Product {pid} already exists. Use update to modify.")

    product["composite_score"] = compute_composite_score(product)
    product["estimated_epc"] = estimated_weekly_epc(product)
    product["added_at"] = datetime.now().isoformat()
    product["status"] = "researching"

    research[pid] = product
    save_research(research)
    return product


def update_product(product_id: str, updates: dict) -> dict:
    """Update a product's data and recompute score."""
    research = load_research()
    if product_id not in research:
        raise ValueError(f"Product {product_id} not found.")
    research[product_id].update(updates)
    research[product_id]["composite_score"] = compute_composite_score(research[product_id])
    research[product_id]["estimated_epc"] = estimated_weekly_epc(research[product_id])
    research[product_id]["updated_at"] = datetime.now().isoformat()
    save_research(research)
    return research[product_id]


def get_top_10(this_week_only: bool = False) -> list:
    """Return top 10 products by composite score."""
    research = load_research()
    products = list(research.values())

    if this_week_only:
        cutoff = datetime.now() - timedelta(days=7)
        products = [
            p for p in products
            if datetime.fromisoformat(p["added_at"]) >= cutoff
        ]

    products.sort(key=lambda p: p.get("composite_score", 0), reverse=True)
    return products[:10]


def add_competitor(handle: str, niche: str, estimated_followers: int,
                   notes: str = "") -> dict:
    """Track a competitor TikTok creator."""
    competitors = load_competitors()
    competitor = {
        "handle": handle,
        "niche": niche,
        "estimated_followers": estimated_followers,
        "notes": notes,
        "products_observed": [],
        "added_at": datetime.now().isoformat(),
        "last_checked": datetime.now().isoformat(),
    }
    competitors[handle] = competitor
    save_competitors(competitors)
    return competitor


def log_competitor_product(handle: str, product_name: str, video_url: str,
                            estimated_views: int) -> None:
    """Log a product observed being promoted by a competitor."""
    competitors = load_competitors()
    if handle not in competitors:
        raise ValueError(f"Competitor {handle} not tracked. Add them first.")
    entry = {
        "product": product_name,
        "video_url": video_url,
        "estimated_views": estimated_views,
        "observed_at": datetime.now().isoformat(),
    }
    competitors[handle]["products_observed"].append(entry)
    competitors[handle]["last_checked"] = datetime.now().isoformat()
    save_competitors(competitors)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_add(_args):
    print("\n=== Add Product to Research Database ===")
    product_id = input("Product ID (slug): ").strip()
    name = input("Product name: ").strip()
    price = float(input("Price to consumer ($): ").strip())
    commission_pct = float(input("Commission rate (%): ").strip())
    network = input("Network (TikTok Shop / ClickBank / ShareASale / etc.): ").strip()

    print("Categories: " + ", ".join(CATEGORIES))
    category = input("Category: ").strip()

    trend_score = int(input("Trend score 1-10 (check TikTok Creative Center, Google Trends): ").strip())
    competition = input("Competition level (low / medium / high / saturated): ").strip()
    affiliate_url = input("Affiliate URL: ").strip()
    notes = input("Notes (optional): ").strip()

    product = {
        "id": product_id,
        "name": name,
        "price_usd": price,
        "commission_pct": commission_pct,
        "network": network,
        "category": category,
        "trend_score": trend_score,
        "competition_level": competition,
        "affiliate_url": affiliate_url,
        "notes": notes,
    }

    result = add_product(product)
    print(f"\n✓ Product added: {result['name']}")
    print(f"  Composite Score:    {result['composite_score']}/10")
    print(f"  Estimated EPC:      ${result['estimated_epc']}")
    print(f"  Commission/Sale:    ${price * commission_pct / 100:.2f}")


def cmd_score(_args):
    """Recompute scores for all products (useful after updating benchmarks)."""
    research = load_research()
    for pid, product in research.items():
        research[pid]["composite_score"] = compute_composite_score(product)
        research[pid]["estimated_epc"] = estimated_weekly_epc(product)
    save_research(research)
    print(f"✓ Rescored {len(research)} products.")
    cmd_top10(_args)


def cmd_top10(_args):
    """Display the top 10 products to promote this week."""
    top = get_top_10()
    if not top:
        print("No products in database. Use `add` to add products.")
        return

    print(f"\n{'='*90}")
    print(f"TOP 10 PRODUCTS TO PROMOTE — {datetime.now().strftime('%Y-W%W')}")
    print(f"{'='*90}")
    print(f"{'#':<3} {'Product':<22} {'Network':<16} {'Price':<8} {'Comm%':<7} {'Trend':<7} {'Comp':<10} {'Score':<7} {'EPC'}")
    print(f"{'-'*90}")
    for i, p in enumerate(top, 1):
        commission_usd = p.get("price_usd", 0) * p.get("commission_pct", 0) / 100
        print(
            f"{i:<3} {p['name'][:21]:<22} {p.get('network','')[:15]:<16} "
            f"${p.get('price_usd',0):<7.0f} {p.get('commission_pct',0):<7.0f} "
            f"{p.get('trend_score',0):<7} {p.get('competition_level','')[:9]:<10} "
            f"{p.get('composite_score',0):<7} ${p.get('estimated_epc',0):.4f}"
        )
    print(f"\nTop pick: {top[0]['name']} — Score {top[0]['composite_score']}/10")
    if top[0].get("notes"):
        print(f"  Notes: {top[0]['notes']}")


def cmd_competitor(_args):
    print("\n1. Add competitor  2. Log competitor product  3. View competitors")
    choice = input("Choice: ").strip()
    if choice == "1":
        handle = input("TikTok handle (@username): ").strip()
        niche = input("Niche: ").strip()
        followers = int(input("Estimated followers: ").strip() or 0)
        notes = input("Notes: ").strip()
        c = add_competitor(handle, niche, followers, notes)
        print(f"✓ Tracking @{c['handle']}")
    elif choice == "2":
        handle = input("Competitor handle: ").strip()
        product = input("Product name they're promoting: ").strip()
        url = input("Video URL: ").strip()
        views = int(input("Estimated views: ").strip() or 0)
        log_competitor_product(handle, product, url, views)
        print("✓ Logged.")
    elif choice == "3":
        competitors = load_competitors()
        if not competitors:
            print("No competitors tracked.")
            return
        for handle, c in competitors.items():
            print(f"\n@{handle} | {c['niche']} | {c['estimated_followers']:,} followers")
            for obs in c["products_observed"][-3:]:
                print(f"  → {obs['product']} ({obs['estimated_views']:,} views) — {obs['observed_at'][:10]}")


def cmd_trends(_args):
    """Show category CVR benchmarks and trend guidance."""
    print(f"\n{'='*60}")
    print("CATEGORY CVR BENCHMARKS (TikTok, industry estimates)")
    print(f"{'='*60}")
    print(f"{'Category':<25} {'Est. CVR':<12} {'Score/10'}")
    print(f"{'-'*60}")
    for cat, cvr in sorted(CATEGORY_CVR_BENCHMARKS.items(), key=lambda x: -x[1]):
        score = min(10.0, cvr / 0.05 * 10)
        print(f"{cat:<25} {cvr*100:.1f}%        {score:.1f}")
    print(f"\nTrend data sources:")
    print("  - TikTok Creative Center: ads.tiktok.com/business/creativecenter")
    print("  - Google Trends: trends.google.com (search your niche keywords)")
    print("  - TikTok hashtag views: search hashtag in TikTok app")
    print("  - Amazon Best Sellers: amazon.com/best-sellers")
    print("  - Exploding Topics: explodingtopics.com")


def main():
    ensure_data_dir()
    parser = argparse.ArgumentParser(description="Affiliate Product Research & Scoring")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("add", help="Add a product to research")
    subparsers.add_parser("score", help="Rescore all products")
    subparsers.add_parser("top10", help="Show top 10 products this week")
    subparsers.add_parser("competitor", help="Track competitor creators")
    subparsers.add_parser("trends", help="Show category trend benchmarks")

    args = parser.parse_args()
    commands = {
        "add": cmd_add,
        "score": cmd_score,
        "top10": cmd_top10,
        "competitor": cmd_competitor,
        "trends": cmd_trends,
    }
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
