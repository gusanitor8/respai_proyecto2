import os
import requests
import json
import time

# ---------------- CONFIG ----------------
API_KEY = "AIzaSyCtkUjni3XDsoM0brb4iCKjfVxy8rvCaBw"
VIDEO_ID = "nHkKJ87FS6s"  
BASE_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
MAX_CALLS = 20             # 20 calls x 100 results = 2000 comments
OUTPUT_DIR = "data/iphone_samsung_4_comments_relevance"
SUFIX = ""
# ----------------------------------------


def fetch_comments():
    """
    Fetch comments from a YouTube video using the YouTube Data API v3.
    Handles pagination with nextPageToken up to MAX_CALLS.
    Each response is saved as a JSON file in OUTPUT_DIR.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    next_page_token = None

    for call_number in range(1, MAX_CALLS + 1):
        params = {
            "part": "snippet,replies",
            "videoId": VIDEO_ID,
            "maxResults": 100,
            "key": API_KEY,
            "order": "relevance"
        }
        if next_page_token:
            params["pageToken"] = next_page_token

        print(f"Fetching page {call_number} (token={next_page_token})...")
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()

        # Save response to file
        file_path = os.path.join(OUTPUT_DIR, f"comments_page_{call_number}{SUFIX}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved response to {file_path}")

        # Get next page token
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            print("No more pages available.")
            break

        time.sleep(1)  # <-- polite pause to avoid hitting quota too fast


if __name__ == "__main__":
    fetch_comments()