import pygame

# pygame mixer の初期化
pygame.mixer.init()

def play_sound(filename):
    """MP3ファイルを再生する関数"""
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
