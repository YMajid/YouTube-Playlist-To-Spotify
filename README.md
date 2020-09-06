# YouTube-Playlist-To-Spotify

Generates a Spotify playlist based on the songs/podcasts found in your liked videos playlist on YouTube.

## How to use:

1. Install libraries

```
pip install -r requirements.txt
```

2. Generate your Spotify [client_id and client_secret](https://developer.spotify.com/documentation/general/guides/authorization-guide/) and add it to the `Secrets.py` file

3. Set up your [YouTube OAuth](https://developers.google.com/youtube/v3/getting-started/)

4. Run the python script

```
python GeneratePlaylist.py
```
