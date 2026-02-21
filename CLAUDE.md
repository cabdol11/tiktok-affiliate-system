# CLAUDE.md — TikTok Affiliate System
## Organizational Control & Autonomy Guidelines

This file governs how Claude and any AI team members operate on this project.
Read this file before taking any action.

---

## Project Overview

**Owner:** Connor Abdolhosseinzadeh (@cabdol11)
**Goal:** $10,000 net profit per week via TikTok affiliate marketing
**Primary niche:** Beauty & Skincare (TikTok Shop), expanding to AI Tools and Fitness
**Current phase:** Phase 1 — Building (Week 1)
**GitHub:** https://github.com/cabdol11/tiktok-affiliate-system

---

## Tech Stack

- **Language:** Python 3.9+
- **Virtual environment:** `venv/` (always use `venv/bin/python3` to run scripts)
- **Data storage:** JSON files in `data/` directory (gitignored)
- **Scripts:** `affiliate_tracker.py`, `content_scheduler.py`, `product_research.py`, `link_manager.py`, `financials.py`

**Run any script:**
```bash
cd /Users/connorabdolhosseinzadeh/tiktok-affiliate-system
venv/bin/python3 <script>.py <command>
```

---

## Autonomy Rules — What Claude Can Do Without Asking

Claude and team agents may proceed without checking in for:

- Running any script in read/report mode (`report`, `dashboard`, `top10`, `trends`, `health`, `history`, `project`)
- Adding products, links, or data entries to the local database (`data/`)
- Editing `.md` documentation files
- Writing new Python scripts or utilities that extend the system
- Installing packages into `venv/` via pip
- Researching trending products, competitors, or affiliate programs via web search
- Committing changes to git and pushing to GitHub
- Creating new branches for feature work

---

## Requires Owner Approval Before Acting

Always stop and confirm with Connor before:

- Deleting any file or data
- Spending any money (ads, tools, subscriptions)
- Signing up for or connecting to any external service or affiliate network
- Posting anything publicly on TikTok or any social platform
- Sharing affiliate links or product recommendations externally
- Modifying financial projections in `financials.py` logic (not data entries)
- Changing commission rates or product scores that affect business decisions

---

## Business Rules (Enforce These Always)

- **Minimum product score:** 7.5/10 composite — do not recommend products below this
- **Price sweet spot:** $30–$100 for TikTok Shop products (best CVR)
- **Primary network:** TikTok Shop first, then ClickBank, ShareASale, Impact
- **FTC compliance:** Every affiliate post must include `#affiliate` or `#affiliatelink` — no exceptions
- **Kill threshold:** Any product with 50+ clicks and CVR < 2% — flag for replacement
- **A/B test minimum:** 20+ clicks per variant before declaring a winner

---

## Weekly Priorities (Update Each Monday)

- **Primary product:** Medicube PDRN Peptide Serum (Score: 7.99/10)
- **Network:** TikTok Shop
- **Phase:** 1 — Organic only, no ad spend yet
- **Weekly sales target:** 1–2 sales (Week 1 milestone)

---

## File Map

| File | Purpose |
|---|---|
| `affiliate_tracker.py` | Track products, clicks, sales, P&L |
| `content_scheduler.py` | Schedule videos, log performance |
| `product_research.py` | Research and score products |
| `link_manager.py` | Tracked links and A/B testing |
| `financials.py` | Weekly financials, projections |
| `business_plan.md` | Full niche strategy and profit math |
| `content_system.md` | Hook library, caption templates, frameworks |
| `weekly_sop.md` | Exact daily/weekly workflow |
| `scaling_playbook.md` | Growth roadmap to $10K/week |
| `tool_stack.md` | All tools, accounts, and software |
| `data/` | Local JSON data (gitignored) |

---

## Git Workflow

- **Branch:** `main` (single branch for now)
- **Commit style:** Imperative, concise — e.g. `Add Medicube product to research DB`
- **Push:** After every meaningful change
- **Remote:** https://github.com/cabdol11/tiktok-affiliate-system

---

## Team Roles (Future)

As the system scales, roles will be assigned:

| Role | Responsibility |
|---|---|
| Research Agent | Monday product research, competitor tracking |
| Content Agent | Hook writing, caption generation, content calendar |
| Analytics Agent | Friday performance review, weekly reports |
| Finance Agent | Weekly P&L logging, projections |

All agents operate under the autonomy rules above.

---

## Current Status

- [x] Git initialized and pushed to GitHub
- [x] Virtual environment set up
- [x] All scripts verified working
- [x] First product added: Medicube PDRN Peptide Serum (7.99/10)
- [ ] TikTok Shop affiliate account connected
- [ ] First tracked link created
- [ ] First video posted
- [ ] First sale logged
