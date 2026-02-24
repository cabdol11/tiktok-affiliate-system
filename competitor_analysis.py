#!/usr/bin/env python3
"""
TikTok Shop — Competitor Analysis Tracker
-------------------------------------------
Track competitors, their products, pricing, affiliate counts, and GMV.
Identify gaps and positioning opportunities.

Commands:
    python competitor_analysis.py dashboard     Overview of competitive landscape
    python competitor_analysis.py list          All tracked competitors
    python competitor_analysis.py add           Add a competitor
    python competitor_analysis.py update        Update competitor data
    python competitor_analysis.py gaps          Surface positioning gaps
    python competitor_analysis.py report        Full competitive report
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

DATA_DIR         = Path(__file__).parent / "data"
COMPETITORS_FILE = DATA_DIR / "competitors.json"


def _load():
    if not COMPETITORS_FILE.exists():
        return {"competitors": {}, "last_updated": None}
    with open(COMPETITORS_FILE) as f:
        try:
            return json.load(f)
        except Exception:
            return {"competitors": {}, "last_updated": None}


def _save(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(COMPETITORS_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


THREAT_LEVELS = {1: "LOW", 2: "MODERATE", 3: "HIGH", 4: "CRITICAL"}


def cmd_dashboard(args):
    db = _load()
    comps = db.get("competitors", {})
    if not comps:
        print("\n  No competitors tracked yet. Run: python competitor_analysis.py add")
        return

    by_category = {}
    for c in comps.values():
        cat = c.get("category", "other")
        by_category.setdefault(cat, []).append(c)

    print(f"\n  COMPETITIVE LANDSCAPE — {datetime.now().strftime('%B %d, %Y')}")
    print(f"  {'─'*70}")

    for cat, entries in sorted(by_category.items()):
        print(f"\n  [{cat.upper()}]")
        print(f"  {'Brand':<22} {'Price':>7} {'Affiliates':>11} {'GMV/mo':>12} {'Threat':<10} {'Gap'}")
        print(f"  {'─'*22} {'─'*7} {'─'*11} {'─'*12} {'─'*10} {'─'*20}")
        for c in sorted(entries, key=lambda x: x.get("threat_level", 1), reverse=True):
            threat = THREAT_LEVELS.get(c.get("threat_level", 1), "LOW")
            flag   = "⚠ " if c.get("threat_level", 1) >= 3 else "  "
            price  = f"${c.get('avg_price', 0):.0f}"
            affs   = str(c.get("affiliate_count", "?"))
            gmv    = f"${c.get('monthly_gmv', 0):,.0f}" if c.get("monthly_gmv") else "unknown"
            gap    = c.get("our_gap", "")[:30]
            print(f"  {flag}{c['name']:<22} {price:>7} {affs:>11} {gmv:>12} {threat:<10} {gap}")

    total_comps = len(comps)
    high_threat = sum(1 for c in comps.values() if c.get("threat_level", 1) >= 3)
    print(f"\n  Total competitors tracked: {total_comps}  |  High threat: {high_threat}")
    if db.get("last_updated"):
        print(f"  Last updated: {db['last_updated'][:10]}")
    print()


def cmd_list(args):
    db    = _load()
    comps = db.get("competitors", {})
    if not comps:
        print("\n  No competitors yet.")
        return

    for cid, c in comps.items():
        print(f"\n  ── {c['name']} ({c.get('origin','?')}) ──")
        print(f"     Category:       {c.get('category','?')}")
        print(f"     Products:       {c.get('products','?')}")
        print(f"     Price range:    ${c.get('min_price',0)}–${c.get('max_price',0)}")
        print(f"     Affiliates:     {c.get('affiliate_count','unknown')}")
        print(f"     Monthly GMV:    ${c.get('monthly_gmv',0):,}" if c.get('monthly_gmv') else "     Monthly GMV:    unknown")
        print(f"     TikTok Shop:    {c.get('tiktok_shop_url','N/A')}")
        print(f"     Why winning:    {c.get('why_winning','?')}")
        print(f"     Their weakness: {c.get('weakness','?')}")
        print(f"     Our gap:        {c.get('our_gap','?')}")
        print(f"     Threat level:   {THREAT_LEVELS.get(c.get('threat_level',1),'LOW')}")
    print()


def cmd_add(args):
    db = _load()

    name       = input("Brand name: ").strip()
    origin     = input("Country of origin: ").strip()
    category   = input("Category (pdrn_serum/kojic_serum/beauty/supplements/other): ").strip()
    products   = input("Key products: ").strip()
    min_price  = float(input("Min price ($): ").strip() or "0")
    max_price  = float(input("Max price ($): ").strip() or "0")
    avg_price  = (min_price + max_price) / 2
    affiliates = input("Affiliate count (number or 'unknown'): ").strip()
    gmv        = input("Est. monthly GMV ($ number or leave blank): ").strip()
    shop_url   = input("TikTok Shop URL (or leave blank): ").strip()
    winning    = input("Why are they winning right now: ").strip()
    weakness   = input("Their biggest weakness: ").strip()
    our_gap    = input("How we beat them (our positioning gap): ").strip()
    threat     = int(input("Threat level 1=Low 2=Moderate 3=High 4=Critical: ").strip() or "2")

    cid = name.lower().replace(" ", "_")
    db["competitors"][cid] = {
        "id":              cid,
        "name":            name,
        "origin":          origin,
        "category":        category,
        "products":        products,
        "min_price":       min_price,
        "max_price":       max_price,
        "avg_price":       avg_price,
        "affiliate_count": int(affiliates) if affiliates.isdigit() else affiliates,
        "monthly_gmv":     float(gmv) if gmv else None,
        "tiktok_shop_url": shop_url,
        "why_winning":     winning,
        "weakness":        weakness,
        "our_gap":         our_gap,
        "threat_level":    threat,
        "added":           datetime.now().isoformat(),
        "history":         [],
    }
    _save(db)
    print(f"\n  ✓ {name} added to competitor tracker")


def cmd_update(args):
    db    = _load()
    comps = db.get("competitors", {})

    print("\nCompetitors:")
    cids = list(comps.keys())
    for i, cid in enumerate(cids, 1):
        print(f"  {i}. {comps[cid]['name']}")
    choice = int(input("\nSelect number: ").strip()) - 1
    cid    = cids[choice]
    c      = comps[cid]

    print(f"\nUpdating: {c['name']}  (press Enter to keep current value)")

    fields = {
        "affiliate_count": f"Affiliate count (current: {c.get('affiliate_count','?')}): ",
        "monthly_gmv":     f"Monthly GMV (current: ${c.get('monthly_gmv',0):,}): ",
        "avg_price":       f"Avg price (current: ${c.get('avg_price',0):.0f}): ",
        "weakness":        f"Weakness (current: {c.get('weakness','?')}): ",
        "our_gap":         f"Our gap (current: {c.get('our_gap','?')}): ",
        "threat_level":    f"Threat 1-4 (current: {c.get('threat_level',1)}): ",
    }

    # Snapshot history before update
    snapshot = {k: c.get(k) for k in fields}
    snapshot["date"] = datetime.now().isoformat()
    c.setdefault("history", []).append(snapshot)

    for field, prompt in fields.items():
        val = input(prompt).strip()
        if val:
            if field in ("affiliate_count", "threat_level"):
                c[field] = int(val) if val.isdigit() else val
            elif field == "monthly_gmv":
                c[field] = float(val.replace(",", "").replace("$", ""))
            elif field == "avg_price":
                c[field] = float(val.replace("$", ""))
            else:
                c[field] = val

    c["last_updated"] = datetime.now().isoformat()
    _save(db)
    print(f"\n  ✓ {c['name']} updated")


def cmd_gaps(args):
    db    = _load()
    comps = db.get("competitors", {})

    print(f"\n  POSITIONING GAPS — Where We Win\n  {'─'*60}")

    # Price gaps
    by_cat = {}
    for c in comps.values():
        cat = c.get("category", "other")
        by_cat.setdefault(cat, []).append(c)

    for cat, entries in sorted(by_cat.items()):
        prices = [c.get("avg_price", 0) for c in entries if c.get("avg_price")]
        if prices:
            min_p = min(prices)
            max_p = max(prices)
            print(f"\n  [{cat.upper()}]")
            print(f"  Competitor price range:  ${min_p:.0f} – ${max_p:.0f}")
            if min_p > 20:
                print(f"  ✓ PRICE GAP: Under-cut at ${min_p - 4:.0f} — below every competitor")
            else:
                print(f"  Price floor is low. Compete on quality + creator volume instead.")

        weaknesses = [c.get("weakness", "") for c in entries if c.get("weakness")]
        gaps       = [c.get("our_gap", "") for c in entries if c.get("our_gap")]

        if weaknesses:
            print(f"\n  Competitor weaknesses to exploit:")
            for w in set(weaknesses):
                if w:
                    print(f"    ▶  {w}")

        if gaps:
            print(f"\n  Our positioning advantages:")
            for g in set(gaps):
                if g:
                    print(f"    ✓  {g}")

    print()


def cmd_report(args):
    db    = _load()
    comps = db.get("competitors", {})

    if not comps:
        print("\n  No data. Run: python competitor_analysis.py add")
        return

    total_aff_tracked = sum(
        c.get("affiliate_count", 0) for c in comps.values()
        if isinstance(c.get("affiliate_count"), int)
    )
    total_gmv_tracked = sum(
        c.get("monthly_gmv", 0) for c in comps.values()
        if c.get("monthly_gmv")
    )
    critical = [c for c in comps.values() if c.get("threat_level", 1) >= 3]

    print(f"\n  COMPETITIVE INTELLIGENCE REPORT")
    print(f"  Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}")
    print(f"  {'─'*60}")
    print(f"  Competitors tracked:       {len(comps)}")
    print(f"  High/critical threats:     {len(critical)}")
    print(f"  Total competitor GMV/mo:   ${total_gmv_tracked:,.0f}")
    print(f"  Total competitor affiliates: {total_aff_tracked:,}")
    print()

    if critical:
        print(f"  TOP THREATS — Act On These:")
        for c in sorted(critical, key=lambda x: x.get("threat_level", 1), reverse=True):
            print(f"\n  ⚠  {c['name']} (Threat: {THREAT_LEVELS.get(c['threat_level'])})")
            print(f"     Why winning:  {c.get('why_winning','?')}")
            print(f"     Their weakness: {c.get('weakness','?')}")
            print(f"     Our counter:  {c.get('our_gap','?')}")

    print(f"\n  MARKET SHARE OPPORTUNITY:")
    if total_gmv_tracked:
        target_share = total_gmv_tracked * 0.10
        print(f"  10% of tracked competitor GMV = ${target_share:,.0f}/month")
        print(f"  That is your minimum viable target.")
    print()


def main():
    parser = argparse.ArgumentParser(description="TikTok Shop Competitor Tracker")
    sub    = parser.add_subparsers(dest="cmd")

    sub.add_parser("dashboard", help="Competitive overview")
    sub.add_parser("list",      help="All competitor details")
    sub.add_parser("add",       help="Add a competitor")
    sub.add_parser("update",    help="Update competitor data")
    sub.add_parser("gaps",      help="Positioning gaps")
    sub.add_parser("report",    help="Full competitive report")

    args = parser.parse_args()
    dispatch = {
        "dashboard": cmd_dashboard,
        "list":      cmd_list,
        "add":       cmd_add,
        "update":    cmd_update,
        "gaps":      cmd_gaps,
        "report":    cmd_report,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
