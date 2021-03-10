from urllib.request import urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse

import keyboard
import time
import os

search_query = input("검색어: ")
generated_search_query = parse.quote(search_query)
scroll_goal = int(input("스크롤 횟수: "))

chrome_webdriver_path = "chromedriver.exe"
chrome_webdriver_options = webdriver.ChromeOptions()
# chrome_webdriver_options.add_argument("--window-size=1280,720")

chrome_webdriver = webdriver.Chrome(executable_path=chrome_webdriver_path, options=chrome_webdriver_options)
chrome_webdriver.get(url="https://www.pinterest.co.kr/")

login_btn = chrome_webdriver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]")
login_btn.click()

fb_login_button = chrome_webdriver.find_element_by_xpath(
    "/html/body/div[1]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/div[1]/div[1]/div/button")
fb_login_button.click()

while True:
    if keyboard.is_pressed("return"):
        time.sleep(5)
        break

chrome_webdriver.get(url=f"https://www.pinterest.co.kr/search/pins/?q={generated_search_query}")
time.sleep(2)

img_srcs = list()
last_height = chrome_webdriver.execute_script("return document.body.scrollHeight")
for scroll_cnt in range(scroll_goal):
    time.sleep(1.5)
    soup = BeautifulSoup(chrome_webdriver.page_source, "html.parser")
    img_tags = soup.find_all("img")
    for img_tag in img_tags:
        img_src = img_tag.get("src")
        if (img_src in img_srcs) is False:
            img_srcs.append(img_src)

    print(f"scroll_cnt: {scroll_cnt}")
    chrome_webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    current_height = chrome_webdriver.execute_script("return document.body.scrollHeight")
    if current_height == last_height:
        time.sleep(2)
        chrome_webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        current_height = chrome_webdriver.execute_script("return document.body.scrollHeight")
        if current_height == last_height:
            break

    last_height = chrome_webdriver.execute_script("return document.body.scrollHeight")

if os.path.exists(f"./{search_query}") is False:
    os.mkdir(f"./{search_query}")
for img_number, img_src in enumerate(img_srcs):
    separated_url = img_src.rsplit(sep="/", maxsplit=2)
    img_name = separated_url[-1]
    ext = os.path.splitext(img_name)[-1]
    print(f"{img_number}: {img_src}")
    urlretrieve(img_src, filename=f"./{search_query}/{search_query}_{img_number}{ext}")

chrome_webdriver.close()
