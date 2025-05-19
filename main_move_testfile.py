import time
from goolem_bot.gbot_lnx import *
from goolem_bot.gscreen_lnx import *
if __name__ == "__main__":

    gs=gScreen()
    gk=gKeyboard()
    gm=gMouse()
    gm.move(gs.findImageOnScreen("img/filetest.png"))
    gm.move(gs.findImageOnScreen("img/filetest_blue.png"))
    time.sleep(2)
    gm.press(button='left')
    time.sleep(2)
    gm.move(gs.findImageOnScreen("img/foldertest2.png"))
    time.sleep(2)
    gm.release(button='left')
    time.sleep(2)
    gm.move(gs.findImageOnScreen("img/filetest.png"))
    gm.move(gs.findImageOnScreen("img/filetest_blue.png"))
    time.sleep(2)
    gm.press(button='left')
    time.sleep(2)
    gm.move(gs.findImageOnScreen("img/foldertest.png"))
    time.sleep(2)
    gm.release(button='left')
    time.sleep(2)
