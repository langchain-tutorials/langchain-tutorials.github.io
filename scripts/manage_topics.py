#!/usr/bin/env python3
"""Utility script to manage used topics tracking for LangChain Tutorials"""
import json
import os
from datetime import datetime, timedelta
import argparse

def get_topics_file_path():
    if os.path.exists("_data") or not os.path.exists("scripts"):
        return "_data/used_topics.json"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, "_data", "used_topics.json")


USED_TOPICS_FILE = get_topics_file_path()


def load_topics():
    """Load used topics from file"""
    if not os.path.exists(USED_TOPICS_FILE):
        return {}
    try:
        with open(USED_TOPICS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading topics: {e}")
        return {}


def save_topics(topics):
    """Save topics to file"""
    os.makedirs(os.path.dirname(USED_TOPICS_FILE) or '.', exist_ok=True)
    with open(USED_TOPICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)


def list_topics(topics):
    """List all used topics"""
    if not topics:
        print("📋 No tracked topics found in _data/used_topics.json")
        return

    print(f"\n📋 Tracked LangChain Topics ({len(topics)}):")
    print("=" * 80)

    sorted_topics = sorted(
        topics.items(),
        key=lambda x: x[1].get('date', '') if isinstance(x[1], dict) else '',
        reverse=True
    )

    for i, (key, data) in enumerate(sorted_topics, 1):
        if isinstance(data, dict):
            title = data.get('title', key)
            date = data.get('date', 'Unknown')
            permalink = data.get('permalink', 'N/A')
        else:
            title = key
            date = 'Unknown'
            permalink = 'N/A'

        try:
            dt = datetime.fromisoformat(date)
            date_str = dt.strftime('%Y-%m-%d %H:%M')
            age_days = (datetime.now() - dt).days
            age_str = f"({age_days}d ago)"
        except Exception:
            date_str = date
            age_str = ""

        print(f"\n{i}. {title[:75]}")
        print(f"   🔗 Permalink: {permalink}")
        print(f"   📅 Date: {date_str} {age_str}")


def clean_old_topics(topics, days=45):
    """Remove topics older than specified days"""
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.isoformat()

    original_count = len(topics)
    topics = {
        k: v for k, v in topics.items()
        if isinstance(v, dict) and v.get('date', '') > cutoff_str
    }
    removed = original_count - len(topics)

    print(f"🧹 Cleaned {removed} topics older than {days} days")
    print(f"📊 Remaining topics: {len(topics)}")

    save_topics(topics)
    return topics


def clear_all_topics():
    """Clear all used topics"""
    if os.path.exists(USED_TOPICS_FILE):
        os.remove(USED_TOPICS_FILE)
        print("✅ All tracked topics cleared!")
    else:
        print("ℹ️ No topics file to clear.")


def main():
    parser = argparse.ArgumentParser(description="Manage tracked topics for LangChain Tutorials")
    parser.add_argument("--list", action="store_true", help="List all tracked topics")
    parser.add_argument("--clean", type=int, default=0, help="Clean topics older than N days (e.g. --clean 45)")
    parser.add_argument("--clear", action="store_true", help="Clear all tracked topics")

    args = parser.parse_args()

    if args.clear:
        clear_all_topics()
        return

    topics = load_topics()

    if args.clean > 0:
        clean_old_topics(topics, days=args.clean)
        return

    list_topics(topics)


if __name__ == "__main__":
    main()

