import os
import json
import requests
import youtube_dl
import googleapiclient.errors
import googleapiclient.discovery
import google_auth_oauthlib.flow
from Secrets import client_id, client_secret

class GeneratePlaylist:
  def __init__(self):
    self.youtube_client = self.get_youtube_client()
    self.song_information = {}

  def get_youtube_client(self):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()

    youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return youtube_client


  def get_liked_videos(self):
    request = self.youtube_client.videos().list(
      part = "snippet,contentDetails,statistics",
      myRating = "like"
    )
    response = request.execute()

    for item in response:
      title = item["snippet"]["title"]
      youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

      video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
      song_name = video["track"]
      artist_name = video["artist"]
      spotify_uri = self.find_song_uri(song_name, artist_name)

      self.song_information[title] = {
        "song_name": song_name,
        "artist_name": artist_name,
        "youtube_url": youtube_url,
        "spotify_uri": spotify_uri
      }

  def create_spotify_playlist(self):
    body_parameters = json.dumps({
      "name": "YouTube Playlist",
      "public": True,
      "collaborative": False,
      "description": "Content from your YouTube playlist"
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(self.client_id)
    response = requests.post(
      query,
      data = body_parameters,
      headers = {
                "Authorization": "Bearer {}".format(self.client_secret),
                "Content-Type": "application/json"
                }
    )
    response_json = response.json()

    return response_json["id"]

  def find_song_uri(self, song_name, artist_name):
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(song_name, artist_name)
    response = requests.get(
      query,
      headers = {
                "Authorization": "Bearer {}".format(self.client_secret),
                "Content-Type": "application/json"
                }
    )
    response_json = response.json()
    songs = response_json["tracks"]["items"]

    song_uri = songs[0]["uri"]
    return song_uri

  def add_song_to_playlist(self):
    self.get_liked_videos()

    uri_list = []
    for song, information in self.song_information:
      uri_list.append(information["spotify_uri"])
    
    playlist_id = self.create_spotify_playlist()

    request_data = json.dumps(uri_list)
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    response = requests.post(
      query,
      data = request_data,
      headers = {
                "Authorization": "Bearer {}".format(self.client_secret),
                "Content-Type": "application/json"
                }
    )

    response_json = response.json()
    return response_json
  
if __name__ == '__main__':
    gp = GeneratePlaylist()
    gp.add_song_to_playlist()
