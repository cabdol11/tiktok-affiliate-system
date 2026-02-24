# TikTok Shop OS — GTM Playbook
## Week-by-week execution. No ambiguity. Just do this.

---

## THE NORTH STAR

**12-month goal:** $240K MRR from SaaS + managed services combined
**24-month goal:** $1.8M MRR (billionaire runway)
**The metric that predicts everything:** Brands contacted per week → set a minimum of 20

---

## WEEK 1 — FOUNDATION

**Day 1–2: Build your proof**
- [ ] Document your own brand's GMV numbers (real or projected from test)
- [ ] Write one case study: even if it's "$X GMV in first 30 days with our own product"
- [ ] Create a one-page "what we do" overview — lift from sales_deck.md Slide 4

**Day 3–4: Build your hit list**
- [ ] Use the prospect list in outreach_sequences.md
- [ ] Verify each brand has TikTok Shop enabled (visit their TikTok profile)
- [ ] Find the right contact for each: LinkedIn search "[Brand Name] founder" or "head of growth"
- [ ] Add all 20 to brand_outreach.py: `python brand_outreach.py add`

**Day 5: Send first 10 outreach messages**
- [ ] Email sequence: copy from outreach_sequences.md Sequence 1 Email 1
- [ ] LinkedIn: send connection requests with note from Sequence 2
- [ ] Log every send in CRM: `python brand_outreach.py touch`

**Week 1 target:** 20 prospects in CRM, 10 contacted, 0 deals (normal)

---

## WEEK 2 — MOMENTUM

**Day 8–9: Follow up + new outreach**
- [ ] Follow up on Week 1 contacts with Email 2 (4 days since Email 1)
- [ ] Send 10 new cold outreach messages
- [ ] Total: 20 brands contacted

**Day 10: LinkedIn content post**

Post this on LinkedIn (copy verbatim, personalize numbers):

> "TikTok Shop brands spending on Spark Ads but not running affiliates are leaving 70% of their GMV potential on the table.
>
> Here's what we've seen: the same product, same audience, same price point — but with 100 active affiliates instead of paid ads — converts at 2–3× the rate.
>
> We generated [$X] in GMV in [X] days for [our brand / a brand we work with] using purely affiliate distribution.
>
> If you're a DTC brand on TikTok Shop and your affiliate count is under 50, DM me."

**Day 11–12: First reply handling**
- If anyone replies: book a call SAME DAY. Use the demo script in outreach_sequences.md.
- Update CRM immediately: `python brand_outreach.py convert`

**Week 2 target:** 20 total contacted, 3–5 replies, 1 demo scheduled

---

## WEEK 3 — FIRST DEMO

**Demo week goals:**
- [ ] Run 2–3 demo calls using the script in Sequence 4
- [ ] Send proposals same day as demo using the template in Sequence 5
- [ ] Follow up on proposals within 24 hours with a Loom video walkthrough

**Loom video script (2 minutes):**
> "Hey [Name], [Your name] here. Wanted to put a face to the email and
> walk you through the proposal I sent in about 90 seconds.
> [Screen share proposal. Walk through economics slide only.]
> The number I want you to focus on is this one — [point to net revenue line].
> That's what you walk away with after everything.
> If that math works for [Brand], let's do a 30-day pilot this week.
> Here's my calendar — grab any slot that works."

**Week 3 target:** 2 demos run, 1 proposal sent, 1 verbal yes

---

## WEEK 4 — FIRST CLOSE

**Close target:** 1 managed client signed by end of week 4

**What closing looks like:**
- Signed proposal (via DocuSign, HelloSign, or even a written email reply confirming terms)
- Commission rate set in their TikTok Seller Center
- Product samples arranged
- Kick-off call scheduled

**After close:**
- [ ] Move to closed_won in CRM: `python brand_outreach.py convert`
- [ ] Document the close story (what worked, what objection you overcame)
- [ ] Screenshot the win. Post to LinkedIn immediately.

---

## MONTHS 2–3 — SCALE OUTREACH

**Weekly cadence:**
- Monday: Send 20 new cold outreaches
- Tuesday: Follow up on all unanswered messages from 4+ days ago
- Wednesday: LinkedIn post (case study, data, insight)
- Thursday: Run demos (batch them — 3+ calls on one day is fine)
- Friday: Send proposals, follow up on open proposals, update CRM

**Month 2 target:** 5 managed clients, $25–50K/month GMV under management
**Month 3 target:** 10 managed clients, $100K+/month GMV under management

---

## MONTH 3 — LAUNCH CONTENT ENGINE

TikTok + LinkedIn content is your inbound machine. Every post is a sales call that scales.

**TikTok content (3x/week):**
- Format 1: "We tested [product] with 50 creators. Here's what happened." (results reveal)
- Format 2: "What a $[X] TikTok Shop month looks like behind the scenes" (POV/behind scenes)
- Format 3: "How to find TikTok creators for your brand in 10 minutes" (tutorial — lead gen)

**LinkedIn content (2x/week):**
- Raw GMV data and case studies
- "What I learned running TikTok Shop affiliates for [X] brands"
- "The 3 mistakes DTC brands make on TikTok Shop"

**Goal:** Every content piece should generate at least 1 inbound DM per week by month 4.

---

## MONTH 6 — LAUNCH SAAS BETA

**When to launch SaaS:** When you have 10+ managed clients and you're running the operation manually

**How to launch:**
1. Tell your managed clients: "We're launching a self-serve version of the platform we use for you."
2. Offer them 3 months free in exchange for feedback and a testimonial
3. Use their feedback to fix the top 3 pain points before public launch
4. Launch on Product Hunt, post on LinkedIn, post case study on TikTok

**SaaS launch day targets:**
- 50 sign-ups in first 48 hours
- 10 paid conversions in first 30 days
- 1 press mention (reach out to TechCrunch, The Information, Glossy)

---

## MONTH 12 — APPLY TO TIKTOK PARTNER PROGRAM

TikTok has an official Agency Partner Program for TikTok Shop. Getting listed means:
- Inbound from TikTok directly
- Co-marketing opportunities
- Early access to new TikTok Shop features
- Credibility signal that closes deals

**How to apply:**
1. URL: https://business.tiktokshop.com/us/affiliate (Agency Partner section)
2. Requirements: demonstrated GMV results, active brands, compliance history
3. Apply at month 12 when you have real GMV data to submit

---

## METRICS DASHBOARD — TRACK WEEKLY

Run this every Monday morning:
```
python brand_outreach.py dashboard
```

**KPIs to hit each month:**

| Metric | Month 1 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|----------|
| Brands contacted | 40 | 120 | 300 | 800 |
| Demo call rate | 10% | 15% | 20% | 25% |
| Close rate | 10% | 15% | 20% | 25% |
| Managed clients | 1 | 8 | 25 | 80 |
| SaaS brands | 0 | 0 | 20 | 200 |
| MRR (combined) | $5K | $40K | $130K | $500K |

---

## THE ONE THING

If you only do one thing from this playbook every single week:

**Contact 20 brands. Every week. Without exception.**

Everything else is optimization. The outreach volume is the business.

At 20/week: ~1,000 brands/year contacted
At 15% demo rate: 150 demos
At 20% close rate from demo: 30 clients
At $2,000/month average: **$60K MRR from outreach alone**

Do not stop the outreach to build the deck. Do not stop outreach to build the software. The outreach IS the business until $500K MRR.
