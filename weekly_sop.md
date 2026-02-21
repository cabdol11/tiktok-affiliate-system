# Weekly Standard Operating Procedure
## Your Exact Weekly Workflow to Hit $10K/Week Net

---

## OVERVIEW

**Total weekly time commitment:**
- Weeks 1-4 (building phase): 4-5 hours/day
- Weeks 5-8 (optimizing phase): 3-4 hours/day
- Weeks 9-12 (scaling phase): 2-3 hours/day (systems do more work)
- Week 20+ (mature phase): 1-2 hours/day (creator network handles most production)

**Weekly time breakdown:**
| Day | Activity | Time |
|-----|----------|------|
| Monday | Planning + Research | 2-3 hours |
| Tuesday | Content creation + posting | 3-4 hours |
| Wednesday | Content creation + posting | 3-4 hours |
| Thursday | Content creation + posting | 3-4 hours |
| Friday | Analytics review + optimization | 2-3 hours |
| Saturday | Content creation + posting | 3-4 hours |
| Sunday | Batch filming + email newsletter | 3-4 hours |

**Daily recurring tasks (every day, 30-45 min):**
- Post scheduled videos
- Engage with comments for first 30 minutes after each post
- Check analytics for previous day's videos

---

## MONDAY: PRODUCT RESEARCH + CONTENT PLANNING (2-3 hours)

### 8:00 AM – Product Research (1 hour)

**Step 1: TikTok Creative Center (15 min)**
- Go to ads.tiktok.com/business/creativecenter → "Trending Products"
- Filter by: Your niche, last 7 days, sort by "Sales volume"
- Note top 5 products with sales velocity increasing (not just total)
- Screenshot for product_research.py entry

**Step 2: Competitor Check (15 min)**
- Open your tracked competitor list (from product_research.py → competitor)
- Check their last 7 days of content: What products are they pushing?
- Videos with 500K+ views in last 48 hours → note the product, the framework used
- If a competitor is promoting something heavily, it's converting for them

**Step 3: Amazon Best Sellers (10 min)**
- amazon.com/best-sellers → Navigate to your niche subcategory
- Note any items that jumped from top 50 → top 10 in the last week (use Keepa browser extension to track movement)
- Cross-reference: Is this on TikTok Creative Center trending too? If yes, it's a priority

**Step 4: Google Trends (5 min)**
- trends.google.com → search your niche product keywords
- Filter: Last 30 days, United States
- Rising searches = opportunity. Peaked searches = late to the party

**Step 5: Log into product_research.py**
```bash
python product_research.py add
```
Add any new products discovered. Run `top10` command to see this week's prioritized list.

---

### 9:00 AM – Content Planning (1 hour)

**Step 1: Review last week's analytics (20 min)**
- TikTok Analytics → Content → Sort by Watch Time %
- Identify your top 3 videos by watch time AND by link-in-bio visit rate (these may differ)
- Answer: Which framework drove the most profile visits? → Post 2 more of that format this week

**Step 2: Build this week's content calendar in Notion (20 min)**

Fill in your weekly calendar (use Week 2+ template from content_system.md):
```
Tuesday:
  Post 1 (7AM): [Product] — [Framework] — Hook: "[chosen hook from library]"
  Post 2 (1PM): [Product] — [Framework] — Hook: "[chosen hook]"
  Post 3 (8PM): [Product] — [Framework] — Hook: "[chosen hook]"

Wednesday: [same format]
...
```

**Step 3: Select this week's priority products (20 min)**

Run in terminal:
```bash
python product_research.py top10
python affiliate_tracker.py health  # check for any CVR alerts
```

From the output, choose:
- 1 primary product (highest composite score, your main focus this week)
- 2 secondary products (rotate in for variety)
- 1 "evergreen" product (always performs, lower commission but reliable)

---

### 10:00 AM – Link & Technical Setup (30 min)

**Create any new tracked links:**
```bash
python link_manager.py create   # For each new product you're featuring this week
```

**Update Beacons.ai:**
- Log in to beacons.ai → Update "TOP PICKS THIS WEEK" block with this week's primary product
- Move last week's top pick to the relevant category page
- Ensure all links are active (test every link by clicking)

**Schedule A/B test if applicable:**
```bash
python link_manager.py ab-test  # Create test for any product you want to optimize
```

---

## TUESDAY – THURSDAY: CONTENT CREATION + POSTING (3-4 hours/day)

### Morning Block (6:00–9:00 AM)

**6:00 AM – Film Morning Video**

Before filming, prep:
- [ ] Product laid out/set up for demo
- [ ] Good lighting (ring light or window light, natural preferred)
- [ ] Clean background (solid color or organized aesthetic background)
- [ ] Hook cue card ready (write your exact first 3 seconds on paper)

Film your morning video (6:30 AM target):
1. Film 3-5 takes of the hook (first 3 seconds — this is the most important part)
2. Film the main content (product demo, results, review)
3. Film your CTA outro ("Link in my bio, it's the first thing")
4. Film any B-roll: close-ups of the product, packaging, results

**7:00 AM – Edit in CapCut**
1. Import all clips
2. Trim: Remove dead space at start and end of each clip
3. Add captions: CapCut → Text → Auto-captions → Review and fix errors
4. Add background music: CapCut's commercial library → sort by "Trending"
5. Add any text overlays (hook text, key benefit callouts)
6. Export: 1080p, 60fps, no CapCut watermark (CapCut Pro)

**7:30 AM – Post Video #1**
- Open TikTok → + → Upload
- Write caption using Caption Template from content_system.md
- Add 8-12 hashtags (rotate between your 3 hashtag sets)
- Add TikTok Shop product tag if applicable
- Schedule or post immediately
- **Set a timer for 30 minutes — stay on the app and reply to every comment**

**Comment engagement (7:30–8:00 AM):**
Comments that deserve full replies:
- "Where is the link?" → Reply with "[Product name] is in my bio, first link!"
- "Does this actually work?" → Give a genuine 1-2 sentence answer + "Tried it for X weeks"
- "Price?" → Reply with current price + "Linked in bio"
- "I have [similar problem], would this work?" → Personalized answer

Comments that deserve emoji replies:
- Generic positive comments → ❤️ or ✅

Comments you should pin:
- If someone says "I bought it and it's amazing" → Pin this. Social proof on your video boosts CVR.

---

### Afternoon Block (12:00–2:00 PM)

**12:00 PM – Film & Edit Video #2**
- Similar workflow to morning
- Different framework than morning video (variety signals quality to algorithm)
- Can be shorter (15-30 seconds) — short-form punchy content fills the lunchtime slot well

**12:30 PM – Post Video #2**
- Same posting workflow
- Respond to morning video comments that came in since 8 AM (10-15 min)

---

### Evening Block (7:00–9:00 PM)

**7:00 PM – Film & Edit Video #3 (Prime Time Post)**
- Prime time slot = highest viewership, post your best content here
- If you batch-filmed on Sunday, edit and post your best Sunday footage now
- If not batch-filmed, create your most polished video of the day

**7:30 PM – Post Video #3**
- 30-minute comment engagement window (7:30–8:00 PM)
- This is your most important engagement window of the day

**8:00 PM – Optional Video #4 (Weeks 3+ when you have content volume)**
- Re-post a slightly modified version of a video that performed well 7-10 days ago
- Change the hook text overlay only (same underlying video, different opening line)
- Many creators see 30-50% of viral views from "second wind" reposts

---

## FRIDAY: ANALYTICS REVIEW + OPTIMIZATION (2-3 hours)

### Weekly Analytics Review Checklist

**Step 1: TikTok Analytics Deep Dive (45 min)**
- [ ] Overall metrics: Follower count change, total views, total profile visits this week
- [ ] Content analysis: Sort this week's videos by "Video views" AND by "Watched full video"
- [ ] Identify your top 3 videos (by each metric)
- [ ] Identify your bottom 3 videos — what framework/hook/product?
- [ ] Write one sentence learning: "This week, [framework] outperformed [other framework] because [reason]"

**Step 2: Affiliate Performance Review (30 min)**
```bash
python affiliate_tracker.py report     # P&L report
python affiliate_tracker.py health     # CVR alerts
python affiliate_tracker.py dashboard  # Full view
```

Review:
- Which product earned the most this week?
- Which product got the most clicks but fewest sales? (low CVR → swap product or landing page)
- Any products with 50+ clicks and CVR < 2%? → Kill or A/B test

**Step 3: Link Manager Review (15 min)**
```bash
python link_manager.py top     # Top links by EPC
python link_manager.py dashboard
```

Review:
- Which link generated the most revenue?
- Is your A/B test showing a winner yet? (need 20+ clicks per variant)
- Any links with high clicks but zero conversions? → Check if link is broken

**Step 4: Financial Logging (15 min)**
```bash
python financials.py log-week
```
Log this week's numbers. Then run:
```bash
python financials.py dashboard
python financials.py project   # How many weeks to $10K?
```

**Step 5: Content Scheduler Logging (15 min)**
```bash
python content_scheduler.py log    # Update metrics for this week's videos
python content_scheduler.py report # Weekly content performance
```

**Step 6: Next Week Adjustments (30 min)**
Based on the data:
- Increase posts of the top-performing framework by 1/day
- Reduce posts of the worst-performing framework
- Update product priority in Notion for Monday's planning
- Write down 3 new content ideas that occurred to you this week

---

## SATURDAY: CONTENT CREATION + POSTING (3-4 hours)

Same structure as Tuesday-Thursday.

**Saturday-specific content:**
- Weekend audience is more relaxed, browsing for entertainment
- "Week's favorites" roundup content performs well (list format, 5-7 products)
- "What I ordered this week" unboxing (casual, authentic energy)
- "Watch me get ready" / lifestyle content with product integration

---

## SUNDAY: BATCH FILMING + EMAIL NEWSLETTER (3-4 hours)

### 10:00 AM – Batch Filming Session (2 hours)

**Prep (15 min):**
- [ ] Set up filming area with good lighting
- [ ] Gather all products you'll feature this week
- [ ] Print your content calendar for the week
- [ ] Phone charged to 100%, storage cleared

**Filming order (most efficient):**
1. Film all videos with the same background/setup first
2. Then move to different background for variety
3. Film hooks separately from main content (lets you mix and match later)

**Target: Film 8-10 raw videos in 2 hours**
- 2 minutes per setup, 3-4 takes each = ~15 minutes per video
- You won't use all 10, but having extras prevents "I have nothing to post" days

**Batch edit on Sunday evening (optional):**
- Edit 3-4 videos at once in CapCut
- Schedule via TikTok's built-in scheduler for Monday-Wednesday posting
- Frees up weekday mornings for engagement and research instead of filming

---

### 12:00 PM – Weekly Email Newsletter (1 hour)

**Template for your weekly email:**
```
Subject: My top [#] finds this week (including one I can't stop using)

Hey [First Name],

[1 sentence about what you've been testing/doing this week — keeps it personal]

Here's what actually caught my eye:

1. [Product Name] — $[price]
[2-3 sentences: what it is, what you liked, specific result]
[Your affiliate link with UTM tracking]

2. [Product Name] — $[price]
[2-3 sentences]
[Your affiliate link]

3. [Product Name] — $[price] ← (this one is my favorite this week)
[2-3 sentences — save your best for last]
[Your affiliate link]

Quick tip: [One actionable tip related to your niche — builds authority]

Talk soon,
[Your name]

P.S. [Soft CTA — "Reply and tell me what you're looking for, I'll find it"]
```

**Email writing tips:**
- Subject lines with a number outperform by 25%
- "I can't stop using" language is consistently the highest-open framing
- Keep emails under 300 words — mobile readers scroll fast
- The P.S. often gets read before the body — use it for your best CTA

---

## DAILY HABITS (Non-Negotiable — Do Every Single Day)

### Morning (5 min before posting)
- [ ] Check: What are trending sounds in your niche right now? (search in TikTok Discover)
- [ ] Check: Any viral posts in your niche in last 12 hours to potentially duet/stitch?

### After Each Post (30 min)
- [ ] Stay on the video, refresh, reply to every comment
- [ ] Like comments that add value (they'll get notified and may re-engage)
- [ ] If a comment says "link?" — reply AND add that same person with a direct message (DM) with the link (TikTok allows DMs to followers)

### Evening (5 min)
- [ ] Check: Did any video spike unexpectedly today?
- [ ] If a video spiked: Boost it with a quick Spark Ad ($20 test) if you're in Phase 2+

---

## MONTHLY TASKS (First Monday of Each Month)

**Month-start actions:**
- [ ] Review all active affiliate programs — any new opportunities?
- [ ] Check if you've hit volume thresholds for rate negotiation (see scaling_playbook.md)
- [ ] Update Beacons.ai with new products, remove any that are sold out/discontinued
- [ ] Review ConvertKit subscriber growth — time to upgrade plan?
- [ ] Content audit: Are any of your pinned/featured videos outdated?

**Rate negotiation trigger check:**
```
This month's sales by product → compare to negotiation thresholds in scaling_playbook.md
→ Draft negotiation emails for any program where you hit volume targets
```

**Financial review:**
```bash
python financials.py history    # All-time performance
python financials.py project    # Updated projection to $10K
```

---

## ALGORITHM SIGNALS CHEAT SHEET

Actions that boost distribution (most to least impactful):
1. **Shares** — Most powerful signal. Encourage by creating content worth sharing.
2. **Saves** — "Save this for later" content (tip lists, how-to content)
3. **Comments** — Controversial hooks, questions in captions ("Would you try this?")
4. **Completion rate** — Hook must stop the scroll. End must deliver the payoff.
5. **Watch time** — Not just completion rate, but raw minutes watched
6. **Likes** — Least important, but still a positive signal

Actions that hurt distribution (avoid):
1. Low completion rate (< 30%) — Your hook isn't working. Test new hooks.
2. High skip rate in first 1-2 seconds — Your very first frame isn't compelling
3. No engagement in first 30 minutes — Algorithm tests every video to a small audience; if they don't engage, distribution stops
4. Inconsistent posting — Algorithm rewards daily posters with baseline distribution boost
