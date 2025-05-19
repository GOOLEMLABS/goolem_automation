
from ctypes import *
import time
#import ctypes

#ctypes gmouse wrapper
#g++ gmouse_x11.c -o libgmouse_x11.so -lX11
#g++ gkeyboard_xt.c -o libgkeyboard_xt.so -lX11
libgkeyboard_x11 = cdll.LoadLibrary('/home/goolem/goolemlabs/gdevices/libgkeyboard_xt.so')

class glibkeyboard():
    def __init__(self):
        if libgkeyboard_x11.initialize_x_keyboard() != 0:
            print("Error al inicializar la conexión X para el teclado")
            exit()

    def __del__(self):
        libgkeyboard_x11.close_x_keyboard()
        print("Conexión X para el teclado cerrada")

    def keyboard_press(self, keyword):
        keyboard_press = libgkeyboard_x11.keyboard_press_extern
        keyboard_press.argtypes = [c_char_p]
        keyboard_press.restype = c_int
        keyword_bytes = keyword.encode('utf-8')
        result = keyboard_press(keyword_bytes)
        if result != 0:
            print(f"Error al presionar la tecla: {keyword}")
        time.sleep(0.1)

    def keyboard_release(self, keyword):
        keyboard_release = libgkeyboard_x11.keyboard_release_extern
        keyboard_release.argtypes = [c_char_p]
        keyboard_release.restype = c_int
        keyword_bytes = keyword.encode('utf-8')
        result = keyboard_release(keyword_bytes)
        if result != 0:
            print(f"Error al soltar la tecla: {keyword}")
        time.sleep(0.1)

    def keyboard_press_and_release(self, keyword):
        keyboard_press_and_release = libgkeyboard_x11.keyboard_press_and_release_extern
        keyboard_press_and_release.argtypes = [c_char_p]
        keyboard_press_and_release.restype = c_int
        keyword_bytes = keyword.encode('utf-8')
        result = keyboard_press_and_release(keyword_bytes)
        if result != 0:
            print(f"Error al presionar y soltar la tecla: {keyword}")
        time.sleep(0.1)

if __name__ == "__main__":
    gk = glibkeyboard() # Inicializar la conexión

    print(" tecla 'Return'")
    gk.keyboard_press_and_release("www.b.")
    time.sleep(1)

 