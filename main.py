from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
date=input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

BILL_URL=f"https://www.billboard.com/charts/hot-100/{date}/"

response=requests.get(url=BILL_URL)
response.raise_for_status()
info=response.text
soup=BeautifulSoup(info,"lxml")
song_info=soup.find_all(name="h3",class_="c-title")
song_names=[]
a={}
for song in song_info:
    a=song.getText()
    song_names.append(a)
    
new_list = [item.strip() for item in song_names]
song_names=(new_list[7:407])
final_list=song_names[0::4]


CLIENT_ID="enter your id"
CLIENT_SECRET="enter your secret code"
NAME="Ayush Tiwari"



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=NAME, 
    )
)
user_id = sp.current_user()["id"]

print(user_id)


#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in final_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
