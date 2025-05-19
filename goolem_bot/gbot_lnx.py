#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#gbot ctypes from goolem linux os :/home/goolem/scripts# sh x11.sh
#140520251501

import faulthandler
faulthandler.enable()


####http://kbdlayout.info/kbdsp/virtualkeys

import base64
import os
from gdevices.gkeyboardpy import glibkeyboard
from gdevices.gmousepy import glibmouse
from goolem_bot.gscreen_lnx import *
import cv2
import time # opcional
import numpy
#from PIL import ImageGrab
#import gaux.hexkeycodes
import  ctypes
# import gaux.hexkeycodes
import ctypes
# pillow opencv-python numpy pip install numpy==1.19.3 pip install pywin32
import os
import time  # opcional
import numpy as np
import cv2
#from PIL import Image
import cv2
import numpy
import subprocess

#from PIL import ImageGrab


#clipboard


class gKeyboard():
    def __init__(self):
        self.gk=glibkeyboard()


    def combine(self,key1,key2):
        self.press(key1)
        self.click(key2)
        self.release(key1)

    def click(self,key):
        if key.isupper():
            self.shift_click(key)
        else:
            self.low_click(key)

    def low_click(self,key):
        key=key.upper()
        self.press_and_release(key)

    def shift_click(self,key):
        self.press('SHIFT')
        self.press_and_release(key)
        self.release('SHIFT')

    def type_string(self,text,wait=0.1):
        for k in text:
            self.gk.keyboard_press_and_release(self.get_keysym(k))
 
    def get_keysym(self, char):
        keysym_map = {
            '.': 'period',
            ' ': 'SPACE',
            ',': 'comma',
            ':': 'colon',
            '/': 'slash',
            '\\': 'backslash',
            '-': 'minus',
            '_': 'underscore',
            '=': 'equal',
            '+': 'plus',
            '!': 'exclam',
            '@': 'at',
            '#': 'numbersign',
            '$': 'dollar',
            '%': 'percent',
            '^': 'asciicircum',
            '&': 'ampersand',
            '*': 'asterisk',
            '(': 'parenleft',
            ')': 'parenright',
            ';': 'semicolon',
            '\'': 'apostrophe',
            '"': 'quotedbl',
            '<': 'less',
            '>': 'greater',
            '?': 'question',
            '[': 'bracketleft',
            ']': 'bracketright',
            '{': 'braceleft',
            '}': 'braceright',
            '\n': 'Return',  # Enter
            '\t': 'Tab',
            '\\x08': 'BackSpace',  # Borrar hacia atrás
            ' ': 'SPACE',
            ',': 'comma',
            '.': 'period',
            '/': 'slash',
            ';': 'semicolon',
            '\'': 'apostrophe',
            '[': 'bracketleft',
            ']': 'bracketright',
            '\\': 'backslash',
            '-': 'minus',
            '=': 'equal',
            '`': 'grave',
            '!': 'exclam',
            '@': 'at',
            '#': 'numbersign',
            '$': 'dollar',
            '%': 'percent',
            '^': 'asciicircum',
            '&': 'ampersand',
            '*': 'asterisk',
            '(': 'parenleft',
            ')': 'parenright',
            ':': 'colon',
            '"': 'quotedbl',
            '<': 'less',
            '>': 'greater',
            '?': 'question',
            '{': 'braceleft',
            '}': 'braceright',
            '|': 'bar',
            '_': 'underscore',
            '+': 'plus',
            '~': 'asciitilde',
            ' ': 'SPACE',
            'Left': 'Left',
            'Right': 'Right',
            'Up': 'Up',
            'Down': 'Down',
            'Home': 'Home',
            'End': 'End',
            'PageUp': 'Page_Up',
            'PageDown': 'Page_Down',
            'Insert': 'Insert',
            'Delete': 'Delete',
            'Shift_L': 'Shift_L',
            'Shift_R': 'Shift_R',
            'Control_L': 'Control_L',
            'Control_R': 'Control_R',
            'Alt_L': 'Alt_L',
            'Alt_R': 'Alt_R',
            'Caps_Lock': 'Caps_Lock',
            'Num_Lock': 'Num_Lock',
            'Scroll_Lock': 'Scroll_Lock',
            'Escape': 'Escape',
            'F1': 'F1',
            'F2': 'F2',
            'F3': 'F3',
            'F4': 'F4',
            'F5': 'F5',
            'F6': 'F6',
            'F7': 'F7',
            'F8': 'F8',
            'F9': 'F9',
            'F10': 'F10',
            'F11': 'F11',
            'F12': 'F12',
            # Añade más teclas especiales según necesites
        }
        return keysym_map.get(char, char) # Devuelve el Keysym o el propio carácter si no hay excepción



    def press(self,key):
        self.gk.keyboard_press(key)

    def release(self,key):
        self.gk.keyboard_release(key)

    def press_and_release(self,key):
        self.gk.keyboard_press_and_release(key)




class gcopy():
    def get_clipboard_text():
        user32.OpenClipboard(0)
        value=''
        try:
            if user32.IsClipboardFormatAvailable(CF_TEXT):
                data = user32.GetClipboardData(CF_TEXT)
                data_locked = kernel32.GlobalLock(data)
                text = ctypes.c_char_p(data_locked)
                value = text.value
                kernel32.GlobalUnlock(data_locked)

        finally:
            user32.CloseClipboard()
        print("find")
        return value




class gMouse():

    def click(self,button='left'):
        if button == 'left':
            self.press('left')
            self.release('left')
        if button == 'right':
            self.press('right')
            self.release('right')

    def press(self,button='left'):
        if button == 'left':
            glibmouse().mouse_event(1,1)
        if button == 'right':
            glibmouse().mouse_event(3,1)

    def release(self,button='left'):
        if button == 'left':
            glibmouse().mouse_event(1,0)
        if button == 'right':
            glibmouse().mouse_event(3,0)


    def move(self,point,delay=0.001):
        glibmouse().mouse_move(point)
        time.sleep(delay)
        #click()


class gScreen:
    def __init__(self):
        self.gm=gMouse()
        #sct.grab(sct.monitors[1])


    def get_clipboard_text(self):
        user32.OpenClipboard(0)
        value=''
        try:
            if user32.IsClipboardFormatAvailable(CF_TEXT):
                data = user32.GetClipboardData(CF_TEXT)
                data_locked = kernel32.GlobalLock(data)
                text = ctypes.c_char_p(data_locked)
                value = text.value
                print("value")
                kernel32.GlobalUnlock(data_locked)

        finally:
            user32.CloseClipboard()
        print("find")
        return value

    def findImageOnScreen(self,imgpath,sector=""):#,4points):
        #self.monitor = {"top": 40, "left": 0, "width": 2736, "height": 1824}
        #self.grab_screen()
        return self.matchTemplate(self.grab_screen(sector),imgpath) # return point 

    def wait_until_findIMageOnScreen(self,imgpath,sector="",seconds=5):
        print("wait until find")
        timeout = time.time() + seconds
        condition_met = False
        ret=False
        while time.time() < timeout:
            print("waiting")
            [x,y]=self.findImageOnScreen(imgpath,sector)
            if x!=None:
               
               condition_met = True
               break  # Exit the loop as the condition is true
            time.sleep(1)  # Wait for 0.1 seconds before checking again

        return condition_met

    def left_click_on_icon(self,imgpath_first,imgpath_sec='',sector='',wait_time=1):#sector as TL TR DL DW top left right ...
        #we have the option of sending two images. example: one to find an
        #icon or another to click on windows logo or changes dependind on web
        [x,y]=self.findImageOnScreen(imgpath_first,sector)
        print("left click on icon", x,y)
        enc=False
        if x!=None:
            print("move mouse ",x,y)
            self.gm.move(x,y)
            self.gm.click(button='left')
            enc= True
        if enc==False and imgpath_sec!='':
            [x,y]=self.findImageOnScreen(imgpath_sec,sector)
            if x!=None:
                self.gm.move(x,y)
                self.gm.click(button='left')
                enc= True
        print(imgpath_first,imgpath_sec,enc)
        return enc

    def grab_screen(self, sector):
        # mon = (0, 0, 1300, 900)
        wa=window_attributes()
        dwindow_attributes=wa.get_window_attributes()
        x=dwindow_attributes.width
        y=dwindow_attributes.height

        if sector == '':
            mon = (0, 0, x, y)  # screen size
        if sector == 'TL':  # TOP LEFT
            mon = (0, 0, x / 2, y / 2)
        if sector == 'TR':
            mon = (x / 2, 0, x, y / 2)
        if sector == 'DL':
            mon = (0, y / 2, x / 2, y)
        if sector == 'DR':
            mon = (x / 2, y / 2, x, y)
        print("screen size", mon)
        #img = numpy.asarray(ImageGrab.grab(bbox=mon).convert("RGBA"))  funciona en windows
        #img = numpy.asarray(ImageGrab.grab(bbox=mon).convert("RGB"))
        callscreen = subprocess.run(["goolem_bot/gscreenshot_lnx"], capture_output=True, text=True)

        img = cv2.imread('/dev/shm/gscreenshot.png',1)#colors
        #img=numpy.array(ImageGrab.grab(bbox=mon)).convert("RGB")
        #img = img.shape()

        # cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imwrite('grabbed_at_screen_pil.png', img)

        #arr = np.random.randint(0, 2 ** 16 - 1, (32, 64), dtype=np.uint16)  # or np.ones etc.

        #array_buffer = arr.tobytes()
        #img.frombytes(array_buffer, 'raw', "I;16")
        #img.save("16-bit_test_pillow.png")
        # cv2.imshow("pil test", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # time.sleep(10)
        return img




    def matchTemplate(self,img,imgpath) :  # return point 
        #img = numpy.array(sct.grab(monitor))
        try:
            if not os.path.isfile(imgpath):
                pass
        except:
            print("we can't find image at %s" % imgpath)
            raise
        print ( "loading image to find %s"%imgpath)
        imgtofind = cv2.imread(imgpath)#,cv2.CV_32F) -- checj this shit 
        try:
            cv2.imwrite('/dev/shm/imgtofind.png',imgtofind)
        except:
            print("can't find image ",imgtofind)
            quit()
        #imgtofind_1=numpy.asarray(imgtofind)
        #cv2.imwrite('imgtofind_1.png',imgtofind)
        cv2.imwrite('/dev/shm/img_1.png',img)
        res = cv2.matchTemplate(imgtofind,img,cv2.TM_SQDIFF)#cv2.TM_CCOEFF #cv2.TM_SQDIFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = min_loc
        h, w ,_= imgtofind.shape#[::-1]  #?[1::-1]#
        print("image to find shape ", w,h)
        bottom_right = (top_left[0] +w  , top_left[1] + h )
        print( min_loc, max_loc)
        print("top left 0 ",top_left[0]," w ",w, top_left[1],h)
        cv2.rectangle(img,(top_left[0], top_left[1]) ,(top_left[0]+ w,top_left[1]+ h),(255, 0, 0), -1)
        #reference cv2.rectangle(img, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (255, 0, 0), -1)
        #cv2.circle(image, center_coordinates,                         radius, color, thickness)
        cv2.circle(img, (int(top_left[0]+w/2), int(top_left[1]+h/2)), w, 255, 16)
        cv2.imwrite('/dev/shm/grabbed.png',img)
        print("found " ,int(top_left[0]+w/2),int(top_left[1]+h/2))
        #return center of the rectangle as an array point 
        return ([int(top_left[0]+w/2),int(top_left[1]+h/2)])


    def get_image_list_for_match(directorio: str) -> list:
        """
        Lista los nombres de los ficheros en un directorio de imagenes .

        :param directorio: Ruta del directorio a listar.
        :return: Lista de nombres de ficheros.
        """
        try:
            return [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]
        except Exception as e:
            print(f"Error al acceder al directorio: {e}")
            return []


if __name__ == "__main__":

    gs=gScreen()
    gk=gKeyboard()
    gk.define_hexkeycodes()


