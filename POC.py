__author__ = 'orenko, dango'


from selenium import webdriver
import time
import re
from random import randint
from selenium.common.exceptions import *
import os
from selenium.common.exceptions import WebDriverException
import pyautogui as ag
from PIL import ImageGrab

ROOT_URL_HOT = "http://www.hot.net.il/heb/Internet/speed/"
COORDS = (500, 670)
CROP_COORDS = (300, 630) 
STD_SLEEP = 3
SHORT_SLEEP = 0.6


JS_GET_COORDS=\
"""
var cursorX;
var cursorY;
document.onclick = function(e){
    cursorX = e.pageX;
    cursorY = e.pageY;
}
setInterval(checkCursor, 1000);
function checkCursor(){
    alert("Cursor at: " + cursorX + ", " + cursorY);
}
"""
#
# chromedriver = "/Users/orenko/Downloads/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver


def open_target(root_url):
    # driver = webdriver.Chrome("C:\Users\orenko\Downloads\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Firefox()
    driver.get(root_url)
    current = driver.find_element_by_class_name("current")

    like = driver.find_elements_by_tag_name('div')
    ag.moveTo(*COORDS)
    ag.keyDown("f11")
    ag.click()
    # time.sleep(1)
    ag.moveTo(*CROP_COORDS)
    time.sleep(28)
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
    time.sleep(0.1)
    ag.dragRel(150, 150, 1, button='left')
    time.sleep(STD_SLEEP)
    ag.hotkey("ctrl", "s")
    time.sleep(STD_SLEEP)
    ag.hotkey("ctrl", "enter")
    time.sleep(STD_SLEEP)
    ag.hotkey("left")
    time.sleep(SHORT_SLEEP)
    ag.hotkey("enter")
    # import gtk
    # clipboard = gtk.clipboard_get()
    # image = clipboard.wait_for_image()
    # if image is not None:
    #     image.save(fname, "png")
    #     print "PNG image saved to file", fn

    # im = ImageGrab.grabclipboard()
    # print im._bitmap()
    # with open("snapshot.png", "wb") as f:
    #     im.save(f)

    # # time.sleep(30)
    # png = driver.get_screenshot_as_png()
    # # print type(png)
    # write_pic(png, "snapshot.png")
    print "done"
    # ag.keyDown("f11")
    return


def write_pic(png, filename):
    with open(filename, 'wb') as f:
        f.write(png)


def crop_flash_element(flash_elem, driver):
    coordinates = flash_elem.get_location()
    png = driver.get_screenshot_as_png()
    write_pic(png, "snapshot.png")


if __name__=='__main__':
    open_target(ROOT_URL_HOT)
