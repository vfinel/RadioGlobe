import vlc
import time


def test_pause():
    # creating a media player object
    media_player = vlc.MediaListPlayer()

    # creating Instance class object
    player = vlc.Instance()

    # creating a new media list object
    media_list = player.media_list_new()

    # creating a new media
    media = player.media_new("radio-fx/radio-fx.wav")

    # adding media to media list
    media_list.add_media(media)

    # setting media list to the media player
    media_player.set_media_list(media_list)

    # start playing
    media_player.play()

    print("playing for 5 seconds...")
    # wait so the video can be played for 5 seconds
    # irrespective for length of video
    time.sleep(5)

    # pausing media
    print("pausing for 4 seconds...")
    media_player.set_pause(1)

    # wait for 4 second
    # so that it remained paused for 4 seconds
    time.sleep(4)

    print("playing for 1 second...")
    media_player.set_pause(0)
    time.sleep(1)


def test_state():
    media_player = vlc.MediaListPlayer()
    url = "http://emisoras.dip-badajoz.es:8022/stream"

    player = vlc.Instance()
    media_list = player.media_list_new()
    media = player.media_new(url)
    media_list.add_media(media)
    media_player.set_media_list(media_list)

    # start playing
    media_player.play()

    print("playing for 5 seconds...")
    for i in range(10):
        media_state = media_player.get_state()
        print(f"{media_state = }")
        time.sleep(1)


if __name__ == "__main__":
    # test_pause()
    test_state()
    print("exiting program")
