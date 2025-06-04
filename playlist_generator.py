import os
import random
from typing import List

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Scopes for accessing YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube"]

# Simple mapping from moods to search keywords
MOOD_MAP = {
    "happy": ["happy songs", "upbeat music"],
    "calm": ["chill music", "relaxing songs"],
    "energetic": ["high energy music", "workout playlist"],
    "sad": ["sad songs", "melancholy music"],
}

def authenticate() -> 'Resource':
    """Authenticate the user and return a YouTube API service."""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES)
            creds = flow.run_console()
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def create_playlist(service, title: str, description: str) -> str:
    """Create a YouTube playlist and return its ID."""
    request = service.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {"privacyStatus": "private"}
        },
    )
    response = request.execute()
    return response["id"]

def search_videos(service, query: str, max_results: int = 10) -> List[str]:
    """Search for videos and return a list of video IDs."""
    request = service.search().list(
        part="id",
        q=query,
        type="video",
        maxResults=max_results,
    )
    response = request.execute()
    return [item["id"]["videoId"] for item in response.get("items", [])]

def add_video_to_playlist(service, playlist_id: str, video_id: str) -> None:
    """Add a video to the specified playlist."""
    service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()

def generate_mood_playlist(service, mood: str, num_tracks: int = 5) -> str:
    """Generate a playlist for the given mood."""
    keywords = MOOD_MAP.get(mood.lower())
    if not keywords:
        raise ValueError(f"Unknown mood: {mood}")
    query = random.choice(keywords)
    video_ids = search_videos(service, query, max_results=num_tracks)
    playlist_id = create_playlist(service, f"{mood.title()} Playlist", f"A playlist for {mood} mood")
    for vid in video_ids:
        add_video_to_playlist(service, playlist_id, vid)
    return playlist_id

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate mood playlists on YouTube Music")
    parser.add_argument("mood", help="Mood to base the playlist on")
    parser.add_argument("-n", "--num", type=int, default=5, help="Number of tracks to add")
    args = parser.parse_args()
    try:
        service = authenticate()
        playlist_id = generate_mood_playlist(service, args.mood, args.num)
        print(f"Created playlist with ID: {playlist_id}")
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
