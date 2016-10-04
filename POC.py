__author__ = 'orenko, dango'


from selenium import webdriver
import time
import pyautogui as ag


ROOT_URL_HOT = "http://www.hot.net.il/heb/Internet/speed/"
COORDS = (500, 670)
CROP_COORDS = (300, 630) 
STD_SLEEP = 1.5
SHORT_SLEEP = 0.6
LONG_SLEEP = 30
BOX_DRAG = 150


def open_target(root_url):
    driver = webdriver.Firefox()
    driver.get(root_url)
    puppeteer_sys()
    print "done"
    return


def puppeteer_sys():
    ag.moveTo(*COORDS)
    ag.keyDown("f11")
    ag.click()
    ag.moveTo(*CROP_COORDS)
    time.sleep(LONG_SLEEP)
    ag.keyDown("printscreen")
    ag.hotkey("Win")
    ag.hotkey("s")
    ag.hotkey("n")
    ag.hotkey("i")
    time.sleep(SHORT_SLEEP)
    ag.hotkey("enter")
    time.sleep(SHORT_SLEEP)
    ag.hotkey("ctrl")
    ag.hotkey("n")
    time.sleep(SHORT_SLEEP)
    ag.dragRel(BOX_DRAG, BOX_DRAG, 1, button='left')
    time.sleep(STD_SLEEP)
    ag.hotkey("ctrl", "s")
    time.sleep(STD_SLEEP)
    ag.hotkey("ctrl", "enter")
    time.sleep(STD_SLEEP)
    ag.hotkey("left")
    time.sleep(SHORT_SLEEP)
    ag.hotkey("enter")
    ag.hotkey("alt", "f4")


if __name__=='__main__':
    open_target(ROOT_URL_HOT)
