import requests
import sys

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
