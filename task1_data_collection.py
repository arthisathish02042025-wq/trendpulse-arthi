#Task 1 — Fetch Data from API
import requests
import json
import time
import os
from datetime import datetime

def fetch_trending_data():
    # 1. Setup Configuration
    headers = {"User-Agent": "TrendPulse/1.0"}
    categories = {
        "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
        "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
        "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
        "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
        "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
    }

    # 2. Fetch Top 500 Story IDs from HackerNews
    try:
        id_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(id_url, headers=headers)
        response.raise_for_status()
        all_ids = response.json()[:500]
    except Exception as e:
        print(f"Error fetching top story IDs: {e}")
        return

    # 3. Fetch full details for each story
    raw_stories = []
    print("Fetching story details from HackerNews...")
    for story_id in all_ids:
        try:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
            story = requests.get(item_url, headers=headers).json()
            # Only add if it's a valid story with a title
            if story and "title" in story:
                raw_stories.append(story)
        except Exception as e:
            # Print error and move on to next ID without crashing
            print(f"Skipping story {story_id} due to error: {e}")
            continue

    # 4. Filter into categories and extract required fields
    final_collection = []
    
    for category, keywords in categories.items():
        count = 0
        for story in raw_stories:
            # Limit to 25 stories per category
            if count >= 25:
                break
                
            title = story.get("title", "")
            title_lower = title.lower()
            
            # Check if any keyword matches the title
            if any(kw.lower() in title_lower for kw in keywords):
                # Map HackerNews fields to TrendPulse fields
                extracted_item = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                final_collection.append(extracted_item)
                count += 1
        
        # Wait 2 seconds between each category loop
        time.sleep(2)

    # 5. Create data directory and save JSON
    if not os.path.exists("data"):
        os.makedirs("data")

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_collection, f, indent=4)

    # Final Expected Console Message
    print(f"Collected {len(final_collection)} stories. Saved to {filename}")

if __name__ == "__main__":
    fetch_trending_data()