#!/usr/bin/env python3
"""
TikTok Shop — Fulfillment Tracker
------------------------------------
Track inventory, orders, creator seeds, and shipments.

Commands:
    python fulfillment_tracker.py inventory     Current stock levels
    python fulfillment_tracker.py receive       Log incoming inventory
    python fulfillment_tracker.py seed          Log creator seed shipment
    python fulfillment_tracker.py order         Log a customer order
    python fulfillment_tracker.py ship          Mark order as shipped
    python fulfillment_tracker.py dashboard     Full fulfillment overview
    python fulfillment_tracker.py suppliers     View supplier list
    python fulfillment_tracker.py add-supplier  Add a supplier
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR          = Path(__file__).parent / "data"
INVENTORY_FILE    = DATA_DIR / "inventory.json"
ORDERS_FILE       = DATA_DIR / "orders.json"
SUPPLIERS_FILE    = DATA_DIR / "suppliers.json"

FULFILLMENT_METHODS = ["self", "fbt", "3pl"]
ORDER_STATUSES      = ["pending", "picked", "shipped", "delivered", "returned"]


def _load(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        try:
            return json.load(f)
        except Exception:
            return default


def _save(path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


# ─── Inventory ────────────────────────────────────────────────────────────

def cmd_inventory(args):
    inv = _load(INVENTORY_FILE, {"products": {}})
    products = inv.get("products", {})

    if not products:
        print("\n  No inventory yet. Run: python fulfillment_tracker.py receive")
        return

    print(f"\n  INVENTORY — {datetime.now().strftime('%B %d, %Y')}")
    print(f"  {'─'*65}")
    print(f"  {'SKU':<20} {'Product':<24} {'On Hand':>8} {'Reserved':>9} {'Available':>10} {'Location':<10}")
    print(f"  {'─'*20} {'─'*24} {'─'*8} {'─'*9} {'─'*10} {'─'*10}")

    for sku, p in products.items():
        on_hand   = p.get("on_hand", 0)
        reserved  = p.get("reserved", 0)
        available = on_hand - reserved
        location  = p.get("location", "home")
        flag      = "  ⚠ LOW" if available < p.get("reorder_point", 50) else ""
        print(f"  {sku:<20} {p.get('name','?')[:23]:<24} {on_hand:>8} {reserved:>9} {available:>10} {location:<10}{flag}")

    total_units = sum(p.get("on_hand", 0) for p in products.values())
    total_value = sum(p.get("on_hand", 0) * p.get("unit_cost", 0) for p in products.values())
    print(f"\n  Total units on hand:  {total_units}")
    print(f"  Total COGS value:     ${total_value:,.2f}")
    print()


def cmd_receive(args):
    inv = _load(INVENTORY_FILE, {"products": {}})

    sku      = input("SKU (e.g. PDRN-SERUM-30ML): ").strip().upper()
    name     = input("Product name: ").strip()
    qty      = int(input("Quantity received: ").strip())
    cost     = float(input("Unit cost ($): ").strip())
    supplier = input("Supplier name: ").strip()
    location = input("Location (home/fbt/3pl): ").strip() or "home"
    reorder  = int(input("Reorder point (alert when below X units): ").strip() or "50")

    if sku not in inv["products"]:
        inv["products"][sku] = {
            "sku":          sku,
            "name":         name,
            "on_hand":      0,
            "reserved":     0,
            "unit_cost":    cost,
            "sell_price":   0,
            "location":     location,
            "reorder_point": reorder,
            "supplier":     supplier,
            "receipts":     [],
        }

    inv["products"][sku]["on_hand"]   += qty
    inv["products"][sku]["unit_cost"]  = cost
    inv["products"][sku]["location"]   = location
    inv["products"][sku]["receipts"].append({
        "date":     datetime.now().isoformat(),
        "qty":      qty,
        "cost":     cost,
        "supplier": supplier,
    })

    _save(INVENTORY_FILE, inv)
    print(f"\n  ✓ Received {qty} units of {name} ({sku})")
    print(f"    New on-hand: {inv['products'][sku]['on_hand']}")


def cmd_seed(args):
    """Log a creator seed shipment — deducts from inventory."""
    inv     = _load(INVENTORY_FILE, {"products": {}})
    orders  = _load(ORDERS_FILE, {"orders": [], "seeds": []})

    print("\nAvailable SKUs:")
    for sku, p in inv["products"].items():
        print(f"  {sku} — {p['name']} ({p.get('on_hand',0)} on hand)")

    sku      = input("\nSKU to seed: ").strip().upper()
    creator  = input("Creator handle (@username): ").strip()
    qty      = int(input("Units to send: ").strip() or "1")
    address  = input("Ship-to address (or 'TBD'): ").strip()
    tracking = input("Tracking number (or leave blank): ").strip()

    if sku in inv["products"]:
        if inv["products"][sku]["on_hand"] < qty:
            print(f"  ✗ Insufficient stock. On hand: {inv['products'][sku]['on_hand']}")
            return
        inv["products"][sku]["on_hand"] -= qty
        _save(INVENTORY_FILE, inv)

    seed = {
        "id":        f"SEED-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "sku":       sku,
        "creator":   creator,
        "qty":       qty,
        "address":   address,
        "tracking":  tracking,
        "status":    "shipped" if tracking else "pending",
        "date":      datetime.now().isoformat(),
        "content_posted": False,
        "gmv_generated":  0,
    }
    orders["seeds"].append(seed)
    _save(ORDERS_FILE, orders)

    print(f"\n  ✓ Seed logged — {qty}x {sku} → {creator}")
    print(f"    Remaining stock: {inv['products'].get(sku, {}).get('on_hand', '?')}")


def cmd_order(args):
    """Log a customer order."""
    inv    = _load(INVENTORY_FILE, {"products": {}})
    orders = _load(ORDERS_FILE, {"orders": [], "seeds": []})

    print("\nAvailable SKUs:")
    for sku, p in inv["products"].items():
        available = p.get("on_hand", 0) - p.get("reserved", 0)
        print(f"  {sku} — {p['name']} (available: {available})")

    sku        = input("\nSKU: ").strip().upper()
    qty        = int(input("Quantity: ").strip() or "1")
    sale_price = float(input("Sale price ($): ").strip())
    channel    = input("Order source (tiktok_shop/shopify/manual): ").strip() or "tiktok_shop"
    creator    = input("Creator who drove sale (handle or 'organic'): ").strip() or "organic"
    fulfil     = input("Fulfillment method (self/fbt/3pl): ").strip() or "self"

    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Reserve inventory
    if sku in inv["products"]:
        inv["products"][sku]["reserved"] = inv["products"][sku].get("reserved", 0) + qty
        _save(INVENTORY_FILE, inv)

    unit_cost  = inv.get("products", {}).get(sku, {}).get("unit_cost", 0)
    commission = sale_price * 0.20   # default 20% creator commission
    tiktok_fee = sale_price * 0.06   # TikTok 6% platform fee
    net_revenue = (sale_price - unit_cost - commission - tiktok_fee) * qty

    order = {
        "id":            order_id,
        "sku":           sku,
        "qty":           qty,
        "sale_price":    sale_price,
        "unit_cost":     unit_cost,
        "commission":    commission,
        "tiktok_fee":    tiktok_fee,
        "net_revenue":   net_revenue,
        "channel":       channel,
        "creator":       creator,
        "fulfillment":   fulfil,
        "status":        "pending",
        "ordered_at":    datetime.now().isoformat(),
        "shipped_at":    None,
        "tracking":      None,
    }
    orders["orders"].append(order)
    _save(ORDERS_FILE, orders)

    print(f"\n  ✓ Order {order_id} logged")
    print(f"    Sale: ${sale_price:.2f}  |  Net after fees: ${net_revenue:.2f}")


def cmd_ship(args):
    """Mark an order as shipped."""
    orders = _load(ORDERS_FILE, {"orders": [], "seeds": []})
    inv    = _load(INVENTORY_FILE, {"products": {}})

    pending = [o for o in orders["orders"] if o.get("status") == "pending"]
    if not pending:
        print("\n  No pending orders to ship.")
        return

    print("\nPending orders:")
    for i, o in enumerate(pending, 1):
        print(f"  {i}. {o['id']} — {o['qty']}x {o['sku']} | ${o['sale_price']:.2f} | via {o.get('creator','?')}")

    choice   = int(input("\nSelect order number: ").strip()) - 1
    order    = pending[choice]
    tracking = input("Tracking number: ").strip()
    carrier  = input("Carrier (usps/ups/fedex): ").strip() or "usps"

    # Find and update in orders list
    for o in orders["orders"]:
        if o["id"] == order["id"]:
            o["status"]     = "shipped"
            o["shipped_at"] = datetime.now().isoformat()
            o["tracking"]   = tracking
            o["carrier"]    = carrier

    # Release reservation, reduce on-hand
    sku = order["sku"]
    if sku in inv["products"]:
        inv["products"][sku]["reserved"] = max(0, inv["products"][sku].get("reserved", 0) - order["qty"])
        inv["products"][sku]["on_hand"]  = max(0, inv["products"][sku].get("on_hand", 0)  - order["qty"])

    _save(ORDERS_FILE, orders)
    _save(INVENTORY_FILE, inv)

    print(f"\n  ✓ {order['id']} marked as shipped — {carrier.upper()} {tracking}")


def cmd_dashboard(args):
    inv    = _load(INVENTORY_FILE, {"products": {}})
    orders = _load(ORDERS_FILE,    {"orders": [], "seeds": []})

    all_orders  = orders.get("orders", [])
    seeds       = orders.get("seeds", [])
    products    = inv.get("products", {})

    shipped   = [o for o in all_orders if o.get("status") == "shipped"]
    pending   = [o for o in all_orders if o.get("status") == "pending"]
    total_gmv = sum(o["sale_price"] * o["qty"] for o in all_orders)
    total_net = sum(o.get("net_revenue", 0) for o in all_orders)

    # 30-day window
    cutoff_30 = (datetime.now() - timedelta(days=30)).isoformat()
    recent    = [o for o in all_orders if o.get("ordered_at", "") > cutoff_30]
    gmv_30    = sum(o["sale_price"] * o["qty"] for o in recent)

    print(f"\n  FULFILLMENT DASHBOARD — {datetime.now().strftime('%B %d, %Y')}")
    print(f"  {'─'*50}")
    print(f"  Total orders:         {len(all_orders)}")
    print(f"  Pending (to ship):    {len(pending)}")
    print(f"  Shipped:              {len(shipped)}")
    print(f"  Creator seeds sent:   {len(seeds)}")
    print(f"  {'─'*50}")
    print(f"  All-time GMV:         ${total_gmv:,.2f}")
    print(f"  30-day GMV:           ${gmv_30:,.2f}")
    print(f"  All-time net revenue: ${total_net:,.2f}")
    print(f"  {'─'*50}")

    # Inventory alerts
    low_stock = [
        (sku, p) for sku, p in products.items()
        if p.get("on_hand", 0) < p.get("reorder_point", 50)
    ]
    if low_stock:
        print(f"\n  ⚠  LOW STOCK ALERTS:")
        for sku, p in low_stock:
            print(f"    {sku} — {p.get('on_hand',0)} units (reorder at {p.get('reorder_point',50)})")

    # Pending seeds (not yet posted)
    unposted = [s for s in seeds if not s.get("content_posted")]
    if unposted:
        print(f"\n  CREATOR SEEDS — content not yet posted ({len(unposted)}):")
        for s in unposted[:5]:
            print(f"    {s['creator']:<25} {s['sku']}  sent: {s['date'][:10]}")

    if pending:
        print(f"\n  ORDERS AWAITING SHIPMENT ({len(pending)}):")
        for o in pending[:5]:
            print(f"    {o['id']}  {o['qty']}x {o['sku']}  ${o['sale_price']:.2f}  via {o.get('creator','?')}")

    print()


def cmd_suppliers(args):
    sup = _load(SUPPLIERS_FILE, {"suppliers": {}})
    if not sup["suppliers"]:
        print("\n  No suppliers yet. Run: python fulfillment_tracker.py add-supplier")
        return

    print(f"\n  SUPPLIERS\n  {'─'*70}")
    for sid, s in sup["suppliers"].items():
        print(f"\n  {s['name']} ({s.get('country','?')})")
        print(f"    Products:    {s.get('products','?')}")
        print(f"    MOQ:         {s.get('moq','?')}")
        print(f"    Lead time:   {s.get('lead_time','?')}")
        print(f"    Unit cost:   {s.get('unit_cost','?')}")
        print(f"    Contact:     {s.get('contact','?')}")
        print(f"    Status:      {s.get('status','prospect')}")
    print()


def cmd_add_supplier(args):
    sup = _load(SUPPLIERS_FILE, {"suppliers": {}})

    name      = input("Supplier name: ").strip()
    country   = input("Country: ").strip()
    products  = input("Products they make: ").strip()
    moq       = input("MOQ: ").strip()
    lead_time = input("Lead time: ").strip()
    unit_cost = input("Unit cost range: ").strip()
    contact   = input("Website / email / contact: ").strip()
    certs     = input("Certifications (GMP, ISO, etc): ").strip()
    status    = input("Status (prospect/sampling/active): ").strip() or "prospect"

    sid = name.lower().replace(" ", "_")
    sup["suppliers"][sid] = {
        "name":      name,
        "country":   country,
        "products":  products,
        "moq":       moq,
        "lead_time": lead_time,
        "unit_cost": unit_cost,
        "contact":   contact,
        "certs":     certs,
        "status":    status,
        "added":     datetime.now().isoformat(),
        "notes":     [],
    }
    _save(SUPPLIERS_FILE, sup)
    print(f"\n  ✓ {name} added to supplier list")


def main():
    parser = argparse.ArgumentParser(description="TikTok Shop Fulfillment Tracker")
    sub    = parser.add_subparsers(dest="cmd")

    sub.add_parser("inventory",    help="View stock levels")
    sub.add_parser("receive",      help="Log incoming inventory")
    sub.add_parser("seed",         help="Log creator seed shipment")
    sub.add_parser("order",        help="Log a customer order")
    sub.add_parser("ship",         help="Mark order as shipped")
    sub.add_parser("dashboard",    help="Full overview")
    sub.add_parser("suppliers",    help="View suppliers")
    sub.add_parser("add-supplier", help="Add a supplier")

    args = parser.parse_args()

    dispatch = {
        "inventory":    cmd_inventory,
        "receive":      cmd_receive,
        "seed":         cmd_seed,
        "order":        cmd_order,
        "ship":         cmd_ship,
        "dashboard":    cmd_dashboard,
        "suppliers":    cmd_suppliers,
        "add-supplier": cmd_add_supplier,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
