import asyncio
import tkinter as tk
from utils import show_message, send_chime_request_async, send_capture_image_request_async

async def send_request(chime_type):
    """
    カメラとチャイムのAPIを叩く
    """
    await asyncio.gather(
        send_capture_image_request_async(chime_type),
        send_chime_request_async(chime_type)
    )
    show_message("メッセージ", "只今呼び出し中です。少々お待ちください。")

def on_key(event):
    """
    キー入力イベントのハンドラ
    """
    if event.char == '1':
        send_request("delivery")
    elif event.char == '2':
        send_request("visitor")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("インターホン")
    window.geometry("1000x300+460+390")

    message = "配達員の方は「１」を押してください。\nそれ以外の方は「２」を押してください。"
    label = tk.Label(window, text=message, font=("", 30))
    label.pack(anchor="center", expand=1)

    window.bind("<Key>", on_key)

    window.mainloop()
