# Playlist Generator

This project provides a simple command-line tool to create mood-based playlists on YouTube Music using the YouTube Data API.

## Setup
1. Install dependencies:
   ```bash
   pip install google-api-python-client google-auth google-auth-oauthlib
   ```
2. Obtain OAuth credentials from the [Google Cloud Console](https://console.cloud.google.com/) and download `client_secret.json` into this directory.
3. Run the script for the first time to complete the OAuth flow. A `token.pickle` file will be created for future authentication.

## Usage
```bash
python playlist_generator.py <mood> [-n NUMBER_OF_TRACKS]
```

Example:
```bash
python playlist_generator.py happy -n 5
```

Supported moods are: `happy`, `calm`, `energetic`, and `sad`.

The script will create a private playlist in your YouTube account with tracks matching the specified mood.
