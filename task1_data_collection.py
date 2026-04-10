import requests
import time
import os
import json
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (important as per instructions)
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (case-insensitive)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Max stories per category
MAX_PER_CATEGORY = 25


def fetch_top_story_ids():
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]  # first 500 IDs
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story_details(story_id):
    """Fetch details of a single story"""
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def categorize_story(title):
    """Assign category based on keywords"""
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None  # ignore if no category matches


def main():
    # Step 1: Get top story IDs
    story_ids = fetch_top_story_ids()

    collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}

    # Current timestamp
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Loop through categories (IMPORTANT: sleep per category)
    for category in CATEGORIES.keys():
        print(f"\nCollecting category: {category}")

        for story_id in story_ids:
            # Stop if category is full
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = fetch_story_details(story_id)

            if not story:
                continue

            title = story.get("title", "")
            assigned_category = categorize_story(title)

            # Only take matching category
            if assigned_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": collected_at
                }

                collected_stories.append(data)
                category_counts[category] += 1

        # Sleep after each category loop (NOT per story)
        time.sleep(2)

    # Step 3: Save to JSON file
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"\nCollected {len(collected_stories)} stories.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()