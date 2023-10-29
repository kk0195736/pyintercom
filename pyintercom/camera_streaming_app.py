import os
from dotenv import load_dotenv
import cv2
import requests
from flask import Flask, Response, render_template, jsonify
import threading
import datetime

# Load environment variables
load_dotenv()

# Constants
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
CAMERA_DEVICE_ID = 1
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_FPS = 30

app = Flask(__name__)

camera = None
latest_camera_frame = None


def initialize_camera():
    """
    Initialize and set up the camera with the specified configurations.
    """
    global camera
    camera = cv2.VideoCapture(CAMERA_DEVICE_ID)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)


def update_camera_frame():
    """
    Continuously update the camera frame in the background.
    If an error occurs while accessing the camera, the loop breaks.
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


# Start the thread to update the camera frame
camera_update_thread = threading.Thread(target=update_camera_frame)
camera_update_thread.start()

def save_captured_image(frame):
    """
    Save the captured frame as an image with a timestamp-based filename.

    :param frame: Captured frame to be saved.
    :return: Path to the saved image or None if there's an error.
    """
    now = datetime.datetime.now()
    image_path = "./images/" + now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    try:
        cv2.imwrite(image_path, frame)
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
    return image_path


def send_line_notify_with_image(message, image_filename):
    """
    Send a message with an image to LINE using LINE Notify.

    :param message: Message to be sent.
    :param image_filename: Path to the image to be sent.
    """
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + LINE_NOTIFY_TOKEN}
    payload = {"message": message}
    files = {"imageFile": open(image_filename, "rb")}
    try:
        response = requests.post(url, headers=headers, params=payload, files=files)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error sending image to LINE Notify: {e}")


def capture_image_and_notify(flag):
    """
    Capture an image from the camera, save it, and send a notification based on the flag.

    :param flag: Determines the type of notification message to be sent.
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
        send_line_notify_with_image(messages.get(flag, "不明な状況"), image_filename)
    except Exception as e:
        print(f"Unexpected error: {e}")




@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    """
    Provide video frames as a feed for streaming.

    :return: Streamed video frames.
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
def capture_delivery_image():
    """Capture an image when a delivery person arrives."""
    capture_image_and_notify(1)
    return jsonify({"message": "画像を保存しました"})


@app.route("/capture_visitor", methods=["GET", "POST"])
def capture_visitor_image():
    """Capture an image when a visitor arrives."""
    capture_image_and_notify(2)
    return jsonify({"message": "画像を保存しました"})


@app.route("/capture_current", methods=["POST"])
def capture_current_situation_image():
    """Capture the current situation's image."""
    capture_image_and_notify(3)
    return "現在の状況を撮影しました。"


if __name__ == "__main__":
    initialize_camera()
    app.run(host="0.0.0.0", port=8080, threaded=True)
