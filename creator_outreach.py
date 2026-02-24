#!/usr/bin/env python3
"""
creator_outreach.py
-------------------
Manages TikTok beauty/skincare micro-creator recruitment pipeline.
Tracks creators from discovery through active revenue-sharing partnership.
Owner earns 20–30% of creator affiliate commissions as manager fee.

Usage:
    python creator_outreach.py add-creator      # Add a creator to pipeline
    python creator_outreach.py update-status    # Update outreach status
    python creator_outreach.py add-note         # Add note to a creator record
    python creator_outreach.py pipeline         # Full pipeline with status counts
    python creator_outreach.py dashboard        # Active creators, products, revenue share
    python creator_outreach.py top-creators     # Top earners by revenue generated
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
CREATORS_FILE = DATA_DIR / "creators.json"

# Valid pipeline statuses in order
STATUSES = [
    "discovered",   # Found the creator, haven't reached out yet
    "contacted",    # Sent DM or email
    "replied",      # Creator responded (positive or neutral)
    "onboarded",    # Agreed to rev-share, set up with links
    "active",       # Posting content, generating revenue
    "churned",      # Stopped posting or dropped out
]

# Owner's manager fee range (fraction of creator earnings)
MANAGER_FEE_LOW  = 0.20   # 20%
MANAGER_FEE_HIGH = 0.30   # 30%

NICHES = [
    "Skincare",
    "Makeup",
    "Haircare",
    "Nails",
    "Fragrance",
    "Wellness",
    "Beauty Tools",
    "Clean Beauty",
    "Anti-Aging",
    "Other",
]

CONTACT_PLATFORMS = ["TikTok DM", "Email", "Instagram DM", "Twitter DM", "Other"]

# ---------------------------------------------------------------------------
# Data helpers  (same pattern as affiliate_tracker.py / financials.py)
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


def load_creators():
    return load_json(CREATORS_FILE, {})


def save_creators(data):
    save_json(CREATORS_FILE, data)

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _creator_id(handle: str) -> str:
    """Normalise a TikTok handle to a stable dict key."""
    return handle.lstrip("@").lower().strip()


def add_creator(
    handle: str,
    niche: str,
    followers: int,
    contact_platform: str,
    contact_value: str,
    platform_notes: str = "",
    manager_fee_pct: float = MANAGER_FEE_LOW,
) -> dict:
    """Add a new creator to the outreach pipeline."""
    creators = load_creators()
    cid = _creator_id(handle)
    if cid in creators:
        raise ValueError(f"Creator @{cid} already exists. Use update-status or add-note.")

    creator = {
        "id": cid,
        "handle": f"@{cid}",
        "niche": niche,
        "followers": followers,
        "contact_platform": contact_platform,
        "contact_value": contact_value,
        "platform_notes": platform_notes,
        "status": "discovered",
        "manager_fee_pct": round(manager_fee_pct, 4),
        "products": [],             # list of product_ids they're promoting
        "monthly_revenue_usd": 0.0, # creator's gross monthly affiliate rev
        "added_at": datetime.now().isoformat(),
        "status_updated_at": datetime.now().isoformat(),
        "notes": [],
    }
    creators[cid] = creator
    save_creators(creators)
    return creator


def update_status(handle: str, new_status: str, note: str = "") -> dict:
    """Move a creator to a new pipeline status."""
    if new_status not in STATUSES:
        raise ValueError(f"Invalid status '{new_status}'. Choose from: {', '.join(STATUSES)}")
    creators = load_creators()
    cid = _creator_id(handle)
    if cid not in creators:
        raise KeyError(f"Creator @{cid} not found. Add them first with add-creator.")

    old_status = creators[cid]["status"]
    creators[cid]["status"] = new_status
    creators[cid]["status_updated_at"] = datetime.now().isoformat()

    # Auto-log the status change as a note
    change_note = f"Status: {old_status} -> {new_status}"
    if note:
        change_note += f" | {note}"
    creators[cid]["notes"].append({
        "timestamp": datetime.now().isoformat(),
        "text": change_note,
    })

    save_creators(creators)
    return creators[cid]


def add_note(handle: str, text: str) -> dict:
    """Append a free-text note to a creator's record."""
    creators = load_creators()
    cid = _creator_id(handle)
    if cid not in creators:
        raise KeyError(f"Creator @{cid} not found.")

    creators[cid]["notes"].append({
        "timestamp": datetime.now().isoformat(),
        "text": text.strip(),
    })
    save_creators(creators)
    return creators[cid]


def update_revenue(handle: str, monthly_revenue_usd: float,
                   products: list = None) -> dict:
    """Update a creator's monthly revenue figure and product list."""
    creators = load_creators()
    cid = _creator_id(handle)
    if cid not in creators:
        raise KeyError(f"Creator @{cid} not found.")

    creators[cid]["monthly_revenue_usd"] = round(monthly_revenue_usd, 2)
    if products is not None:
        creators[cid]["products"] = products
    save_creators(creators)
    return creators[cid]


def get_pipeline() -> dict:
    """Return all creators grouped by status."""
    creators = load_creators()
    pipeline = {s: [] for s in STATUSES}
    for c in creators.values():
        pipeline[c["status"]].append(c)
    # Sort each bucket by followers descending
    for s in STATUSES:
        pipeline[s].sort(key=lambda x: x["followers"], reverse=True)
    return pipeline


def get_dashboard() -> dict:
    """Aggregate active-creator stats and owner revenue share."""
    creators = load_creators()
    active = [c for c in creators.values() if c["status"] == "active"]

    total_creator_rev = sum(c["monthly_revenue_usd"] for c in active)
    owner_low  = sum(c["monthly_revenue_usd"] * MANAGER_FEE_LOW  for c in active)
    owner_high = sum(c["monthly_revenue_usd"] * MANAGER_FEE_HIGH for c in active)

    rows = []
    for c in sorted(active, key=lambda x: x["monthly_revenue_usd"], reverse=True):
        rows.append({
            "handle": c["handle"],
            "niche": c["niche"],
            "followers": c["followers"],
            "products": c["products"],
            "monthly_revenue_usd": c["monthly_revenue_usd"],
            "owner_cut_low":  round(c["monthly_revenue_usd"] * MANAGER_FEE_LOW,  2),
            "owner_cut_high": round(c["monthly_revenue_usd"] * MANAGER_FEE_HIGH, 2),
            "manager_fee_pct": c["manager_fee_pct"],
        })

    return {
        "active_count": len(active),
        "total_creator_rev_monthly": round(total_creator_rev, 2),
        "owner_monthly_low":  round(owner_low,  2),
        "owner_monthly_high": round(owner_high, 2),
        "creators": rows,
    }


def get_top_creators(limit: int = 10) -> list:
    """Return top creators ranked by monthly revenue."""
    creators = load_creators()
    ranked = sorted(
        creators.values(),
        key=lambda c: c["monthly_revenue_usd"],
        reverse=True,
    )
    results = []
    for c in ranked[:limit]:
        results.append({
            "rank": ranked.index(c) + 1,
            "handle": c["handle"],
            "status": c["status"],
            "niche": c["niche"],
            "followers": c["followers"],
            "monthly_revenue_usd": c["monthly_revenue_usd"],
            "owner_cut_low":  round(c["monthly_revenue_usd"] * MANAGER_FEE_LOW,  2),
            "owner_cut_high": round(c["monthly_revenue_usd"] * MANAGER_FEE_HIGH, 2),
        })
    return results

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _fmt_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def cmd_add_creator(_args):
    print("\n=== Add Creator to Pipeline ===")
    handle = input("TikTok handle (e.g. @glamwithgrace): ").strip()
    if not handle:
        print("Handle is required.")
        return

    print("Niches: " + ", ".join(f"{i+1}. {n}" for i, n in enumerate(NICHES)))
    niche_idx = int(input("Niche number: ").strip()) - 1
    niche = NICHES[niche_idx] if 0 <= niche_idx < len(NICHES) else "Other"

    followers = int(input("Followers (e.g. 45000): ").strip())

    print("Contact platforms: " + ", ".join(f"{i+1}. {p}" for i, p in enumerate(CONTACT_PLATFORMS)))
    plat_idx = int(input("Contact platform number: ").strip()) - 1
    contact_platform = CONTACT_PLATFORMS[plat_idx] if 0 <= plat_idx < len(CONTACT_PLATFORMS) else "Other"

    contact_value = input("Contact value (email address or username): ").strip()
    platform_notes = input("Platform notes (optional — engagement rate, vibe, etc.): ").strip()
    fee_input = input(f"Manager fee % (default {int(MANAGER_FEE_LOW*100)}%, e.g. 25): ").strip()
    manager_fee_pct = float(fee_input) / 100 if fee_input else MANAGER_FEE_LOW

    creator = add_creator(handle, niche, followers, contact_platform,
                          contact_value, platform_notes, manager_fee_pct)

    print(f"\nCreator added: {creator['handle']} | {creator['niche']} | "
          f"{_fmt_followers(creator['followers'])} followers | Status: {creator['status']}")
    print(f"Contact: {creator['contact_platform']} — {creator['contact_value']}")


def cmd_update_status(_args):
    print("\n=== Update Creator Status ===")
    creators = load_creators()
    if not creators:
        print("No creators in pipeline yet. Use add-creator first.")
        return

    handle = input("TikTok handle: ").strip()
    print("Statuses: " + " → ".join(STATUSES))
    new_status = input("New status: ").strip()
    note = input("Note (optional): ").strip()

    # If moving to active, offer revenue/product update
    extra_note = ""
    cid = _creator_id(handle)
    if new_status == "active" and cid in creators:
        rev_input = input("Monthly affiliate revenue for this creator ($, or 0): ").strip()
        if rev_input:
            rev = float(rev_input)
            products_input = input("Products they're promoting (comma-separated IDs, or blank): ").strip()
            products = [p.strip() for p in products_input.split(",")] if products_input else []
            update_revenue(handle, rev, products)
            extra_note = f"Monthly rev set to ${rev:.2f}"

    creator = update_status(handle, new_status, note)
    print(f"\nUpdated: {creator['handle']} → {creator['status']}")
    if extra_note:
        print(f"  {extra_note}")


def cmd_add_note(_args):
    print("\n=== Add Note to Creator ===")
    handle = input("TikTok handle: ").strip()
    text = input("Note: ").strip()
    if not text:
        print("Note cannot be empty.")
        return
    creator = add_note(handle, text)
    print(f"\nNote added to {creator['handle']} ({len(creator['notes'])} notes total)")


def cmd_pipeline(_args):
    pipeline = get_pipeline()
    creators = load_creators()

    print(f"\n{'='*70}")
    print(f"CREATOR PIPELINE — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")

    total = len(creators)
    print(f"Total creators tracked: {total}")
    print()

    # Status summary bar
    print("Status counts:")
    for status in STATUSES:
        count = len(pipeline[status])
        bar = "#" * count
        print(f"  {status:<12} {count:>3}  {bar}")

    print()

    # Detail rows per status
    for status in STATUSES:
        group = pipeline[status]
        if not group:
            continue
        print(f"--- {status.upper()} ({len(group)}) ---")
        print(f"  {'Handle':<22} {'Niche':<14} {'Followers':<10} {'Contact':<16} {'Last Update'}")
        print(f"  {'-'*80}")
        for c in group:
            updated = c["status_updated_at"][:10]
            contact_short = f"{c['contact_platform'][:8]}: {c['contact_value'][:14]}"
            print(
                f"  {c['handle']:<22} {c['niche']:<14} "
                f"{_fmt_followers(c['followers']):<10} {contact_short:<22} {updated}"
            )
        print()


def cmd_dashboard(_args):
    dash = get_dashboard()

    print(f"\n{'='*75}")
    print(f"ACTIVE CREATOR DASHBOARD — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*75}")
    print(f"Active creators:        {dash['active_count']}")
    print(f"Total creator rev/mo:   ${dash['total_creator_rev_monthly']:,.2f}")
    print(f"Owner fee/mo (20%):     ${dash['owner_monthly_low']:,.2f}")
    print(f"Owner fee/mo (30%):     ${dash['owner_monthly_high']:,.2f}")

    if not dash["creators"]:
        print("\nNo active creators yet. Onboard creators and set status to 'active'.")
        return

    print(f"\n{'Handle':<22} {'Niche':<14} {'Followers':<11} {'Creator Rev/mo':<17} {'Owner Cut':<20} Products")
    print(f"{'-'*95}")

    for c in dash["creators"]:
        products_str = ", ".join(c["products"]) if c["products"] else "—"
        cut_range = f"${c['owner_cut_low']:,.2f}–${c['owner_cut_high']:,.2f}"
        fee_label = f"({int(c['manager_fee_pct']*100)}% negotiated)" if c["manager_fee_pct"] not in (MANAGER_FEE_LOW, MANAGER_FEE_HIGH) else ""
        print(
            f"{c['handle']:<22} {c['niche']:<14} "
            f"{_fmt_followers(c['followers']):<11} "
            f"${c['monthly_revenue_usd']:<16,.2f} "
            f"{cut_range:<20} {products_str} {fee_label}"
        )

    print(f"{'-'*95}")
    print(
        f"{'TOTALS':<22} {'':<14} {'':<11} "
        f"${dash['total_creator_rev_monthly']:<16,.2f} "
        f"${dash['owner_monthly_low']:,.2f}–${dash['owner_monthly_high']:,.2f}"
    )


def cmd_top_creators(_args):
    limit_input = input("How many creators to show (default 10): ").strip()
    limit = int(limit_input) if limit_input else 10

    top = get_top_creators(limit)

    if not top:
        print("\nNo creators tracked yet. Use add-creator to start.")
        return

    print(f"\n{'='*80}")
    print(f"TOP {limit} CREATORS BY REVENUE — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*80}")
    print(f"{'#':<4} {'Handle':<22} {'Status':<12} {'Niche':<14} {'Followers':<11} {'Rev/mo':<12} {'Owner Cut'}")
    print(f"{'-'*80}")

    for c in top:
        cut_range = f"${c['owner_cut_low']:,.2f}–${c['owner_cut_high']:,.2f}"
        print(
            f"{c['rank']:<4} {c['handle']:<22} {c['status']:<12} {c['niche']:<14} "
            f"{_fmt_followers(c['followers']):<11} "
            f"${c['monthly_revenue_usd']:<11,.2f} {cut_range}"
        )

    total_rev = sum(c["monthly_revenue_usd"] for c in top)
    total_cut_low  = sum(c["owner_cut_low"]  for c in top)
    total_cut_high = sum(c["owner_cut_high"] for c in top)
    print(f"{'-'*80}")
    print(f"{'':4} {'TOTALS':<22} {'':<12} {'':<14} {'':<11} ${total_rev:<11,.2f} ${total_cut_low:,.2f}–${total_cut_high:,.2f}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    ensure_data_dir()

    parser = argparse.ArgumentParser(
        description="TikTok Beauty/Skincare Creator Outreach & Revenue Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  add-creator     Add a creator to the pipeline
  update-status   Move a creator through the pipeline
  add-note        Append a note to a creator's record
  pipeline        Full pipeline view with status counts
  dashboard       Active creators, products, and owner revenue share
  top-creators    Top earners ranked by monthly revenue

Pipeline stages:
  discovered -> contacted -> replied -> onboarded -> active -> churned

Rev-share model:
  Creator earns affiliate commission.
  Owner takes 20-30% of that as manager fee.
  No upfront costs to creator.
        """,
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("add-creator",    help="Add a creator to the pipeline")
    subparsers.add_parser("update-status",  help="Update a creator's outreach status")
    subparsers.add_parser("add-note",       help="Add a note to a creator's record")
    subparsers.add_parser("pipeline",       help="Show full pipeline with status counts")
    subparsers.add_parser("dashboard",      help="Active creators, products, and monthly revenue share")
    subparsers.add_parser("top-creators",   help="Top earning creators by revenue generated")

    args = parser.parse_args()
    commands = {
        "add-creator":   cmd_add_creator,
        "update-status": cmd_update_status,
        "add-note":      cmd_add_note,
        "pipeline":      cmd_pipeline,
        "dashboard":     cmd_dashboard,
        "top-creators":  cmd_top_creators,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
