#!/usr/bin/env python3
"""
TikTok Shop OS — Brand Outreach CRM
--------------------------------------
Track every prospect, outreach touchpoint, and deal stage.

Commands:
    python brand_outreach.py add          Add a prospect
    python brand_outreach.py pipeline     View full pipeline
    python brand_outreach.py touch        Log a touchpoint
    python brand_outreach.py convert      Move to next stage
    python brand_outreach.py dashboard    Revenue summary
    python brand_outreach.py prospects    List all prospects
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR   = Path(__file__).parent / "data"
CRM_FILE   = DATA_DIR / "brand_crm.json"

STAGES = [
    "identified",
    "researched",
    "contacted",
    "replied",
    "demo_scheduled",
    "demo_done",
    "proposal_sent",
    "negotiating",
    "closed_won",
    "closed_lost",
]

STAGE_LABELS = {
    "identified":      "🔍 Identified",
    "researched":      "📋 Researched",
    "contacted":       "📤 Contacted",
    "replied":         "💬 Replied",
    "demo_scheduled":  "📅 Demo Scheduled",
    "demo_done":       "✅ Demo Done",
    "proposal_sent":   "📄 Proposal Sent",
    "negotiating":     "🤝 Negotiating",
    "closed_won":      "🟢 Closed Won",
    "closed_lost":     "🔴 Closed Lost",
}


def _load():
    if not CRM_FILE.exists():
        return {"prospects": {}, "deals": [], "stats": {}}
    with open(CRM_FILE) as f:
        try:
            return json.load(f)
        except Exception:
            return {"prospects": {}, "deals": [], "stats": {}}


def _save(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CRM_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def cmd_add(args):
    crm = _load()
    brand     = input("Brand name: ").strip()
    niche     = input("Niche (beauty/supplements/home/fashion/other): ").strip()
    est_gmv   = input("Estimated monthly GMV ($): ").strip()
    contact   = input("Contact name: ").strip()
    contact_url = input("LinkedIn / TikTok / Email: ").strip()
    notes     = input("Notes (product, shop size, why a fit): ").strip()

    pid = brand.lower().replace(" ", "_")
    crm["prospects"][pid] = {
        "id":           pid,
        "brand":        brand,
        "niche":        niche,
        "est_monthly_gmv": float(est_gmv.replace(",", "").replace("$", "") or 0),
        "contact":      contact,
        "contact_url":  contact_url,
        "notes":        notes,
        "stage":        "identified",
        "touchpoints":  [],
        "added":        datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat(),
        "deal_type":    None,   # managed | saas
        "monthly_value": 0,
    }
    _save(crm)
    print(f"\n  ✓ {brand} added to pipeline — Stage: Identified")


def cmd_touch(args):
    crm = _load()
    print("\nProspects:")
    for i, (pid, p) in enumerate(crm["prospects"].items(), 1):
        print(f"  {i}. {p['brand']} ({STAGE_LABELS.get(p['stage'], p['stage'])})")
    choice = input("\nSelect number: ").strip()
    pids   = list(crm["prospects"].keys())
    pid    = pids[int(choice) - 1]

    channel = input("Channel (email/linkedin/tiktok/call/meeting): ").strip()
    message = input("What was said / sent: ").strip()
    outcome = input("Outcome (no_reply/replied/meeting_booked/not_interested): ").strip()

    touch = {
        "date":    datetime.now().isoformat(),
        "channel": channel,
        "message": message,
        "outcome": outcome,
    }
    crm["prospects"][pid]["touchpoints"].append(touch)
    crm["prospects"][pid]["last_activity"] = datetime.now().isoformat()

    if outcome == "replied" and crm["prospects"][pid]["stage"] == "contacted":
        crm["prospects"][pid]["stage"] = "replied"
        print("  → Stage updated to: Replied")
    elif outcome == "meeting_booked":
        crm["prospects"][pid]["stage"] = "demo_scheduled"
        print("  → Stage updated to: Demo Scheduled")

    _save(crm)
    print(f"\n  ✓ Touchpoint logged for {crm['prospects'][pid]['brand']}")


def cmd_convert(args):
    crm = _load()
    print("\nProspects:")
    for i, (pid, p) in enumerate(crm["prospects"].items(), 1):
        print(f"  {i}. {p['brand']} — {STAGE_LABELS.get(p['stage'], p['stage'])}")
    choice   = input("\nSelect number: ").strip()
    pids     = list(crm["prospects"].keys())
    pid      = pids[int(choice) - 1]
    prospect = crm["prospects"][pid]

    current_idx = STAGES.index(prospect["stage"]) if prospect["stage"] in STAGES else 0
    print(f"\nCurrent stage: {STAGE_LABELS[prospect['stage']]}")
    print("Move to:")
    for i, s in enumerate(STAGES[current_idx + 1:], 1):
        print(f"  {i}. {STAGE_LABELS[s]}")
    move = input("\nSelect: ").strip()
    new_stage = STAGES[current_idx + int(move)]

    crm["prospects"][pid]["stage"] = new_stage
    crm["prospects"][pid]["last_activity"] = datetime.now().isoformat()

    if new_stage == "closed_won":
        deal_type = input("Deal type (managed/saas): ").strip()
        monthly   = float(input("Monthly value ($): ").strip().replace(",", "").replace("$", "") or 0)
        crm["prospects"][pid]["deal_type"]    = deal_type
        crm["prospects"][pid]["monthly_value"] = monthly
        crm["deals"].append({
            "brand":         prospect["brand"],
            "deal_type":     deal_type,
            "monthly_value": monthly,
            "closed_date":   datetime.now().isoformat(),
        })
        print(f"\n  🟢 DEAL CLOSED — {prospect['brand']} | ${monthly:,.0f}/month")

    _save(crm)
    print(f"\n  ✓ {prospect['brand']} → {STAGE_LABELS[new_stage]}")


def cmd_pipeline(args):
    crm = _load()
    prospects = crm.get("prospects", {})

    print(f"\n  BRAND PIPELINE — {datetime.now().strftime('%B %d, %Y')}")
    print(f"  {'─'*70}")

    stage_groups = {}
    for p in prospects.values():
        s = p.get("stage", "identified")
        stage_groups.setdefault(s, []).append(p)

    total_pipeline = 0
    for stage in STAGES:
        group = stage_groups.get(stage, [])
        if not group:
            continue
        label = STAGE_LABELS.get(stage, stage)
        print(f"\n  {label} ({len(group)})")
        for p in group:
            gmv   = p.get("est_monthly_gmv", 0)
            val   = p.get("monthly_value", 0)
            touch = len(p.get("touchpoints", []))
            last  = p.get("last_activity", "")[:10]
            total_pipeline += gmv * 0.18
            print(f"    • {p['brand']:<28} GMV: ${gmv:>8,.0f}/mo   Touches: {touch}   Last: {last}")

    print(f"\n  {'─'*70}")
    print(f"  Total prospects:     {len(prospects)}")
    won = [p for p in prospects.values() if p.get("stage") == "closed_won"]
    won_mrr = sum(p.get("monthly_value", 0) for p in won)
    print(f"  Closed won:          {len(won)}  |  MRR: ${won_mrr:,.0f}/month")
    print(f"  Pipeline value:      ~${total_pipeline:,.0f}/month (at 18% of est. GMV)")
    print()


def cmd_dashboard(args):
    crm = _load()
    prospects = crm.get("prospects", {})
    deals     = crm.get("deals", [])

    won = [p for p in prospects.values() if p.get("stage") == "closed_won"]
    mrr = sum(p.get("monthly_value", 0) for p in won)
    arr = mrr * 12

    managed = [p for p in won if p.get("deal_type") == "managed"]
    saas    = [p for p in won if p.get("deal_type") == "saas"]

    active     = [p for p in prospects.values() if p.get("stage") not in ("closed_won", "closed_lost")]
    stale_cut  = (datetime.now() - timedelta(days=7)).isoformat()
    stale      = [p for p in active if p.get("last_activity", "") < stale_cut]

    print(f"\n  SALES DASHBOARD — {datetime.now().strftime('%B %d, %Y')}")
    print(f"  {'─'*50}")
    print(f"  MRR:              ${mrr:>10,.0f}")
    print(f"  ARR:              ${arr:>10,.0f}")
    print(f"  Closed deals:     {len(won):>10}")
    print(f"    Managed:        {len(managed):>10}")
    print(f"    SaaS:           {len(saas):>10}")
    print(f"  Active pipeline:  {len(active):>10}")
    print(f"  Stale (>7d):      {len(stale):>10}  ← follow up today")
    print(f"  {'─'*50}")

    # Conversion funnel
    contacted = [p for p in prospects.values() if p.get("stage") not in ("identified", "researched")]
    replied   = [p for p in prospects.values() if p.get("stage") not in ("identified", "researched", "contacted")]
    demos     = [p for p in prospects.values() if p.get("stage") in ("demo_done", "proposal_sent", "negotiating", "closed_won")]

    if contacted:
        print(f"\n  CONVERSION FUNNEL")
        print(f"  Contacted:        {len(contacted)}")
        print(f"  Replied:          {len(replied)}  ({len(replied)/len(contacted)*100:.0f}% of contacted)")
        print(f"  Demos:            {len(demos)}  ({len(demos)/len(contacted)*100:.0f}% of contacted)")
        print(f"  Closed:           {len(won)}  ({len(won)/len(contacted)*100:.0f}% of contacted)")

    if stale:
        print(f"\n  FOLLOW UP TODAY:")
        for p in stale[:5]:
            days = (datetime.now() - datetime.fromisoformat(p["last_activity"])).days
            print(f"  ▶  {p['brand']:<28} {days}d since last touch — {STAGE_LABELS.get(p['stage'], p['stage'])}")
    print()


def cmd_prospects(args):
    crm = _load()
    prospects = list(crm.get("prospects", {}).values())
    if not prospects:
        print("\n  No prospects yet. Run: python brand_outreach.py add")
        return
    print(f"\n  ALL PROSPECTS ({len(prospects)})\n")
    print(f"  {'Brand':<28} {'Niche':<14} {'Stage':<20} {'GMV/mo':>10}")
    print(f"  {'─'*28} {'─'*14} {'─'*20} {'─'*10}")
    for p in sorted(prospects, key=lambda x: STAGES.index(x.get("stage","identified")) if x.get("stage") in STAGES else 99, reverse=True):
        print(f"  {p['brand']:<28} {p.get('niche','?'):<14} {STAGE_LABELS.get(p['stage'],p['stage']):<20} ${p.get('est_monthly_gmv',0):>9,.0f}")
    print()


def main():
    parser = argparse.ArgumentParser(description="TikTok Shop OS — Brand CRM")
    sub    = parser.add_subparsers(dest="cmd")
    sub.add_parser("add",       help="Add a prospect")
    sub.add_parser("pipeline",  help="View pipeline")
    sub.add_parser("touch",     help="Log a touchpoint")
    sub.add_parser("convert",   help="Advance stage")
    sub.add_parser("dashboard", help="Revenue summary")
    sub.add_parser("prospects", help="List all")
    args = parser.parse_args()

    dispatch = {
        "add":       cmd_add,
        "pipeline":  cmd_pipeline,
        "touch":     cmd_touch,
        "convert":   cmd_convert,
        "dashboard": cmd_dashboard,
        "prospects": cmd_prospects,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
