# Fulfillment Guide
## How products get from supplier to customer

---

## THE CHAIN

```
SUPPLIER (Korea/China)
      ↓  ships to you (or direct to 3PL/FBT)
YOUR INVENTORY
      ↓  you list product on TikTok Shop
TIKTOK SHOP LISTING
      ↓  creator posts video → customer clicks → buys
CUSTOMER ORDER
      ↓  you (or FBT/3PL) picks, packs, ships
CUSTOMER RECEIVES PRODUCT
      ↓  TikTok releases payment ~15 days after delivery
YOU GET PAID
```

---

## THREE FULFILLMENT METHODS

### Method 1 — Self-Fulfillment (Start here)
You store inventory at home. You pack and ship each order manually.

**Use when:** 1–50 orders/day
**Cost:** ~$0 setup. USPS/UPS/FedEx per-shipment rates.
**Tools:** Pirateship.com (discounted USPS rates, up to 89% off retail)

**Workflow:**
1. Order comes in via TikTok Shop Seller Center notification
2. Print shipping label (Pirateship or TikTok Shop built-in label tool)
3. Pack product, attach label, drop at carrier
4. Enter tracking in TikTok Shop Seller Center
5. Done

---

### Method 2 — Fulfilled by TikTok (FBT) ⭐ Recommended at scale
TikTok's own warehouse. You ship inventory to them once. They handle every order automatically.

**Use when:** 50+ orders/day OR when self-fulfillment is consuming too much time
**Cost:** ~$0.75/cubic ft/month storage + $3–6/order fulfillment fee
**Benefit:** FBT badge on listings → higher conversion rate

**Setup steps:**
1. Go to TikTok Shop Seller Center → Fulfillment → Fulfilled by TikTok
2. Create inbound shipment
3. Print FBT labels for your inventory boxes
4. Ship boxes to TikTok's warehouse (they assign the nearest one)
5. Inventory goes live — all future orders auto-fulfilled

**FBT warehouse locations (US):** Multiple across CA, TX, NJ, IL

---

### Method 3 — Third-Party Logistics (3PL)
Use an external warehouse. Good for multi-channel (TikTok + Shopify + Amazon from one place).

**Top options:**
| Provider | Best For | Cost |
|----------|---------|------|
| ShipBob | DTC brands, Shopify integration | ~$5–8/order |
| ShipHero | Volume sellers | ~$4–7/order |
| Whiplash | Beauty/lifestyle brands | Custom quote |
| Pirateship | Self-ship with discounted rates | Pay per label |

---

## CREATOR SEEDING (Separate from customer fulfillment)

Before customers can buy, creators need the product to make content.

**The seeding flow:**
1. Identify creator (use `creator_outreach.py`)
2. Get their shipping address (DM them on TikTok)
3. Ship 1–2 units to their address from your home inventory
4. Log it: `python fulfillment_tracker.py seed`
5. Creator receives product → films content → posts with Shop link
6. Customer buys → fulfilled through Method 1, 2, or 3 above

**Budget for seeding:** 50 units × $2.50 COGS = $125 to activate 50 creators
That $125 can generate $10,000+ in GMV if even 10% of creators convert.

---

## SUPPLIER → YOU FLOW

When your order arrives from CALLA/Xiran/Blackbird:

1. **Inspect inventory** — count units, check for damage
2. **Photograph product** — for TikTok Shop listing images
3. **Log receipt:** `python fulfillment_tracker.py receive`
4. **Decide split:**
   - Keep 50–100 units at home for seeds + first orders
   - Ship remainder to FBT warehouse (once you're set up)
5. **Create TikTok Shop listing** in Seller Center
6. **Set commission rate** (20–25% recommended)
7. **Begin creator outreach**

---

## UNIT ECONOMICS PER ORDER

Based on PDRN serum at $28 sell price:

| Item | Amount |
|------|--------|
| Sale price | $28.00 |
| TikTok platform fee (6%) | -$1.68 |
| Creator commission (20%) | -$5.60 |
| Product COGS | -$2.50 |
| Shipping (self-fulfill) | -$4.50 |
| FBT fee (if using FBT) | -$4.00 |
| **Net profit (self-ship)** | **$13.72** |
| **Net profit (FBT)** | **$14.22** |
| **Margin** | **~49%** |

At 100 orders/month: **$1,372 net**
At 1,000 orders/month: **$13,720 net**
At 10,000 orders/month: **$137,200 net**

---

## TRACKING COMMANDS

```bash
# See current inventory
python fulfillment_tracker.py inventory

# Log new inventory arriving from supplier
python fulfillment_tracker.py receive

# Ship product to a creator
python fulfillment_tracker.py seed

# Log a customer order
python fulfillment_tracker.py order

# Mark order shipped (with tracking number)
python fulfillment_tracker.py ship

# Full dashboard
python fulfillment_tracker.py dashboard

# Add a supplier
python fulfillment_tracker.py add-supplier
```

---

## SOURCED SUPPLIERS (Ready to contact)

| Supplier | Product | MOQ | Unit Cost | Lead Time | Contact |
|----------|---------|-----|-----------|-----------|---------|
| **CALLA** (Korea) | PDRN Serum 30ml | 2,000 | ~$1.00 | 20–25 days | callaskincare.com |
| **Xiran** (China) | PDRN + Kojic Acid Serum | 1,000 | $2.00–$2.50 | 25–30 days | xiranskincare.com |
| **Blackbird** (China) | PDRN Serum | 500 | ~$3.00 | 20–25 days | web.blackbirdskincare.com |

**Recommended first order:** Samples from all three → test formulas → order 500–1,000 units from winner → seed 50 creators → scale from there.
