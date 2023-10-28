import serial
from time import sleep

# 定数
SW_OPEN = (0xA0, 0x01, 0x01, 0xA2)
SW_CLOSE = (0xA0, 0x01, 0x00, 0xA1)
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
DELAY = 0.35

def initialize_serial_port():
    """
    シリアルポートを初期化し、それを返します。
    """
    return serial.Serial(SERIAL_PORT, BAUD_RATE)


def open_key(serial_port):
    """
    与えられたシリアルポートを使用して鍵を開きます。
    """
    serial_port.write(SW_OPEN)
    sleep(DELAY)
    serial_port.write(SW_CLOSE)
    sleep(DELAY)


def key_opening_procedure():
    """
    鍵を開ける手続きを行う関数
    """
    with initialize_serial_port() as port:
        open_key(port)


if __name__ == "__main__":
    # このスクリプトが直接実行された場合のみ、以下のコードを実行
    key_opening_procedure()
