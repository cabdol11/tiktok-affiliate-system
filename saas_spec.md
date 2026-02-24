# TikTok Shop OS — Product Specification
## What we're building. What it does. How it makes money.

---

## PRODUCT VISION

TikTok Shop OS is the operating system for brands running affiliate programs on TikTok Shop.

Every brand that wants to scale past $100K/month GMV on TikTok Shop needs:
1. A systematic way to find and recruit creators
2. A way to track who is performing and who isn't
3. Automated commission management
4. Performance analytics that tell them what to double down on

We built this for ourselves. Now we sell access to it.

**Comparable:** Klaviyo for email marketing. Gorgias for customer support. We are the Klaviyo for TikTok Shop affiliate management.

---

## CORE MODULES

### Module 1 — Creator Intelligence

**What it does:**
- Database of 500K+ TikTok creators, filterable by niche, follower count, engagement rate, CVR history
- CVR scoring: estimated conversion rate based on past Shop-tagged content performance
- Niche matching: suggest top 50 creators for any product category automatically
- Contact data: TikTok handle, email (where available), DM-ready templates

**Data sources:** TikTok Creator Marketplace API, proprietary performance data from managed campaigns, third-party enrichment

**Key metric:** Time-to-first-creator-contact reduced from 2 weeks to 2 hours

---

### Module 2 — Outreach Automation

**What it does:**
- Send personalized DM/email sequences to creator lists at scale
- Track opens, replies, and conversion per sequence
- A/B test message variants
- Auto-follow-up on no-reply after configurable interval
- Log all communications per creator

**Key metric:** Creator reply rate benchmark: 15–25% (vs industry manual DM average of 3–5%)

---

### Module 3 — Campaign Management

**What it does:**
- Create campaigns per product/SKU
- Assign creators to campaigns
- Track: videos posted, views, clicks, add-to-cart, GMV, commission earned
- Content calendar: schedule posting dates, send reminders to creators
- Product seeding tracker: who received samples, when, confirmation

**Key metric:** Creator activation rate (invited → posted content) target: 60%+

---

### Module 4 — Commission Management

**What it does:**
- Sync with TikTok Shop Seller Center API to pull live commission data
- Leaderboard: top creators by GMV, CVR, content volume
- Tiered commission automation: auto-increase commission for top performers
- Payout tracking: who is owed what, when paid
- Dispute resolution log

**Key metric:** Commission accuracy rate: 99.9%

---

### Module 5 — Performance Analytics

**What it does:**
- GMV dashboard: today / 7d / 30d / all-time
- Creator performance heatmap: who drives the most GMV, at what CVR
- Content performance: which video formats convert best for each product
- Cohort analysis: creator retention month over month
- Attribution: first-touch vs last-touch GMV credit
- Weekly automated report (PDF) delivered to brand contact

**Key metric:** Brands using analytics module increase GMV 40% faster than those who don't

---

### Module 6 — Product Intelligence

**What it does:**
- ICE scoring for any TikTok Shop product (Impact × Confidence × Ease)
- Trending ingredient/category alerts (when a search term spikes 200%+)
- Competitor analysis: what products similar brands are running through affiliates
- Price elasticity modeling: what commission rate maximizes creator adoption

**Key metric:** Product-to-first-$10K-GMV timeline reduced by 60%

---

## PRICING TIERS

| Tier | Price | Includes | Target |
|------|-------|----------|--------|
| **Starter** | $299/month | 1 brand, 100 creators, basic analytics | Brands doing <$50K GMV |
| **Growth** | $599/month | 3 brands, 500 creators, full analytics, outreach automation | Brands doing $50K–$200K GMV |
| **Scale** | $999/month | Unlimited brands, 2,000+ creators, all modules, API access | Brands doing $200K+ GMV |
| **Enterprise** | Custom | Dedicated support, custom integrations, white-label option | Agencies, large brands |

**Annual discount:** 20% off (2 months free)

---

## REVENUE MODEL

**Year 1 targets:**

| Month | Paying Brands | MRR | ARR Run Rate |
|-------|--------------|-----|-------------|
| 3 | 10 | $6K | $72K |
| 6 | 50 | $30K | $360K |
| 9 | 150 | $90K | $1.1M |
| 12 | 400 | $240K | $2.9M |
| 18 | 1,200 | $720K | $8.6M |
| 24 | 3,000 | $1.8M | $21.6M |

**Assumption:** Average revenue per account (ARPA) = $600/month (blended across tiers)

---

## BUILD ROADMAP

### Phase 1 — MVP (Months 1–3)
**Ship:** Creator database (manual-curated, 10K records) + campaign tracker + basic analytics dashboard
**Stack:** Python backend, SQLite → Postgres, React or simple HTML frontend
**Distribution:** 10 beta brands from managed client base, free access
**Goal:** Prove the tool reduces time-to-GMV by 50%+

### Phase 2 — Growth (Months 3–6)
**Ship:** Outreach automation, TikTok Shop Seller Center sync, commission module
**Distribution:** Convert beta users to paid, begin inbound from content
**Goal:** $30K MRR, <5% monthly churn

### Phase 3 — Scale (Months 6–12)
**Ship:** AI product intelligence, creator CVR scoring, automated reporting
**Distribution:** Shopify App Store listing, TikTok Agency Partner Program
**Goal:** $240K MRR, 400 paying brands

### Phase 4 — Platform (Months 12–24)
**Ship:** API for enterprise, white-label for agencies, creator-side app
**Distribution:** Agency reseller channel, TikTok direct partnership
**Goal:** $1.8M MRR, 3,000 brands

---

## MOAT

The platform gets stronger with every brand added:

1. **Data moat:** More campaigns = better CVR scoring = better creator recommendations
2. **Network moat:** Every brand brings their creators into the shared database
3. **Relationship moat:** Creators who perform for one brand on the platform are warm for others
4. **Switching cost:** Once a brand's creator network, history, and analytics are in the system, they don't leave

---

## COMPETITIVE LANDSCAPE

| Competitor | Weakness | Our Advantage |
|------------|----------|---------------|
| GrowMojo (agency) | Service model only, no software | We have both managed + SaaS |
| Creator.co | Generic influencer platform, not TikTok Shop-specific | Built exclusively for TikTok Shop |
| TikTok Creator Marketplace | Owned by TikTok, no affiliate mgmt | We sit above it, adding the operations layer |
| Shopify Collabs | Shopify-centric, not TikTok-native | Natively TikTok Shop, not bolted on |
| Manual spreadsheets | 99% of brands today | Anything beats a spreadsheet |

---

## THE DISTRIBUTION UNFAIR ADVANTAGE

We are not starting from zero. We have:
1. Our own brand generating real GMV — proof the system works
2. Managed client case studies — social proof
3. Active creator network — immediate value for Day 1 SaaS customers
4. Content on TikTok and LinkedIn showing results — inbound pipeline

No competitor has all four. That is the moat at launch.

---

## SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Time-to-first-GMV for new brands | <14 days |
| Monthly churn rate | <3% |
| Net revenue retention (NRR) | >120% |
| Creator activation rate | >60% |
| Brand NPS | >50 |
| CAC payback period | <3 months |
