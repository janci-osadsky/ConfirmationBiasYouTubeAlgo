import requests
import config
from urllib.parse import urlparse, parse_qs

VIDEO_LINKS_FILE = "links.txt"

def extract_video_id(link):
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("v", [None])[0]


def get_video_metadata(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_id,
        "key": config.API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "items" in data and data["items"]:
        video = data["items"][0]
        snippet = video["snippet"]
        stats = video["statistics"]
        content = video["contentDetails"]

        return {
            "id": video_id,
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "published": snippet.get("publishedAt"),
            "views": stats.get("viewCount"),
            "duration": content.get("duration"),  # in ISO 8601 format
            "likes": stats.get("likeCount", "hidden"),
            "description": snippet.get("description", "")[:150]
        }
    return None


def main():
    with open(VIDEO_LINKS_FILE, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines() if line.strip()]

    print(f"Fetching metadata for {len(links)} videos...")

    all_metadata = []
    for link in links:
        video_id = extract_video_id(link)
        if not video_id:
            print(f"Skipping invalid link: {link}")
            continue

        metadata = get_video_metadata(video_id)
        if metadata:
            print(f"{metadata['title']} ({metadata['views']} views)")
            all_metadata.append(metadata)
        else:
            print(f"Metadata not found for video ID: {video_id}")

    import json
    with open("video_metadata.json", "w", encoding="utf-8") as out:
        json.dump(all_metadata, out, indent=2, ensure_ascii=False)
    return

if __name__ == "__main__":
    main()
