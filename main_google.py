

from gbot.gbot import *
from botlibrary.library import *
#main whatsapp . for whatsapp automation pourposes

if __name__ == "__main__":
    #goolem init
    gs=gScreen()
    gk=gKeyboard()
    fb=firefox_browser()
#http://www.kbdedit.com/manual/low_level_vk_list.html
    if fb.browse("http://www.google.es") :
        time.sleep(2)
        if gs.left_click_on_icon('img/google_find.png'):
            time.sleep(2)
            gk.write("PEDRO LUIS GARCIA ALONSO")
            gk.press('RETURN')
