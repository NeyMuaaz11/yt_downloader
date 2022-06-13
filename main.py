from pytube import YouTube
import requests

query = input("Search for a video..\n")

params = {'q':query,
          'type':'video',
          'part':'snippet',
          'key':'AIzaSyBBZkXjWQhX-WuqmYhAKdIStUfIRAL-EGM'}


url = 'https://www.googleapis.com/youtube/v3/search'

r = requests.get(url, params = params)

data = r.json()

videos = data["items"]

# for video in videos:
    
#     print(f"https://www.youtube.com/watch?v={video['id']['videoId']}")
#     print(video['snippet']['title'])
#     print()

down_url = f"https://www.youtube.com/watch?v={videos[0]['id']['videoId']}"

vid = YouTube(down_url)
down_vid = vid.streams.filter(only_audio = True)
final = down_vid[0]

final.download()
print("downloaded")