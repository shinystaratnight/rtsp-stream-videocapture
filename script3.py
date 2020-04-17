import vlc
import time

player = vlc.MediaPlayer('rtsp://174.0.247.195:554/1/')
player.play()

while 1:
    time.sleep(1)
    player.video_take_snapshot(0, '111.jpg', 0, 0)