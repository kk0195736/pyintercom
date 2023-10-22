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
curl -X POST -H "Content-Type: application/json" -d '{"chimeType": "delivery"}' http://[サーバーのアドレス]:5000/play-chime
```

- 一般の来客用のチャイム音:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"chimeType": "visitor"}' http://[サーバーのアドレス]:5000/play-chime
```

## ライセンス

詳細は[LICENSE](LICENSE)を参照してください。
