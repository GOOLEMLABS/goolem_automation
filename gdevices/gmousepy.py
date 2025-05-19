
from ctypes import *
import time
#import ctypes

#ctypes gmouse wrapper
#g++ gmouse_x11.c -o libgmouse_x11.so -lX11

#libgmouse_x11 = cdll.LoadLibrary('/home/goolem/goolemlabs/gdevices/libgmouse_x11.so')
libgmouse_x11 = cdll.LoadLibrary('/home/goolem/goolemlabs/gdevices/libgmouse_xt.so')
class glibmouse():
    def __init__(self):
        if libgmouse_x11.initialize_x() != 0:
            print("Error al inicializar la conexión X")
            exit()
            
    def __del__(self):
        time.sleep(0.1)
        libgmouse_x11.close_x()
        print("Conexión X cerrada")
    def mouse_move(self,point):
        mouse_move = libgmouse_x11.mouse_move_extern
        mouse_move.argtypes=[c_int,c_int] #int _X, int _Y
        mouse_move(point[0], point[1], 1)
        time.sleep(0.1)

    def mouse_event(self,_BUTTON,_iISPRESS):
        mouse_event = libgmouse_x11.mouse_event_extern
        mouse_event.argtypes=[c_uint,c_int] #int _X, int _Y, int _BUTTON,int _ISPRESS,
        mouse_event( _BUTTON, _iISPRESS)
        time.sleep(0.1)




if __name__ == "__main__":
    gm = glibmouse().mouse_move([26,1066])
    time.sleep(1)
    print("1")
    gm = glibmouse().mouse_event( 1,1)
    gm = glibmouse().mouse_event( 1,0)



