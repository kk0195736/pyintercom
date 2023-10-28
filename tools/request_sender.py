import os
import requests
import sys
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# LINE NotifyのAPIのURL
LINE_NOTIFY_API_URL = "https://notify-api.line.me/api/notify"
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

def send_line_notify_with_image(message, image_filename):
    """
    LINE Notify を使ってメッセージを送信する。
    画像ファイルも一緒に送信する。

    Parameters:
    - message: 送信するメッセージ内容
    - image_filename: 送信する画像のファイル名
    """
    url = "https://notify-api.line.me/api/notify"
    token = os.getenv("LINE_NOTIFY_TOKEN")
    headers = {"Authorization": "Bearer " + token}

    payload = {"message": message}
    files = {"imageFile": open(image_filename, "rb")}

    requests.post(url, headers=headers, params=payload, files=files)

def send_chime_request(chime_type):
    url = "http://localhost:5000/play-chime"
    payload = {"chimeType": chime_type}
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Requested to play {chime_type} chime!")
    else:
        print(f"Failed to send request! Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python request_sender.py [delivery|visitor]")
        sys.exit(1)

    chime_type = sys.argv[1]

    if chime_type not in ["delivery", "visitor"]:
        print("Invalid chime type! Choose either 'delivery' or 'visitor'.")
        sys.exit(1)

    send_chime_request(chime_type)
