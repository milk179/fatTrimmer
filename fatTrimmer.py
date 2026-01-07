from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import time

# no playlist-read-collaborative so I don't delete songs that my collaborators like
scope = "user-library-read playlist-read-private playlist-modify-private playlist-modify-public"
sp = Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.me()["id"]

# get liked songs's URIs

liked_uris = set()
offset = 0

while True:

    results = sp.current_user_saved_tracks(limit=50, offset=offset)

    if not results["items"]:
        break

    for item in results["items"]:
        liked_uris.add(item["track"]["uri"])

    offset += 50

print(f"Fetched {len(liked_uris)} liked songs.")


# get playlists

playlists = []
offset = 0
said = ""

while True:

    cluster = sp.current_user_playlists(limit=50, offset=offset)

    if not cluster["items"]:
        break

    playlists.extend(cluster["items"])

    offset += 50


# iterates through each playlist

for plist in playlists:

    if plist["owner"]["id"] != user_id: # this skips collaborative playlists too
        continue

    remove = []
    track_offset = 0

    # fetches all the tracks from each playlist

    while True:

        if said != f"FETCHING tracks from {plist['name']}":
            print(f"FETCHING tracks from {plist['name']}")
            said = f"FETCHING tracks from {plist['name']}"

        tracks = sp.playlist_items(plist["id"], limit= 50, offset=track_offset)
        time.sleep(0.1)

        if not tracks["items"]:
            break

        for item in tracks["items"]:

            track = item["track"]

            if track is None or track.get("id") is None or track.get("uri") is None or track["is_local"]: # sometimes objects inside the playlist can be invalid tracks, skips them
                continue

            if track and track["uri"] not in liked_uris:
                remove.append(track["uri"])

        track_offset += 50


    # removing unliked tracks

    if remove:

        for i in range(0, len(remove), 50):

            sp.playlist_remove_all_occurrences_of_items(plist["id"], remove[i:i+50])
            time.sleep(0.3)
            if said != f"REMOVED {len(remove)} from {plist['name']}":
                print(f"REMOVED {len(remove)} from {plist['name']}")
                said = f"REMOVED {len(remove)} from {plist['name']}"


print("ALL DONE!!!")
exit()