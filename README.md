# TikTok Affiliate Marketing System
### Target: $10,000 Net Profit Per Week

A complete, production-ready affiliate marketing system for TikTok creators — from niche selection and content production through automation, paid scaling, and financial tracking.

---

## SYSTEM OVERVIEW

```
tiktok-affiliate-system/
├── README.md                 ← You are here — master guide + Day 1 checklist
├── business_plan.md          ← Niche selection, profit math, affiliate networks, legal
├── content_system.md         ← 30-day calendar, 10 video frameworks, 50 hooks, CTAs
├── scaling_playbook.md       ← Organic → Spark Ads → Full paid + creator network
├── tool_stack.md             ← Every tool, setup instructions, costs
├── weekly_sop.md             ← Exact day-by-day operating procedures
│
├── content_scheduler.py      ← Content queue, posting schedule, performance tracking
├── affiliate_tracker.py      ← Multi-network revenue tracking, P&L, CVR alerts
├── product_research.py       ← Product scoring, competitor tracking, top 10 weekly
├── link_manager.py           ← UTM links, A/B testing, video-to-sale attribution
├── financials.py             ← Weekly P&L, $10K projection, ad break-even calc
│
├── requirements.txt          ← Python dependencies (core system: zero installs needed)
└── data/                     ← Auto-created — JSON data files for all scripts
```

**All Python scripts use only the standard library. No pip install required to run the core system.**

---

## DAY 1: EXACT FIRST STEPS

Complete these in order. Budget: 4-6 hours total.

### Step 1: Choose Your Niche (30 min)
Open `business_plan.md` → Section 2 (Top 5 Niches).

Use the scoring framework to pick **one niche**. Do not hedge with multiple niches on Day 1.

**Recommended for most beginners:**
- If you're comfortable on camera and buy beauty/skincare products: → **Beauty & Skincare**
- If you're into fitness: → **Fitness & Supplements**
- If you're tech-oriented: → **AI Tools** (highest CVR, lowest competition in sub-niches)
- If you have pets: → **Pet Products** (easiest authenticity)

---

### Step 2: Set Up Your TikTok Creator Account (20 min)
1. Create or convert your TikTok to a Creator Account
2. Optimize profile: clear face photo, niche-specific username, bio with Beacons.ai link
3. Turn on TikTok Analytics (Settings → Creator Tools → Analytics)

---

### Step 3: Join Your First Affiliate Networks (1 hour)
Sign up in this order:

1. **TikTok Shop Affiliate** — seller.tiktok.com (highest priority, highest CVR)
2. **Amazon Associates** — affiliate-program.amazon.com
3. **ClickBank** — clickbank.com (instant approval)

Do NOT join all networks at once. Get these three working first.

---

### Step 4: Set Up Beacons.ai (30 min)
1. beacons.ai → create account → claim `beacons.ai/yourname`
2. Add your TikTok Shop favorites, Amazon products, ClickBank offers
3. Add ConvertKit email form (sign up at convertkit.com first)
4. Add your TikTok link to this bio page

---

### Step 5: Run the System Scripts (30 min)
```bash
# Navigate to project folder
cd tiktok-affiliate-system

# Create your data directory (auto-created on first run, but confirm it works)
python3 affiliate_tracker.py dashboard

# Add your first affiliate products
python3 product_research.py add   # Add 3-5 products from your chosen niche
python3 product_research.py top10  # See your first ranked list

# Create your first tracked links
python3 link_manager.py create    # For each of your top 3 products
python3 link_manager.py list      # Confirm links are created
```

---

### Step 6: Plan Week 1 Content (1 hour)
Open `content_system.md` → Section 2 (30-Day Calendar) → Copy Week 1 into Notion.

Assign your top 3 products to the calendar:
- Primary product: appears in 50% of posts (your highest-scored product from Step 5)
- Secondary products: fill remaining slots

Pick your first 3 hooks from the Hook Library (Section 4 of `content_system.md`).

---

### Step 7: Film Your First 3 Videos (2 hours)
Framework for your very first video: **Framework 4 — Unboxing + Honest Review**

Why: It's authentic, easy to film, and performs well even with 0 followers.

Script template:
```
[0-3s] "Okay I just got [product] and I need to show you this"
[3-15s] Show unboxing, first impressions
[15-35s] Test it on camera — be genuine
[35-55s] Honest verdict — what you liked, what you didn't
[55-65s] "If you want to try it, it's linked in my bio"
[Disclosure in caption: #affiliate]
```

Post all 3 videos today (morning, afternoon, evening posting windows).

---

### Step 8: Post and Engage (ongoing from Day 1)
After each video posts:
- Stay on the video for 30 minutes
- Reply to every comment
- Check back every 2 hours for new comments on your first day

---

## 90-DAY ROADMAP TO $10K/WEEK

### Phase 1: Weeks 1–4 (Organic Foundation)
**Daily time:** 4-5 hours
**Posting:** 3-5 videos/day
**Goal:** 50-100 sales/week by Week 4

| Week | Focus | Target Sales/Week | Target Net |
|------|-------|------------------|-----------|
| 1 | Post consistently, test formats | 0-3 | $0-$225 |
| 2 | Double down on winning framework | 5-10 | $375-$750 |
| 3 | Product rotation + offer testing | 10-20 | $750-$1,500 |
| 4 | Batch system + first creator outreach | 20-35 | $1,500-$2,625 |

**Week 4 checkpoint:**
- [ ] Follower count: 500-2,000+
- [ ] Identified top 2 converting products
- [ ] Email list: 25-50 subscribers
- [ ] Earning $500-$2,500/week gross

---

### Phase 2: Weeks 5–8 (Spark Ads + Amplification)
**Daily time:** 3-4 hours
**Ad spend:** $200-500/week
**Goal:** 150-200 sales/week by Week 8

| Week | Focus | Target Sales/Week | Target Net |
|------|-------|------------------|-----------|
| 5 | First Spark Ad ($20/day) | 50-70 | $2,500-$3,500 |
| 6 | Optimize + scale winning ad | 80-100 | $4,000-$5,000 |
| 7 | TikTok Shop + Spark combo | 100-130 | $4,500-$5,500 |
| 8 | Creator network pilot (1-2 creators) | 150-200 | $5,500-$7,500 |

**Week 8 checkpoint:**
- [ ] Follower count: 5,000-15,000+
- [ ] Spark Ads running profitably (ROAS > 2.5x)
- [ ] Email list: 200+ subscribers
- [ ] First sub-creator posting content
- [ ] Earning $5,000-$7,500/week net

---

### Phase 3: Weeks 9–12 (Full Paid System + Creator Network)
**Daily time:** 2-3 hours (systems doing more)
**Ad spend:** $1,000-3,000/week
**Goal:** 300+ sales/week by Week 12

| Week | Focus | Target Sales/Week | Target Net |
|------|-------|------------------|-----------|
| 9 | Full TikTok Ads campaign build | 200-250 | $7,000-$8,500 |
| 10 | Email/SMS monetization + retargeting | 250-280 | $8,000-$9,000 |
| 11 | Multi-platform (Reels + Shorts) | 280-300 | $8,500-$9,500 |
| 12 | Rate negotiation + creator team at 3 | 300-350 | $9,000-$10,500 |

**Week 12 checkpoint:**
- [ ] Follower count: 20,000-50,000+
- [ ] Paid ads running at ROAS > 3x
- [ ] Email list: 500+ subscribers
- [ ] 3+ creators in your network
- [ ] Earning $9,000-$10,500/week net

---

### Phase 4: Weeks 13–20 (Consolidate + Systematize)
**Daily time:** 1-2 hours (creator network handles production)
**Goal:** Consistent $10,000+ net/week

Key actions:
- Scale creator network to 5-7 creators
- Renegotiate all affiliate rates where you've hit volume thresholds
- Add Pinterest and email monetization as passive income layers
- Consider hiring a VA ($500-800/month) to manage comment engagement and creator payouts

---

## REALISTIC MILESTONE TIMELINE

| Milestone | Week | Weekly Net | What Gets You There |
|-----------|------|-----------|---------------------|
| First sale | 2 | $75-$150 | First video to 5,000+ views that sends traffic |
| Consistent income | 4 | $500-$2,500 | 3-5 videos/day system, top product identified |
| Quit job threshold | 8 | $2,500-$5,000 | Spark Ads profitable, first creators added |
| Six-figure annual rate | 12 | $5,000-$10,000 | Full paid system + creator network of 3 |
| $10K/week net | 20 | $10,000+ | Creator network of 5-7 + paid ads + email |

**Important note on the timeline:** These projections assume:
- 3-5 posts/day (consistent volume)
- You engage with comments within 30 minutes of every post
- You run the product research and analytics review weekly (data-driven iteration)
- You don't quit during weeks 2-3 when results are slow

The biggest variable is your starting audience. With 0 followers, expect a 2-4 week "warming up" period. With an existing audience of 5,000+, you could hit $500/week by Week 1.

---

## QUICK REFERENCE: DAILY CHECKLIST

**Morning (6-9 AM):**
- [ ] Post Video 1
- [ ] Engage with comments for 30 min after posting
- [ ] Check previous night's video analytics

**Midday (12-2 PM):**
- [ ] Post Video 2
- [ ] Engage with comments for 30 min
- [ ] Respond to any DMs (link requests)

**Evening (7-10 PM):**
- [ ] Post Video 3 (your best content of the day)
- [ ] Engage with comments for 30 min
- [ ] Quick analytics check: Is anything spiking?

**Friday only:**
- [ ] `python3 affiliate_tracker.py report`
- [ ] `python3 financials.py log-week` then `dashboard`
- [ ] `python3 content_scheduler.py report`
- [ ] `python3 link_manager.py top`
- [ ] Write 1-sentence learnings, update next week's plan

---

## EMERGENCY TROUBLESHOOTING

**"My videos are getting 200 views maximum"**
- Problem: You're shadowbanned or your niche/hook isn't resonating
- Solution 1: Check if any video has a community guideline strike (TikTok app → inbox → system notifications)
- Solution 2: Post a completely different hook style for 5 days straight
- Solution 3: Create a fresh account (if violations are the cause)
- Don't: Keep posting the same format hoping it changes

**"I'm getting views but zero link clicks"**
- Problem: Your CTA is weak or your link-in-bio is not set up correctly
- Solution 1: Test explicitly saying "IT'S IN MY BIO" verbally (many viewers don't know how TikTok bio links work)
- Solution 2: Add a screen recording showing how to click the link (5-second clip at the end)
- Solution 3: Use comment engagement: "Comment LINK and I'll reply with the direct link"

**"Lots of link clicks but zero conversions"**
- Problem: Wrong product for your audience, OR landing page friction
- Solution 1: Check if your Beacons.ai link actually works (test it yourself, incognito)
- Solution 2: Switch to TikTok Shop products (in-app checkout removes all friction)
- Solution 3: Check product price vs your audience's spending power (too expensive?)
- Solution 4: `python3 affiliate_tracker.py health` — check which product to cut

**"Ad spend not converting (ROAS below 1)"**
- Problem: Wrong creative, wrong audience, wrong product for paid traffic
- Solution 1: Kill the ad immediately (don't let it run hoping it improves)
- Solution 2: Only boost videos that are ALREADY converting organically (don't try to make failing content win with ads)
- Solution 3: Start over at $10/day and narrow the audience to your proven demographic

---

## LEGAL REMINDERS (Read Before Your First Post)

1. **Add #affiliate to every caption** — Required by FTC. Not optional.
2. **Form your LLC** — Before you reach $1,000/month in revenue
3. **Open a business bank account** — Keep business income separate from day 1
4. **Set aside 25-30% of every payment for taxes**
5. **Do not make income claims** ("I made $10K with this") without being the creator who actually made it — FTC violation

Full legal checklist: see `business_plan.md` → Section 5.

---

## GETTING HELP

If you're stuck, check in this order:
1. `weekly_sop.md` — Your exact protocol for every situation
2. `scaling_playbook.md` — Which phase are you in? What should you focus on?
3. `content_system.md` — Framework and hook library for content blocks
4. `business_plan.md` → Section 3 — Profit math (are your numbers realistic for your current stage?)

**Run a full system diagnostic:**
```bash
python3 product_research.py top10       # Am I promoting the right products?
python3 affiliate_tracker.py dashboard  # Where is revenue coming from?
python3 affiliate_tracker.py health     # What needs to be cut?
python3 link_manager.py top             # What's actually converting?
python3 financials.py dashboard         # Am I on track?
python3 financials.py project           # Updated $10K timeline
```
