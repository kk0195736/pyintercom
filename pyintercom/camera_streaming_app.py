import os
from dotenv import load_dotenv
import cv2
import aiohttp
import aiofiles
from flask import Flask, Response, render_template, jsonify
import threading
import datetime

# 環境変数をロード
load_dotenv()

# 定数
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
CAMERA_DEVICE_ID = 0
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_FPS = 30

app = Flask(__name__)

camera = None
latest_camera_frame = None


def initialize_camera():
    """
    指定された設定でカメラを初期化およびセットアップします。
    """
    global camera
    camera = cv2.VideoCapture(CAMERA_DEVICE_ID)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)


def update_camera_frame():
    """
    バックグラウンドでカメラフレームを継続的に更新します。
    カメラへのアクセス中にエラーが発生した場合、ループが中断します。
    """
    global latest_camera_frame
    while True:
        try:
            success, frame = camera.read()
            if not success:
                print("Failed to read from the camera.")
                break  # Optionally, consider adding a sleep and retry logic
            latest_camera_frame = frame
        except Exception as e:
            print(f"Error accessing camera: {e}")
            break


# カメラフレームの更新を開始するためのスレッド
camera_update_thread = threading.Thread(target=update_camera_frame)
camera_update_thread.start()

def save_captured_image(frame):
    """
    タイムスタンプを基にしたファイル名でキャプチャしたフレームを画像として保存します。

    :param frame: 保存するキャプチャフレーム。
    :return: 保存された画像へのパスまたはエラーが発生した場合はNone。
    """
    now = datetime.datetime.now()
    image_path = "./images/" + now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    try:
        cv2.imwrite(image_path, frame)
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
    return image_path


async def send_line_notify_with_image(message, image_filename):
    """
    LINE Notifyを使用して画像付きのメッセージをLINEに送信します。

    :param message: 送信するメッセージ。
    :param image_filename: 送信する画像へのパス。
    """
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + LINE_NOTIFY_TOKEN}
    payload = {"message": message}

    async with aiofiles.open(image_filename, "rb") as f:
        image_data = await f.read()

    files = {"imageFile": image_data}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=payload, files=files) as response:
                response.raise_for_status()  # Check for HTTP errors
        except aiohttp.ClientError as e:
            print(f"Error sending image to LINE Notify: {e}")


async def capture_image_and_notify(flag):
    """
    カメラから画像をキャプチャし、フラグに基づいて通知を送信します。

    :param flag: 送信する通知メッセージのタイプを決定します。
    """
    try:
        success, frame = camera.read()
        if not success:
            print("Failed to capture an image from the camera.")
            return
        image_filename = save_captured_image(frame)
        if not image_filename:
            print("Failed to save the captured image.")
            return
        messages = {
            1: "配達員が来ました。",
            2: "配達員以外の誰かが来ました。",
            3: "現在の状況を撮影しました。"
        }
        await send_line_notify_with_image(messages.get(flag, "不明な状況"), image_filename)
    except Exception as e:
        print(f"Unexpected error: {e}")




@app.route("/")
def index():
    """メインページをレンダリングします。"""
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    """
    ストリーミングのためのビデオフレームをフィードとして提供します。

    :return: ストリームされたビデオフレーム。
    """

    def generate_frames():
        while True:
            success, frame = camera.read()
            if success:
                ret, jpeg = cv2.imencode(".jpg", frame)
                if ret:
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + jpeg.tobytes()
                        + b"\r\n\r\n"
                    )

    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/capture_delivery", methods=["GET", "POST"])
async def capture_delivery_image():
    """配達員が到着したときの画像をキャプチャします。"""
    await capture_image_and_notify(1)
    return jsonify({"message": "画像を保存しました"})


@app.route("/capture_visitor", methods=["GET", "POST"])
async def capture_visitor_image():
    """訪問者が到着したときの画像をキャプチャします。"""
    await capture_image_and_notify(2)
    return jsonify({"message": "画像を保存しました"})


@app.route("/capture_current", methods=["POST"])
async def capture_current_situation_image():
    """現在の状況の画像をキャプチャします。"""
    await capture_image_and_notify(3)
    return "現在の状況を撮影しました。"


if __name__ == "__main__":
    initialize_camera()
    app.run(host="0.0.0.0", port=8080, threaded=True)
