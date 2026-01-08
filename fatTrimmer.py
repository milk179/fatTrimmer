from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import time
import tkinter as tk
from tkinter import ttk
import threading

def main():

    gui()

def gui():

    root = tk.Tk()
    root.geometry("410x550")
    root.minsize(410, 550)
    root.title("Fat-Trimmer")
    root.configure(bg="gray15")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=2)
    root.rowconfigure(3, weight=3)

    root.resizable(1, 1)


    frame = ttk.Frame(root, padding=0)
    frame.grid()

    label = tk.Label(root, text="Fat-Trimmer", font=('Comfortaa', 24, "underline"), bg="gray15", fg="white")
    label.grid(column=0, row=1, pady=10, sticky="nsew")

    text = tk.Text(root, bg="whitesmoke", bd=4, width=40, height=21, font=('Comfortaa', 13), state="disabled")
    text.grid(column=0, row=3, padx=10, pady=10, sticky="nsew")
    text.tag_config("red", foreground="red", font=("Comfortaa", 13, "bold"))
    text.tag_config("yellow", foreground="dark goldenrod", font=("Comfortaa", 13, "bold"))
    text.tag_config("green", foreground="green", font=("Comfortaa", 13, "bold"))

    button = tk.Button(root, text="Begin Trimming", font=('Comfortaa', 15), bg="whitesmoke", command=lambda: threading.Thread(target=run, args=(button, text), daemon=True).start())
    button.grid(column=0, row=2, pady=20)

    root.mainloop()

def applyTag(text, word, tagName):

    start_index = text.search(word, text.index("insert linestart"), text.index("insert lineend"))
    end_index = f"{start_index}+{len(word)}c"
    text.tag_add(tagName, start_index, end_index)



def run(button, text):

    button.config(state="disabled")

    text.delete("1.0", "end")

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

    text.config(state="normal")
    text.insert("end", f"\nFetched {len(liked_uris)} liked songs.")
    text.see("end")
    text.config(state="disabled")


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

            if said != f"\nFETCHING tracks from {plist['name']}":
                text.config(state="normal")

                text.insert("end", f"\nFETCHING tracks from {plist['name']}")
                applyTag(text, "FETCHING", "yellow")
                text.see("end")

                text.config(state="disabled")

                said = f"\nFETCHING tracks from {plist['name']}"



            tracks = sp.playlist_items(plist["id"], limit= 50, offset=track_offset)

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
                time.sleep(0.2)
                if said != f"\nREMOVED {len(remove)} from {plist['name']}":
                    text.config(state="normal")

                    text.insert("end", f"\nREMOVED {len(remove)} from {plist['name']}")
                    applyTag(text, "REMOVED", "red")
                    text.see("end")

                    text.config(state="disabled")

                    said = f"\nREMOVED {len(remove)} from {plist['name']}"


    text.config(state="normal")

    text.insert("end", "\nALL DONE!!!")
    applyTag(text, "ALL DONE!!!", "green")
    text.see("end")

    text.config(state="disabled")

    button.config(state="normal")


if __name__ == "__main__":
    main()