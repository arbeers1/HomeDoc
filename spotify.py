#File: spotify.py
#Description: Interface for accessing and streaming from spotify

import spotipy
from spotipy.oauth2 import SpotifyOAuth

#client id for this application
client_id = "b1864127f12049e391dc30614475e211"
#Permissions to request
scp = "user-library-read, user-read-playback-state, user-modify-playback-state, streaming"

class spotify():

    def __init__(self, secret_id):
        """
        Creates a spotify object.

        Paramaters:
        secret - The secret key obtained on spotify's dev site
        """
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=secret_id, scope=scp, redirect_uri = "http://localhost/"))

    def music(self):
        """
        Retrieves all user stored music categories

        Returns:
        A list containing the playlist 'Liked Songs' as well as all user created playlist's formatted (playlist_name, playlist_id, image_url).
        """
        list = [("Liked Songs", None, None)]
        result = self._sp.current_user_playlists()["items"]
        for i in range(len(result)):
            list.append((result[i]["name"], result[i]["id"], result[i]["images"][2]["url"]))
        return list

    def tracks(self, playlist_id):
        """
        Retrieves tracks from a given playlist

        Paramaters:
        playlist_id - the id of the playlist, if None then 'Liked Songs' is called

        Returns:
        List of tracks formatted [[track_name, (track_artists), track_uri, image_url, track_duration, track_min, track_sec]]
        """
        if(playlist_id == None):
            result = self._sp.current_user_saved_tracks()["items"]
        else:
            result = self._sp.playlist_items(playlist_id)["items"]
        list = []
        for i in range(len(result)):
            track = []
            track.append((result[i]["track"]["name"]))
            artists_list = []
            for j in range(len(result[i]["track"]["artists"])):
                artists_list.append(result[i]["track"]["artists"][j]["name"])
            track.append(artists_list)
            track.append((result[i]["track"]["uri"]))
            track.append((result[i]["track"]["album"]["images"][2]["url"]))
            track.append((result[i]["track"]["duration_ms"]))
            track.append(int(result[i]["track"]["duration_ms"] / 1000 / 60))
            track.append(int(result[i]["track"]["duration_ms"] / 1000 % 60))
            list.append(track)
        return list

    def search(self, query):
        """
        Retrieves tracks from a given search query

        Paramaters:
        query - the text to search

        Returns:
        List of tracks formatted [[track_name, [track_artists], track_uri, image_url], track_duration, track_min, track_sec]]
        """
        result = self._sp.search(query, limit = 10, type = 'track')["tracks"]["items"]
        list = []
        for i in range(len(result)):
            track = []
            track.append((result[i]["name"]))
            artists_list = []
            for j in range(len(result[i]["artists"])):
                artists_list.append(result[i]["artists"][j]["name"])
            track.append(artists_list)
            track.append((result[i]["uri"]))
            track.append((result[i]["album"]["images"][2]["url"]))
            track.append((result[i]["duration_ms"]))
            track.append(int(result[i]["duration_ms"] / 1000 / 60))
            track.append(int(result[i]["duration_ms"] / 1000 % 60))
            list.append(track)
        return list

    def devices(self):
        """
        Retrieves a list of available devices to remote play on

        Returns:
        List of devices formatted [[device_name, device_id, device_volume]]
        """
        result = self._sp.devices()["devices"]
        list = []
        for i in range(len(result)):
            device = []
            device.append(result[i]["name"])
            device.append(result[i]["id"])
            device.append(result[i]["volume_percent"])
            list.append(device)
        return list   

    def play(self, device, uri, position):
        """
        Plays a track

        Paramaters
        device - the device id to stream to
        uri - the track uri to play
        """
        self._sp.start_playback(device, uris = uri, position_ms = position)

    def player_info(self):
        """
        Gets information about the currently playing track

        Returns:
        tuple formatted [progress, current_min, current_sec, current_uri]
        """
        result = self._sp.current_playback()
        progress = int(result["progress_ms"])
        current_min = int(result["progress_ms"] / 1000 / 60)
        current_sec = int(result["progress_ms"] / 1000 % 60)
        current_uri = result["item"]["uri"]
        return(progress, current_min, current_sec, current_uri)

    def pause(self, device):
        """
        Pause playback

        Paramaters:
        device - spotify device id to pause
        """
        self._sp.pause_playback(device)

    def resume(self, device):
        """
        Resume playback of current song

        Paramaters:
        device - the device id to resume to
        """
        info = self.player_info()
        self.play(device, [info[3]], info[0])

    def skip(self, device):
        """
        Skips to next song in queue

        Paramaters:
        device - the device to skip on
        """
        self._sp.next_track(device)

    def prev(self, device):
        """
        Moves to previous song

        Paramaters:
        device - the device to go back on
        """
        self._sp.previous_track(device)

    def queue(self, uri):
        """
        Adds a track to the queue

        Paramaters
        uri - the track uri to add to queue
        """
        self._sp.add_to_queue(uri, None)