#!/usr/bin/env python3
"""
content_scheduler.py
--------------------
Manages TikTok content queue, posting schedules, and per-post performance tracking.
Calculates estimated earnings per post based on tracked metrics.

Usage:
    python content_scheduler.py --help
    python content_scheduler.py add        # Add a new video to the queue
    python content_scheduler.py schedule   # Show upcoming scheduled posts
    python content_scheduler.py log        # Log performance for a posted video
    python content_scheduler.py report     # Weekly performance report
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
QUEUE_FILE = DATA_DIR / "content_queue.json"
POSTED_FILE = DATA_DIR / "posted_videos.json"

# Best posting windows in your local timezone (24h format)
POSTING_WINDOWS = [
    {"label": "Morning", "start": 6, "end": 9},
    {"label": "Lunch", "start": 12, "end": 14},
    {"label": "Prime Time", "start": 19, "end": 22},
]

# Estimated CTR from views to bio-link click (adjust as you gather real data)
DEFAULT_LINK_CTR = 0.01       # 1% of viewers click the link
# Estimated CVR from link click to purchase
DEFAULT_CVR = 0.025           # 2.5% of clickers buy
# Average commission per sale across your portfolio
DEFAULT_AVG_COMMISSION = 75.0  # $75

# Day-of-week performance multipliers (vs baseline)
DOW_MULTIPLIERS = {
    0: 0.92,  # Monday
    1: 1.22,  # Tuesday
    2: 1.18,  # Wednesday
    3: 1.15,  # Thursday
    4: 1.00,  # Friday
    5: 0.95,  # Saturday
    6: 1.12,  # Sunday
}

VIDEO_FRAMEWORKS = [
    "30-Day Trial",
    "POV Discovery",
    "Things I Wish I Knew",
    "Unboxing + Review",
    "Amazon Finds",
    "Before/After Demo",
    "Duet/Stitch",
    "Day-in-My-Life",
    "Stop Scrolling",
    "Comparison",
]

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    with open(path, "r") as f:
        return json.load(f)


def save_json(path: Path, data: object) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_queue() -> list:
    return load_json(QUEUE_FILE, [])


def save_queue(queue: list) -> None:
    save_json(QUEUE_FILE, queue)


def load_posted() -> list:
    return load_json(POSTED_FILE, [])


def save_posted(posted: list) -> None:
    save_json(POSTED_FILE, posted)

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def estimate_earnings(views: int, link_ctr: float = DEFAULT_LINK_CTR,
                       cvr: float = DEFAULT_CVR,
                       avg_commission: float = DEFAULT_AVG_COMMISSION) -> dict:
    """Estimate earnings from a video given its view count."""
    clicks = int(views * link_ctr)
    conversions = clicks * cvr
    earnings = conversions * avg_commission
    return {
        "estimated_clicks": clicks,
        "estimated_conversions": round(conversions, 2),
        "estimated_earnings_usd": round(earnings, 2),
        "epc": round(earnings / clicks, 4) if clicks > 0 else 0.0,
    }


def suggest_post_time(target_date: Optional[datetime] = None) -> list:
    """Return suggested post times for a given date."""
    target = target_date or datetime.now()
    multiplier = DOW_MULTIPLIERS.get(target.weekday(), 1.0)
    suggestions = []
    for window in POSTING_WINDOWS:
        mid_hour = (window["start"] + window["end"]) // 2
        post_time = target.replace(hour=mid_hour, minute=0, second=0, microsecond=0)
        suggestions.append({
            "window": window["label"],
            "suggested_time": post_time.strftime("%Y-%m-%d %H:%M"),
            "day_multiplier": multiplier,
        })
    return suggestions


def add_video_to_queue(
    title: str,
    product: str,
    framework: str,
    affiliate_link_id: str,
    scheduled_date: str,
    niche: str,
    hook: str,
) -> dict:
    """Add a new video to the content queue."""
    queue = load_queue()
    video = {
        "id": f"vid_{int(datetime.now().timestamp())}",
        "title": title,
        "product": product,
        "framework": framework,
        "niche": niche,
        "hook": hook,
        "affiliate_link_id": affiliate_link_id,
        "scheduled_date": scheduled_date,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
    }
    queue.append(video)
    save_queue(queue)
    return video


def mark_posted(video_id: str, tiktok_url: str = "") -> dict:
    """Move a video from queue to posted, record posting time."""
    queue = load_queue()
    posted = load_posted()

    video = next((v for v in queue if v["id"] == video_id), None)
    if not video:
        raise ValueError(f"Video {video_id} not found in queue.")

    video["status"] = "posted"
    video["posted_at"] = datetime.now().isoformat()
    video["tiktok_url"] = tiktok_url
    video["metrics"] = {
        "views": 0,
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "link_clicks": 0,
        "last_updated": datetime.now().isoformat(),
    }

    queue = [v for v in queue if v["id"] != video_id]
    posted.append(video)
    save_queue(queue)
    save_posted(posted)
    return video


def update_metrics(video_id: str, views: int, likes: int, comments: int,
                   shares: int, link_clicks: int) -> dict:
    """Update performance metrics for a posted video."""
    posted = load_posted()
    video = next((v for v in posted if v["id"] == video_id), None)
    if not video:
        raise ValueError(f"Video {video_id} not found in posted videos.")

    video["metrics"].update({
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "link_clicks": link_clicks,
        "last_updated": datetime.now().isoformat(),
    })
    # Override click-based estimate with actual link_clicks if available
    actual_link_ctr = link_clicks / views if views > 0 else DEFAULT_LINK_CTR
    video["earnings_estimate"] = estimate_earnings(
        views, link_ctr=actual_link_ctr
    )
    save_posted(posted)
    return video


def weekly_report(weeks_back: int = 0) -> dict:
    """Generate a performance report for a given week."""
    posted = load_posted()
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday(), weeks=weeks_back)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=7)

    week_videos = [
        v for v in posted
        if v.get("posted_at")
        and week_start <= datetime.fromisoformat(v["posted_at"]) < week_end
    ]

    if not week_videos:
        return {"error": "No videos found for the specified week.", "week_start": str(week_start.date())}

    total_views = sum(v.get("metrics", {}).get("views", 0) for v in week_videos)
    total_likes = sum(v.get("metrics", {}).get("likes", 0) for v in week_videos)
    total_comments = sum(v.get("metrics", {}).get("comments", 0) for v in week_videos)
    total_shares = sum(v.get("metrics", {}).get("shares", 0) for v in week_videos)
    total_link_clicks = sum(v.get("metrics", {}).get("link_clicks", 0) for v in week_videos)
    total_estimated_earnings = sum(
        v.get("earnings_estimate", {}).get("estimated_earnings_usd", 0) for v in week_videos
    )

    best_video = max(week_videos, key=lambda v: v.get("metrics", {}).get("views", 0))
    framework_counts = {}
    for v in week_videos:
        fw = v.get("framework", "Unknown")
        framework_counts[fw] = framework_counts.get(fw, 0) + 1
    best_framework = max(framework_counts, key=framework_counts.get)

    return {
        "week_of": str(week_start.date()),
        "videos_posted": len(week_videos),
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_link_clicks": total_link_clicks,
        "avg_views_per_video": round(total_views / len(week_videos), 0) if week_videos else 0,
        "engagement_rate_pct": round((total_likes + total_comments + total_shares) / total_views * 100, 2) if total_views > 0 else 0,
        "link_ctr_pct": round(total_link_clicks / total_views * 100, 3) if total_views > 0 else 0,
        "estimated_weekly_earnings_usd": round(total_estimated_earnings, 2),
        "best_video": {
            "id": best_video["id"],
            "title": best_video["title"],
            "views": best_video.get("metrics", {}).get("views", 0),
            "framework": best_video.get("framework"),
        },
        "top_framework": best_framework,
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_add(_args) -> None:
    """Interactive prompt to add a video to the queue."""
    print("\n=== Add New Video to Queue ===")
    title = input("Video title/description: ").strip()
    product = input("Product being promoted: ").strip()

    print("\nFrameworks:")
    for i, fw in enumerate(VIDEO_FRAMEWORKS, 1):
        print(f"  {i}. {fw}")
    fw_idx = int(input("Framework number: ").strip()) - 1
    framework = VIDEO_FRAMEWORKS[fw_idx] if 0 <= fw_idx < len(VIDEO_FRAMEWORKS) else "Custom"

    affiliate_link_id = input("Affiliate link ID (from link_manager): ").strip()
    niche = input("Niche (e.g., beauty, fitness, AI tools): ").strip()
    hook = input("Opening hook line: ").strip()
    scheduled_date = input("Scheduled date (YYYY-MM-DD HH:MM or leave blank for now): ").strip()
    if not scheduled_date:
        scheduled_date = datetime.now().isoformat()

    video = add_video_to_queue(title, product, framework, affiliate_link_id, scheduled_date, niche, hook)
    print(f"\n✓ Video added to queue: {video['id']}")

    suggestions = suggest_post_time(datetime.fromisoformat(scheduled_date[:10]))
    print("\nSuggested posting windows:")
    for s in suggestions:
        print(f"  [{s['window']}] {s['suggested_time']}  (day multiplier: {s['day_multiplier']}x)")


def cmd_schedule(_args) -> None:
    """Display the upcoming content queue."""
    queue = load_queue()
    if not queue:
        print("Queue is empty. Use `add` to add videos.")
        return

    queue_sorted = sorted(queue, key=lambda v: v.get("scheduled_date", ""))
    print(f"\n{'='*70}")
    print(f"{'CONTENT QUEUE':^70}")
    print(f"{'='*70}")
    print(f"{'ID':<20} {'Title':<25} {'Framework':<20} {'Scheduled':<20}")
    print(f"{'-'*70}")
    for v in queue_sorted:
        scheduled = v.get("scheduled_date", "")[:16]
        print(f"{v['id']:<20} {v['title'][:24]:<25} {v.get('framework','')[:19]:<20} {scheduled:<20}")
    print(f"\nTotal queued: {len(queue)} videos")


def cmd_log(_args) -> None:
    """Log or update metrics for a posted video."""
    print("\n=== Log Video Performance ===")
    video_id = input("Video ID (or 'posted' to mark a queued video as posted): ").strip()

    if video_id == "posted":
        queue = load_queue()
        if not queue:
            print("Queue is empty.")
            return
        print("Queued videos:")
        for v in queue:
            print(f"  {v['id']}: {v['title']}")
        video_id = input("Enter video ID to mark as posted: ").strip()
        tiktok_url = input("TikTok video URL (optional): ").strip()
        video = mark_posted(video_id, tiktok_url)
        print(f"✓ Marked as posted: {video['id']}")
        return

    views = int(input("Views: ").strip() or 0)
    likes = int(input("Likes: ").strip() or 0)
    comments = int(input("Comments: ").strip() or 0)
    shares = int(input("Shares: ").strip() or 0)
    link_clicks = int(input("Link clicks (from TikTok analytics or affiliate tracker): ").strip() or 0)

    video = update_metrics(video_id, views, likes, comments, shares, link_clicks)
    est = video.get("earnings_estimate", {})
    print(f"\n✓ Metrics updated for: {video['title']}")
    print(f"  Views: {views:,}  |  Engagement: {likes+comments+shares:,}")
    print(f"  Link Clicks: {link_clicks:,}  |  Link CTR: {link_clicks/views*100:.2f}%" if views else "")
    print(f"  Estimated Earnings: ${est.get('estimated_earnings_usd', 0):.2f}")
    print(f"  Estimated Conversions: {est.get('estimated_conversions', 0)}")


def cmd_report(_args) -> None:
    """Display the weekly performance report."""
    weeks_back = int(input("Weeks back (0 = current week): ").strip() or 0)
    report = weekly_report(weeks_back)

    if "error" in report:
        print(f"\n{report['error']}")
        return

    print(f"\n{'='*60}")
    print(f"WEEKLY REPORT — Week of {report['week_of']}")
    print(f"{'='*60}")
    print(f"Videos Posted:          {report['videos_posted']}")
    print(f"Total Views:            {report['total_views']:,}")
    print(f"Total Link Clicks:      {report['total_link_clicks']:,}")
    print(f"Link CTR:               {report['link_ctr_pct']}%")
    print(f"Engagement Rate:        {report['engagement_rate_pct']}%")
    print(f"Avg Views/Video:        {report['avg_views_per_video']:,.0f}")
    print(f"Estimated Earnings:     ${report['estimated_weekly_earnings_usd']:,.2f}")
    print(f"\nBest Video:             {report['best_video']['title']}")
    print(f"  Views:                {report['best_video']['views']:,}")
    print(f"  Framework:            {report['best_video']['framework']}")
    print(f"\nTop Performing Format:  {report['top_framework']}")
    print(f"{'='*60}")


def main():
    ensure_data_dir()

    parser = argparse.ArgumentParser(
        description="TikTok Content Scheduler & Performance Tracker"
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("add", help="Add a video to the content queue")
    subparsers.add_parser("schedule", help="View the upcoming content queue")
    subparsers.add_parser("log", help="Log performance metrics for a video")
    subparsers.add_parser("report", help="View weekly performance report")

    args = parser.parse_args()

    commands = {
        "add": cmd_add,
        "schedule": cmd_schedule,
        "log": cmd_log,
        "report": cmd_report,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
