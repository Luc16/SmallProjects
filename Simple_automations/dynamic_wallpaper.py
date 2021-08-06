import cv2
import os
import queue
from time import sleep, time
import threading
q = queue.Queue()


def receive():
    url = "https://cdn.jmvstream.com/w/IPC-8597/camera.stream/playlist.m3u8"
    success = False
    fps = 15
    frame, cap = None, None
    while not success:
        cap = cv2.VideoCapture(url)
        success, frame = cap.read()
    q.put(frame)
    while True:
        initial_time = time()
        success, frame = cap.read()
        q.put(frame)
        if not success:
            print("not retrieving")
            cap.release()
            cap = cv2.VideoCapture(url)
            sleep(0.2)
        final_time = time() - initial_time
        if final_time < 1 / fps:
            sleep(1 / fps - final_time)


def display():
    filename = "/home/luc/Documents/Dynamic_Background_image/frame.jpg"
    while True:
        current_frame = q.get(block=True)
        try:
            cv2.imwrite(filename, current_frame)
        except cv2.error:
            pass
        cmd = "gsettings set org.gnome.desktop.background picture-uri file:" + filename
        os.system(cmd)


def main():
    p1 = threading.Thread(target=receive)
    p2 = threading.Thread(target=display)
    p1.start()
    p2.start()
    cmd = "gsettings set org.gnome.desktop.background picture-uri /usr/share/backgrounds/warty-final-ubuntu.png"
    os.system(cmd)


if __name__ == '__main__':
    main()
