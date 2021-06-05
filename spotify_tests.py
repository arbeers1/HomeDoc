import sys

import spotipy
sys.path.insert(1, sys.path[0].replace("tests", "\\src", 1))
from configurator import configurator
from spotify import spotify

config = configurator()
spot = spotify(config.secret)

def test_music():
    results = spot.music()
    assert(results[0][0] == "Liked Songs")
    #These lines is dependent on the user and playlist order
    assert(results[1][1] == "34pwxTfFmtSmZI14D077YG")
    assert(len(results) == 3)

def test_tracks():
    #User dependent
    results = spot.tracks("34pwxTfFmtSmZI14D077YG")
    assert(len(results) == 20)
    assert(results[0][0] == "Mr. Right Now (feat. Drake)")

def test_search():
    #Time dependent test. May fail as relevance of songs change.
    results = spot.search("Ice Water")
    assert(len(results) == 10)
    assert(results[0][0] == "Ice Water (feat. Trippie Redd)")

def test_devices():
    #Make sure another device is online and discoverable to view
    print(spot.devices())

def test_play():
    #Must be connected to a spotify device
    spot.play(spot.devices()[0][1], [spot.search("Ice Water")[0][2]], None)

def test_playback():
    #Consider playing a song while testing this method and see if time matches up
    print(spot.player_info())

def test_pause():
    #Verify music pauses on device
    spot.pause(spot.devices()[0][1])

def test_resume():
    #Verify music resumes on device
    spot.resume(spot.devices()[0][1])

def test_skip():
    #Verify device skips to next song
    spot.skip(spot.devices()[0][1])

def test_prev():
    #Verify device moves to prev song
    spot.prev(spot.devices()[0][1])

def test_queue():
    spot.queue(spot.tracks("34pwxTfFmtSmZI14D077YG")[0][2])

#test_music()
#test_tracks()
#test_search()
#test_devices()
#test_play()
#test_playback()
#test_pause()
#test_resume()
#test_skip()
#test_prev()
test_queue()