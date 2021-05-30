import cv2
import os
from time import sleep, time


def main():
    initial_url = "https://cdn.jmvstream.com/w/IPC-8597/camera.stream/media-ue93wluap_"
    stream_num = 2800
    url = initial_url + f"{stream_num}.ts"
    cap = cv2.VideoCapture(url)

    print("--- Conectando... ---")
    while not cap.isOpened():
        stream_num += 1
        url = initial_url + f"{stream_num}.ts"
        cap = cv2.VideoCapture(url)
        if stream_num > 9999:
            return

    stream_num += 10
    url = initial_url + f"{stream_num}.ts"
    cap = cv2.VideoCapture(url)
    stream_num += 1
    url = initial_url + f"{stream_num}.ts"
    cap1 = cv2.VideoCapture(url)

    print("--- Conexão estabelecida!! ---")
    while True:
        try:
            initial_time = time()
            # Capture frame-by-frame
            ret, current_frame = cap.read()
            if current_frame is None:
                stream_num += 1
                cap = cap1
                url = initial_url + f"{stream_num}.ts"
                cap1 = cv2.VideoCapture(url)
                ret, current_frame = cap.read()
                if current_frame is None:
                    count = 0
                    stream_num -= 1
                    while not cap.isOpened():
                        count += 1
                        url = initial_url + f"{stream_num}.ts"
                        cap = cv2.VideoCapture(url)
                        if cap.isOpened():
                            break
                        url = initial_url + f"{stream_num}.ts"
                        cap = cv2.VideoCapture(url)
                        if cap.isOpened():
                            break
                        url = initial_url + f"{stream_num}.ts"
                        cap = cv2.VideoCapture(url)

                        if stream_num > 999:
                            return
                print(stream_num)

            filename = "/home/luc/Documents/Dynamic_Background_image/frame.jpg"
            try:
                cv2.imwrite(filename, current_frame)
            except cv2.error as e:
                print(e)

            cmd = "gsettings set org.gnome.desktop.background picture-uri file:" + filename
            os.system(cmd)
            final_time = time() - initial_time
            if final_time < 1 / 15:
                sleep(1 / 15 - final_time)
        except KeyboardInterrupt:
            break

    # release the capture
    cap.release()
    cv2.destroyAllWindows()
    cmd = "gsettings set org.gnome.desktop.background picture-uri /usr/share/backgrounds/warty-final-ubuntu.png"
    os.system(cmd)


if __name__ == '__main__':
    main()
