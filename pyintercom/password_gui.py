import tkinter as tk
import threading
import os
from dotenv import load_dotenv
from key_opener import key_opening_procedure


# .envファイルから環境変数を読み込む
load_dotenv()
PASSWORD = os.getenv("PASSWORD")

def create_label(root, text, font_size):
    """指定された設定でラベルを作成し、中央に配置する関数"""
    label = tk.Label(root, text=text, font=("", font_size))
    label.pack(anchor="center", expand=1)
    return label


def display_password_stars(pass_input_length):
    """入力されたパスワードの文字数に応じて星（＊）を表示する関数"""
    star_positions = {
        1: "＊            ",
        2: "＊   ＊        ",
        3: "＊   ＊   ＊    ",
        4: "＊   ＊   ＊   ＊"
    }
    return star_positions.get(pass_input_length, "             ")


def key_handler(e, pass_input, label2, label3, root):
    """
    キー入力イベントのハンドラ。入力されたキーに応じて動作を制御する。

    Parameters:
    - e: キーイベント
    - pass_input: ユーザーからの入力を保存するリスト
    - label2: 入力状況を表示するラベル
    - label3: 結果（OPEN or FAILED）を表示するラベル
    - root: tkinterのメインウィンドウ
    """
    pass_input.append(e.char)
    password_stars_label["text"] = display_password_stars(len(pass_input))
    if len(pass_input) == 4:
        if pass_input == list(PASSWORD):
            result_label["text"] = "OPEN"
            thread1 = threading.Thread(target=key_opening_procedure)
            thread1.start()
            root.after(3000, lambda: root.destroy())
        else:
            result_label["text"] = "FAILED"
            root.after(1000, lambda: root.destroy())


def pass_screen():
    """
    暗証番号の入力画面を表示する関数
    """
    global root, password_stars_label, result_label

    pass_input = []

    root = tk.Tk()
    root.title("暗証番号")
    root.geometry("1000x300+460+390")

    # ラベルの作成
    instruction_label = create_label(root, "パスワードを入力してください。", 30) # 指示メッセージ
    password_stars_label = create_label(root, "             ", 30)                # 入力されたパスワードの＊表示
    result_label = create_label(root, "", 30)                                     # 結果表示（OPEN/FAILED）

    root.bind("<KeyPress>", key_handler)

    # 30秒後にウインドウを閉じる
    root.after(30000, lambda: root.destroy())
    root.mainloop()


if __name__ == "__main__":
    pass_screen()
