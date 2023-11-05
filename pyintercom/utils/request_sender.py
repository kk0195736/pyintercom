import aiohttp
import sys

async def send_chime_request_async(chime_type):
    """
    チャイムAPIサーバにリクエストを飛ばす。
    """
    url = "http://localhost:5000/play-chime"
    payload = {"chimeType": chime_type}
    headers = {
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                print(f"Requested to play {chime_type} chime!")
            else:
                print(f"Failed to send request! Status code: {response.status}")
                print(await response.text())

async def send_capture_image_request_async(chime_type):
    """
    画像キャプチャAPIサーバにリクエストを飛ばす。
    """
    url = "http://localhost:8080/capture_image"
    payload = {"chimeType": chime_type}
    headers = {
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                print(f"Requested to capture {chime_type} image!")
            else:
                print(f"Failed to send request! Status code: {response.status}")
                print(await response.text())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python request_sender.py [delivery|visitor]")
        sys.exit(1)

    chime_type = sys.argv[1]

    if chime_type not in ["delivery", "visitor"]:
        print("Invalid chime type! Choose either 'delivery' or 'visitor'.")
        sys.exit(1)

    send_chime_request_async(chime_type)
