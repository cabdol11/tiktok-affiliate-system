# Tool Stack Setup Guide
## Every Tool You Need, How to Set It Up, and How to Use It

---

## TIER 1: DAY 1 TOOLS (Set up before your first post)

### 1. CapCut (Video Editing) — FREE
**Why:** #1 TikTok editing tool, native integration, templates are algorithm-optimized.

**Setup:**
1. Download CapCut from App Store / Google Play / capcut.com (desktop version recommended for speed)
2. Sign in with TikTok account (or create separate account)
3. Enable auto-captions: Settings → Captions → Auto-generate
4. Install these free template packs (search in CapCut Template tab):
   - "Product Review" templates (clean, fast cuts)
   - "Amazon Finds" templates (text overlay style)
   - "Before After" templates (split screen)

**Key features to use:**
- **Auto-captions:** Add captions to every video. Captioned videos get 25% higher watch time.
- **Templates:** For your first 2 weeks, use templates. They're pre-optimized for TikTok format.
- **Beat sync:** Sync cuts to music beats for higher retention
- **Text animations:** Use "trending" text styles visible in the Template section
- **Speed ramp:** Slow down at key product moments, speed up transitions

**CapCut Pro** ($7.99/month): Only needed for removing CapCut watermark on exports. Worth it.

**Workflow:**
- Film all raw footage on phone
- Import to CapCut
- Add auto-captions → edit captions for accuracy
- Add background music (use CapCut's commercial music library — royalty-free)
- Export at 1080p, 60fps for TikTok

---

### 2. TikTok Creator Account — FREE
**Why:** Unlocks analytics, Creator Marketplace, TikTok Shop Affiliate, and scheduling.

**Setup:**
1. If you have a personal TikTok: Settings → Manage Account → Switch to Creator Account
2. If new: Download TikTok → create account → immediately switch to Creator Account
3. Profile setup:
   - Profile photo: Clear face photo (not logo — faces get 30% more follows)
   - Username: Your niche + your name (e.g., @techreviews_sarah, @skincarewithmike)
   - Bio: "[Niche] finds | New drops weekly | Links below ↓" (max 80 chars)
   - Add Beacons.ai link to bio (set up next)
4. Creator tools to enable immediately:
   - Settings → Creator tools → Analytics (turn on)
   - Settings → Creator tools → TikTok Shop → Apply for TikTok Shop Affiliate
   - Settings → Creator tools → LIVE → Enable if you have 1,000+ followers

**TikTok Analytics you should check daily:**
- Overview tab: Followers, likes, views (big picture)
- Content tab: Individual video performance → sort by Watch Time %
- Followers tab: When are your followers online? (set your posting schedule to match)

---

### 3. Beacons.ai (Link-in-Bio) — FREE / Pro $10/month
**Why:** Multi-link hub, affiliate link organizer, email collection, analytics.

**Setup:**
1. Go to beacons.ai → Sign up → Choose Creator plan (free)
2. Claim your URL: beacons.ai/yourname
3. Build your page (this is your affiliate storefront):

**Recommended page structure:**
```
[Profile Photo + Name]
[One-line bio: "I find products that actually work"]

[Block 1] TOP PICKS THIS WEEK (update every Friday)
  → Link to your #1 converting product

[Block 2] EMAIL LIST
  → "Get my weekly finds" → ConvertKit form embed

[Block 3] NICHE CATEGORY PAGES
  → Beauty Favorites
  → Kitchen Gadgets
  → AI Tools
  (Each page has 5-10 affiliate products sorted by price)

[Block 4] AMAZON STOREFRONT
  → Direct link to your Amazon Associates storefront

[Block 5] FOLLOW ME
  → Instagram, YouTube links
```

**Beacons Pro** ($10/month): Removes Beacons branding, enables custom domain, unlocks analytics for each link. Get this by Week 2.

**Analytics to track:** Beacons provides click data per link. Export weekly and log into link_manager.py.

---

### 4. Canva (Graphics + Thumbnails) — FREE / Pro $12.99/month
**Why:** Create scroll-stopping cover images, episode graphics, comparison charts.

**Setup:**
1. canva.com → Sign up (use Google account)
2. Install the TikTok Video template (1080×1920) as your default
3. Create your brand kit (free with Canva):
   - Primary color: Choose 1-2 brand colors
   - Font: 1 display font (for hooks) + 1 body font (for captions)
   - Save as "My Brand Kit"

**Templates to create and save:**
- **Hook text overlay:** Large, bold text on colored background for first 3 seconds
- **"VS" comparison card:** Side-by-side comparison for product comparisons
- **Price tag graphic:** "$29 vs $129 — same results?" format
- **Review stars:** 5-star rating card for unboxing videos
- **"Sponsored/Affiliate" disclosure badge:** Save this — add to every video thumbnail

**Canva Pro** ($12.99/month): Unlocks background remover, Magic Resize (resize one design to all formats), brand kit across all designs. Get this at Week 4.

---

## TIER 2: WEEK 2 TOOLS

### 5. ConvertKit (Email Marketing) — FREE up to 1,000 subscribers / $29+/month
**Why:** Best deliverability for creator audiences, visual automation builder, integrates with Beacons.ai.

**Setup:**
1. convertkit.com → Sign up (free up to 1,000 subscribers)
2. Create your first form: "Get My Weekly Product Finds"
   - Form type: Inline (embed in Beacons.ai)
   - Success message: "Check your email — I just sent you my top 3 picks"
3. Create welcome sequence:
   - Email 1 (immediate): Subject: "Here's what I use every day"
     - Your top 3 affiliate products + links
     - Include UTM parameters: `?utm_source=email&utm_medium=welcome&utm_campaign=welcome_seq`
   - Email 2 (Day 3): Subject: "I tested this so you don't have to"
     - One product deep-dive review
   - Email 3 (Day 7): Subject: "My favorite finds this week"
     - Weekly format you'll maintain forever
4. Connect to Beacons.ai: Beacons → Integrations → ConvertKit → Add API key

**Weekly broadcast setup:**
- Every Sunday, write your weekly "Top Finds" email
- 3-5 products, each with your affiliate link
- Subject line formula: "[Number] things worth buying this week" or "What I found this week"

---

### 6. Notion (Content Planning Dashboard) — FREE
**Why:** Your command center. Tracks content ideas, posting schedule, product research notes.

**Setup:**
1. notion.so → Sign up (free personal plan)
2. Create a workspace: "TikTok Affiliate HQ"
3. Create these databases:

**Content Ideas Database (Kanban view):**
```
Columns: Idea | In Production | Posted | Analyzing
Properties: Product, Framework, Estimated Commission, Hook
```

**Product Research Database (Table view):**
```
Columns: Product | Network | Commission | Score | Status | Notes
(Sync with product_research.py data manually weekly)
```

**Weekly Goals Tracker:**
```
Week | Sales Goal | Actual | Net Profit Goal | Actual | Key Learnings
```

**Download Notion mobile app:** Add video ideas on the go (you'll have ideas while shopping, etc.)

---

### 7. VidIQ (TikTok Analytics) — FREE / Pro $16.58/month
**Why:** Competitor analytics, trending hashtag research, keyword volume on TikTok.

**Setup:**
1. vidiq.com → Sign up → Connect TikTok account
2. Install Chrome extension for desktop research
3. Use "Keywords" tab to research TikTok search volume for your niche
4. Use "Competitors" tab to see what's working for top creators in your niche

**Key features:**
- **Trending topics:** See what's trending in your niche before it peaks
- **Best time to post:** Personalized to your follower timezone (more accurate than general guides)
- **Keyword research:** Find high-volume, low-competition search terms to include in captions

**VidIQ Pro** ($16.58/month): Unlocks competitor deep-dives, AI-powered title/hook suggestions, trend alerts. Worth it at Week 4.

---

## TIER 3: WEEKS 4–8 TOOLS

### 8. TikTok Creator Marketplace
**Why:** Brand deal layer on top of affiliate income. Brands pay $200-$5,000+ per video.

**Eligibility:** 10,000+ followers, 100,000 video views in last 30 days.

**Setup:**
1. TikTok app → Creator tools → Creator Marketplace → Apply
2. Complete profile: niche, audience demographics, past brand work
3. Set your rates:
   - 10K-50K followers: $200-$500/video
   - 50K-200K: $500-$2,000/video
   - 200K-1M: $2,000-$8,000/video

**Stack brand deals ON TOP of affiliate:**
- Negotiate to include your own affiliate link in sponsored posts (many brands allow this)
- Get paid $500 for the post PLUS earn commissions on every sale
- This doubles or triples your income per video

**How to get brand deals without waiting:**
- Email brands directly: "I reach [X] targeted buyers in your niche. My audience purchased $[X] in products this month."
- Use affiliate performance data as proof (screenshot from affiliate_tracker.py)

---

### 9. TikTok Ads Manager (Paid Phase) — Pay-per-use
**Why:** Spark Ads to boost organic content, Video Shopping Ads for TikTok Shop.

**Setup:**
1. ads.tiktok.com → Sign up for Business Account
2. Connect your TikTok Creator account
3. Install TikTok Pixel:
   - Ads Manager → Assets → Events → Web Events → Add manually
   - Copy pixel code → paste into Beacons.ai custom code section
   - Set up events: PageView, Lead (email signup), Purchase (if possible)
4. Add payment method (credit card — use a business card for expense tracking)

**First campaign setup — see scaling_playbook.md Week 5 for full details.**

---

## TIER 4: SCALE PHASE TOOLS (Week 9+)

### 10. RedTrack (Advanced Affiliate Tracking) — $149/month
**Why:** At scale, you need pixel-level tracking across networks. RedTrack does this.

**When to start:** When you're spending $1,000+/week on ads or managing 20+ affiliate products.

**What it replaces:** Manual logging in affiliate_tracker.py (automates click/conversion tracking)

**Setup (high-level):**
1. redtrack.io → Sign up → Business plan
2. Create a "Campaign" for each affiliate product
3. Add traffic source (TikTok Ads)
4. Add offer (your affiliate link with RedTrack's tracking parameters)
5. Generate RedTrack tracking link → use this instead of raw affiliate link
6. RedTrack automatically logs clicks, conversions, and calculates EPC/ROAS

**Key features:**
- Multi-touch attribution (which video → which click → which sale, even across days)
- S2S postback integration with affiliate networks (no pixel fires needed)
- Automatic UTM parameter injection
- Bot traffic filtering (protects your accounts from invalid clicks)

---

### 11. Voluum (Alternative to RedTrack) — $199/month
**Same use case as RedTrack.** Voluum is older, more established. RedTrack is newer, better UX.

**Choose RedTrack** if you're starting out. **Choose Voluum** if you're running $5K+/day in ad spend.

---

## TOOL COST SUMMARY

| Tool | Monthly Cost | Start Week |
|------|-------------|-----------|
| CapCut Pro | $7.99 | Week 1 |
| TikTok Creator | Free | Day 1 |
| Beacons.ai | Free → $10 | Week 2 |
| Canva | Free → $12.99 | Week 4 |
| ConvertKit | Free → $29 | Week 2 |
| Notion | Free | Week 1 |
| VidIQ | Free → $16.58 | Week 4 |
| TikTok Ads Manager | Pay-per-use | Week 5 |
| RedTrack | $149 | Week 9 |
| **Total (Weeks 1-4)** | **~$8/month** | |
| **Total (Weeks 5-8)** | **~$80/month + ad spend** | |
| **Total (Weeks 9+)** | **~$230/month + ad spend** | |
