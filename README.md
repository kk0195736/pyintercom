# pyintercom

`pyintercom`は、来客や配達員が来たときに特定のチャイム音を再生するAPIサーバーです。

## ディレクトリ構造

```
pyintercom/
├── LICENSE              # ライセンス情報
├── README.md            # このREADMEファイル
├── chime_sounds/        # チャイム音源ファイル
│   ├── delivery_chime.mp3  # 配達員が来た場合のチャイム音
│   └── visitor_chime.mp3   # 一般の来客用のチャイム音
├── pyintercom
│   ├── __init__.py         # パッケージ初期化ファイル
│   ├── chime_api_server.py # チャイムAPIサーバーのメインファイル
│   └── utils/              # ユーティリティモジュール
│       ├── __init__.py         # パッケージ初期化ファイル
│       └── audio_player.py     # MP3音源の再生機能
├── tools/               # pyintercomで使用するツール群
│ └── request_sender.py     # APIを叩くプログラム
└── requirements.txt      # 必要なPythonパッケージリスト
```

## インストール

1. このリポジトリをクローンします。

```bash
git clone [リポジトリのURL]
cd pyintercom
```

2. 必要なPythonパッケージをインストールします。

```bash
pip install -r requirements.txt
```

## 使用方法

1. APIサーバーを起動します。

```bash
python pyintercom/chime_api_server.py
```

2. APIサーバーが起動している状態で、POSTリクエストを送信してチャイム音を再生します。

- 配達員が来た場合のチャイム音:

```bash
python tools/request_sender.py delivery
```

- 一般の来客用のチャイム音:

```bash
python tools/request_sender.py visitor
```

## ライセンス

詳細は[LICENSE](LICENSE)を参照してください。

---

# pyintercom (English)

`pyintercom` is an API server that plays specific chime sounds when visitors or delivery personnel arrive.

## Directory Structure

```
pyintercom/
├── LICENSE              # License information
├── README.md            # This README file
├── chime_sounds/        # Chime sound files
│   ├── delivery_chime.mp3  # Chime for when a delivery person arrives
│   └── visitor_chime.mp3   # Chime for general visitors
├── pyintercom
│   ├── __init__.py         # Package initialization file
│   ├── chime_api_server.py # Main file for the chime API server
│   └── utils/              # Utility modules
│       ├── __init__.py         # Package initialization file
│       └── audio_player.py     # MP3 audio playback function
├── tools/               # Tools used by pyintercom
│ └── request_sender.py     # Programs that call the API
└── requirements.txt      # List of required Python packages
```

## Installation

1. Clone this repository.

```bash
git clone [repository URL]
cd pyintercom
```

2. Install the necessary Python packages.

```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server.

```bash
python pyintercom/chime_api_server.py
```

2. With the API server running, send a POST request to play a chime sound.

- Chime for when a delivery person arrives:

```bash
python tools/request_sender.py delivery
```

- Chime for general visitors:

```bash
python tools/request_sender.py visitor
```

## License

Please refer to the [LICENSE](LICENSE) for details.
