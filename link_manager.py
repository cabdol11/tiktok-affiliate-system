#!/usr/bin/env python3
"""
link_manager.py
---------------
Creates and manages UTM-tracked affiliate links.
Runs A/B tests on landing page variations.
Tracks which video → which link → which sale.
Generates a unified link performance dashboard.

Usage:
    python link_manager.py create      # Create a new tracked link
    python link_manager.py list        # List all links
    python link_manager.py click       # Record a click on a link
    python link_manager.py ab-test     # Create an A/B test between two links
    python link_manager.py dashboard   # Full link performance dashboard
    python link_manager.py top         # Top performing links by EPC
"""

import argparse
import json
import random
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
LINKS_FILE = DATA_DIR / "links.json"
AB_TESTS_FILE = DATA_DIR / "ab_tests.json"
LINK_CLICKS_FILE = DATA_DIR / "link_clicks.json"

# Your Beacons.ai / Linktree base URL — replace with your actual link-in-bio URL
LINK_IN_BIO_BASE = "https://beacons.ai/yourusername"

# UTM source values
UTM_SOURCES = {
    "tiktok": "tiktok",
    "instagram": "instagram",
    "youtube": "youtube",
    "email": "email",
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


def load_links():
    return load_json(LINKS_FILE, {})


def save_links(data):
    save_json(LINKS_FILE, data)


def load_ab_tests():
    return load_json(AB_TESTS_FILE, {})


def save_ab_tests(data):
    save_json(AB_TESTS_FILE, data)


def load_link_clicks():
    return load_json(LINK_CLICKS_FILE, [])


def save_link_clicks(data):
    save_json(LINK_CLICKS_FILE, data)

# ---------------------------------------------------------------------------
# UTM builder
# ---------------------------------------------------------------------------

def build_utm_url(base_url: str, source: str, medium: str,
                   campaign: str, content: str = "", term: str = "") -> str:
    """
    Append UTM parameters to a URL for tracking.

    Args:
        base_url:  The destination affiliate URL
        source:    Traffic source (tiktok, instagram, email)
        medium:    Traffic medium (organic, spark_ad, story)
        campaign:  Campaign name (e.g., video_id or product slug)
        content:   A/B variant or specific CTA identifier
        term:      Optional search term / hook identifier

    Returns:
        Full URL with UTM parameters appended
    """
    params = {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
    }
    if content:
        params["utm_content"] = content
    if term:
        params["utm_term"] = term

    separator = "&" if "?" in base_url else "?"
    return base_url + separator + urllib.parse.urlencode(params)


def generate_link_id() -> str:
    """Generate a short unique link identifier."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "lnk_" + "".join(random.choices(chars, k=8))

# ---------------------------------------------------------------------------
# Link operations
# ---------------------------------------------------------------------------

def create_link(
    destination_url: str,
    product_id: str,
    product_name: str,
    source: str = "tiktok",
    medium: str = "organic",
    campaign: str = "",
    content: str = "",
    video_id: str = "",
    variant: str = "A",
) -> dict:
    """Create a new UTM-tracked affiliate link."""
    links = load_links()
    link_id = generate_link_id()

    if not campaign:
        campaign = product_id

    tracked_url = build_utm_url(
        destination_url,
        source=source,
        medium=medium,
        campaign=campaign,
        content=content or f"variant_{variant}",
        term=video_id,
    )

    link = {
        "id": link_id,
        "product_id": product_id,
        "product_name": product_name,
        "destination_url": destination_url,
        "tracked_url": tracked_url,
        "source": source,
        "medium": medium,
        "campaign": campaign,
        "content": content,
        "variant": variant,
        "video_id": video_id,
        "created_at": datetime.now().isoformat(),
        "status": "active",
        "stats": {
            "clicks": 0,
            "conversions": 0,
            "revenue_usd": 0.0,
            "last_clicked": None,
        },
    }
    links[link_id] = link
    save_links(links)
    return link


def record_link_click(link_id: str, sale_amount: float = 0.0,
                       converted: bool = False) -> dict:
    """Record a click (and optionally a conversion) on a tracked link."""
    links = load_links()
    if link_id not in links:
        raise ValueError(f"Link {link_id} not found.")

    links[link_id]["stats"]["clicks"] += 1
    links[link_id]["stats"]["last_clicked"] = datetime.now().isoformat()

    if converted:
        links[link_id]["stats"]["conversions"] += 1
        links[link_id]["stats"]["revenue_usd"] += sale_amount

    click_log = {
        "link_id": link_id,
        "product_id": links[link_id]["product_id"],
        "video_id": links[link_id]["video_id"],
        "converted": converted,
        "sale_amount": sale_amount,
        "timestamp": datetime.now().isoformat(),
    }
    all_clicks = load_link_clicks()
    all_clicks.append(click_log)
    save_link_clicks(all_clicks)
    save_links(links)
    return click_log


def create_ab_test(
    test_name: str,
    product_id: str,
    url_a: str,
    url_b: str,
    hypothesis: str = "",
) -> dict:
    """Create an A/B test between two destination URLs for the same product."""
    ab_tests = load_ab_tests()
    test_id = f"ab_{int(datetime.now().timestamp())}"

    link_a = create_link(url_a, product_id, test_name, variant="A", content="ab_test_a")
    link_b = create_link(url_b, product_id, test_name, variant="B", content="ab_test_b")

    test = {
        "id": test_id,
        "name": test_name,
        "product_id": product_id,
        "hypothesis": hypothesis,
        "link_a_id": link_a["id"],
        "link_b_id": link_b["id"],
        "url_a": url_a,
        "url_b": url_b,
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "winner": None,
    }
    ab_tests[test_id] = test
    save_ab_tests(ab_tests)
    return test


def get_ab_test_results(test_id: str) -> dict:
    """Compute winner of an A/B test based on CVR."""
    ab_tests = load_ab_tests()
    if test_id not in ab_tests:
        raise ValueError(f"A/B test {test_id} not found.")

    test = ab_tests[test_id]
    links = load_links()

    link_a = links.get(test["link_a_id"], {})
    link_b = links.get(test["link_b_id"], {})

    def stats(link):
        s = link.get("stats", {})
        clicks = s.get("clicks", 0)
        convs = s.get("conversions", 0)
        rev = s.get("revenue_usd", 0.0)
        cvr = convs / clicks if clicks > 0 else 0.0
        epc = rev / clicks if clicks > 0 else 0.0
        return {"clicks": clicks, "conversions": convs, "revenue": rev, "cvr": cvr, "epc": epc}

    stats_a = stats(link_a)
    stats_b = stats(link_b)

    # Determine winner by CVR (minimum 20 clicks each for significance)
    if stats_a["clicks"] >= 20 and stats_b["clicks"] >= 20:
        winner = "A" if stats_a["cvr"] >= stats_b["cvr"] else "B"
        improvement = abs(stats_a["cvr"] - stats_b["cvr"]) / max(stats_a["cvr"], stats_b["cvr"]) * 100
    else:
        winner = "Insufficient data"
        improvement = 0

    return {
        "test_id": test_id,
        "name": test["name"],
        "hypothesis": test["hypothesis"],
        "status": test["status"],
        "variant_a": {"url": test["url_a"], **stats_a},
        "variant_b": {"url": test["url_b"], **stats_b},
        "winner": winner,
        "improvement_pct": round(improvement, 1),
        "min_clicks_reached": stats_a["clicks"] >= 20 and stats_b["clicks"] >= 20,
    }


def link_performance_dashboard() -> list:
    """Return all links sorted by EPC."""
    links = load_links()
    results = []
    for lid, link in links.items():
        s = link.get("stats", {})
        clicks = s.get("clicks", 0)
        convs = s.get("conversions", 0)
        rev = s.get("revenue_usd", 0.0)
        cvr = round(convs / clicks * 100, 2) if clicks > 0 else 0.0
        epc = round(rev / clicks, 4) if clicks > 0 else 0.0
        results.append({
            "id": lid,
            "product": link.get("product_name", ""),
            "source": link.get("source", ""),
            "medium": link.get("medium", ""),
            "variant": link.get("variant", ""),
            "video_id": link.get("video_id", ""),
            "clicks": clicks,
            "conversions": convs,
            "cvr_pct": cvr,
            "revenue_usd": round(rev, 2),
            "epc": epc,
            "status": link.get("status", "active"),
        })
    results.sort(key=lambda x: x["epc"], reverse=True)
    return results


def video_to_sale_report(video_id: str) -> dict:
    """Show all sales that originated from a specific video."""
    all_clicks = load_link_clicks()
    video_clicks = [c for c in all_clicks if c.get("video_id") == video_id or
                    _link_video_match(c["link_id"], video_id)]

    total_clicks = len(video_clicks)
    conversions = [c for c in video_clicks if c.get("converted")]
    total_revenue = sum(c.get("sale_amount", 0) for c in conversions)
    cvr = len(conversions) / total_clicks if total_clicks > 0 else 0.0
    epc = total_revenue / total_clicks if total_clicks > 0 else 0.0

    return {
        "video_id": video_id,
        "total_clicks": total_clicks,
        "total_conversions": len(conversions),
        "cvr_pct": round(cvr * 100, 2),
        "total_revenue_usd": round(total_revenue, 2),
        "epc": round(epc, 4),
    }


def _link_video_match(link_id: str, video_id: str) -> bool:
    """Helper: check if a link is associated with a video."""
    links = load_links()
    return links.get(link_id, {}).get("video_id") == video_id

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_create(_args):
    print("\n=== Create Tracked Affiliate Link ===")
    destination = input("Destination affiliate URL: ").strip()
    product_id = input("Product ID: ").strip()
    product_name = input("Product name: ").strip()
    source = input("Source (tiktok/instagram/youtube/email) [tiktok]: ").strip() or "tiktok"
    medium = input("Medium (organic/spark_ad/story/email) [organic]: ").strip() or "organic"
    campaign = input("Campaign name (or leave blank to use product ID): ").strip()
    video_id = input("Associated video ID (optional): ").strip()
    variant = input("Variant (A/B) [A]: ").strip() or "A"

    link = create_link(destination, product_id, product_name,
                        source=source, medium=medium, campaign=campaign,
                        video_id=video_id, variant=variant)
    print(f"\n✓ Link created: {link['id']}")
    print(f"  Tracked URL: {link['tracked_url']}")
    print(f"\nAdd this to your Beacons.ai / Linktree as: {product_name}")


def cmd_list(_args):
    dashboard = link_performance_dashboard()
    if not dashboard:
        print("No links created yet. Use `create` to add links.")
        return
    print(f"\n{'='*85}")
    print(f"ALL TRACKED LINKS")
    print(f"{'='*85}")
    print(f"{'ID':<12} {'Product':<20} {'Src':<10} {'Med':<12} {'Var':<4} {'Clicks':<8} {'CVR%':<7} {'Revenue':<12} {'EPC'}")
    print(f"{'-'*85}")
    for l in dashboard:
        print(
            f"{l['id']:<12} {l['product'][:19]:<20} {l['source'][:9]:<10} "
            f"{l['medium'][:11]:<12} {l['variant']:<4} {l['clicks']:<8} "
            f"{l['cvr_pct']:<7} ${l['revenue_usd']:<11,.2f} ${l['epc']:.4f}"
        )


def cmd_click(_args):
    print("\n=== Record Link Click ===")
    link_id = input("Link ID: ").strip()
    converted = input("Did this result in a sale? (y/n) [n]: ").strip().lower() == "y"
    sale_amount = 0.0
    if converted:
        sale_amount = float(input("Commission earned ($): ").strip() or 0)
    result = record_link_click(link_id, sale_amount=sale_amount, converted=converted)
    print(f"✓ Click recorded. Converted: {converted}" + (f" | ${sale_amount}" if converted else ""))


def cmd_ab_test(_args):
    print("\n1. Create A/B test  2. View results")
    choice = input("Choice: ").strip()
    if choice == "1":
        name = input("Test name: ").strip()
        product_id = input("Product ID: ").strip()
        url_a = input("URL A (current): ").strip()
        url_b = input("URL B (challenger): ").strip()
        hypothesis = input("Hypothesis (what you're testing): ").strip()
        test = create_ab_test(name, product_id, url_a, url_b, hypothesis)
        print(f"\n✓ A/B test created: {test['id']}")
        print(f"  Link A ID: {test['link_a_id']}")
        print(f"  Link B ID: {test['link_b_id']}")
        print(f"  Run both links, then check results with option 2.")
    elif choice == "2":
        ab_tests = load_ab_tests()
        if not ab_tests:
            print("No A/B tests running.")
            return
        test_id = input(f"Test ID ({', '.join(ab_tests.keys())}): ").strip()
        results = get_ab_test_results(test_id)
        print(f"\n{'='*60}")
        print(f"A/B TEST RESULTS: {results['name']}")
        print(f"{'='*60}")
        print(f"Hypothesis: {results['hypothesis']}")
        for var in ["a", "b"]:
            v = results[f"variant_{var}"]
            print(f"\nVariant {var.upper()}: {v['url'][:60]}")
            print(f"  Clicks: {v['clicks']}  |  CVR: {v['cvr']*100:.2f}%  |  EPC: ${v['epc']:.4f}")
        print(f"\nWinner: Variant {results['winner']}")
        if results["min_clicks_reached"]:
            print(f"Improvement: {results['improvement_pct']}%")
        else:
            print("Need 20+ clicks per variant for statistical confidence.")


def cmd_dashboard(_args):
    dashboard = link_performance_dashboard()
    total_clicks = sum(l["clicks"] for l in dashboard)
    total_revenue = sum(l["revenue_usd"] for l in dashboard)
    total_convs = sum(l["conversions"] for l in dashboard)
    overall_cvr = total_convs / total_clicks * 100 if total_clicks else 0
    overall_epc = total_revenue / total_clicks if total_clicks else 0

    print(f"\n{'='*60}")
    print(f"LINK MANAGER DASHBOARD — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"Active Links:           {len(dashboard)}")
    print(f"Total Clicks:           {total_clicks:,}")
    print(f"Total Conversions:      {total_convs:,}")
    print(f"Overall CVR:            {overall_cvr:.2f}%")
    print(f"Total Revenue:          ${total_revenue:,.2f}")
    print(f"Overall EPC:            ${overall_epc:.4f}")
    if dashboard:
        top = dashboard[0]
        print(f"\nTop Link: {top['id']} — {top['product']} (EPC: ${top['epc']:.4f})")


def cmd_top(_args):
    dashboard = link_performance_dashboard()
    top5 = [l for l in dashboard if l["clicks"] >= 5][:5]
    print(f"\n{'='*60}")
    print("TOP LINKS BY EPC (min 5 clicks)")
    print(f"{'='*60}")
    for i, l in enumerate(top5, 1):
        print(f"\n{i}. {l['product']} (Variant {l['variant']})")
        print(f"   Link ID: {l['id']}")
        print(f"   Clicks: {l['clicks']}  |  CVR: {l['cvr_pct']}%  |  EPC: ${l['epc']:.4f}")
        print(f"   Revenue: ${l['revenue_usd']:,.2f}  |  Source: {l['source']} / {l['medium']}")


def main():
    ensure_data_dir()
    parser = argparse.ArgumentParser(description="Affiliate Link Manager & A/B Testing")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("create", help="Create a new tracked link")
    subparsers.add_parser("list", help="List all tracked links")
    subparsers.add_parser("click", help="Record a click event")
    subparsers.add_parser("ab-test", help="Create or view A/B tests")
    subparsers.add_parser("dashboard", help="Link performance dashboard")
    subparsers.add_parser("top", help="Top performing links by EPC")

    args = parser.parse_args()
    commands = {
        "create": cmd_create,
        "list": cmd_list,
        "click": cmd_click,
        "ab-test": cmd_ab_test,
        "dashboard": cmd_dashboard,
        "top": cmd_top,
    }
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
