from flask import Flask, request
import threading
import os
from utils import play_sound

app = Flask(__name__)

# 定数の定義
DELIVERY_PERSON_CHIME = 'delivery'
VISITOR_CHIME = 'visitor'
CHIME_SOUNDS_PATH = os.environ.get('CHIME_SOUNDS_PATH', '../chime_sounds/')

@app.route('/play-chime', methods=['POST'])
def handle_play_chime_request():
    """チャイム音の再生を制御するAPIエンドポイント"""
    chime_type = request.json.get('chimeType')

    # 対応するチャイム音のファイル名を取得
    sound_file_path = get_sound_file_path(chime_type)
    if not sound_file_path:
        return {'status': 'error', 'message': 'Invalid chimeType'}, 400

    # 並列処理でMP3ファイルを再生
    thread = threading.Thread(target=play_sound, args=(sound_file_path,))
    thread.start()

    return {'status': 'success'}, 200

def get_sound_file_path(chime_type):
    """チャイムの種類に対応する音源ファイルのパスを返す"""
    if chime_type == DELIVERY_PERSON_CHIME:
        return os.path.join(CHIME_SOUNDS_PATH, 'delivery_chime.mp3')
    elif chime_type == VISITOR_CHIME:
        return os.path.join(CHIME_SOUNDS_PATH, 'visitor_chime.mp3')
    return None

if __name__ == "__main__":
    HOST = os.environ.get('CHIME_API_HOST', '0.0.0.0')
    PORT = int(os.environ.get('CHIME_API_PORT', 5000))
    app.run(host=HOST, port=PORT)
