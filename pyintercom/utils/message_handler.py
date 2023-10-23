import tkinter as tk


def show_message(title, txt):
    root = tk.Tk()
    root.title(title)
    root.geometry("1000x200+460+440")  # ウィンドウのサイズと位置を指定
    label = tk.Label(root, text=txt, font=("", 30))  # フォントサイズを30に指定
    label.pack(anchor="center", expand=1)
    root.after(5000, lambda: root.destroy())  # 5秒後にウィンドウを閉じる
    root.mainloop()


if __name__ == "__main__":
    show_message("メッセージ", "只今呼び出し中です。少々お待ちください。")
