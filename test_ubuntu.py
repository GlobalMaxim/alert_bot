import asyncio
from re import A
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from parser import Parser
from imagePreparator import ImagePreparator
import json
import os

def  parse_photo():
    os.environ['DISPLAY'] = ':10.0'
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9230")
   # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    webd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
   # webd = webdriver.Chrome(executable_path='/usr/local/lib/chromedriver', options=options)
    
    wd = Parser(webd)
    wd.openPage('https://alerts.in.ua/')
    wd.setLocalStorage('darkMode', 'true')
    wd.setLocalStorage('liteMap', 'false')
    wd.wait('//div[@id="map"]/*[name()="svg"]/*[name()="g"]//*[@id="a"]')
    wd.getImage('screenshot.png')
    image = ImagePreparator()
    image.cutImage('screenshot.png')
    webd.stop_client()
    webd.close()
    webd.quit()
    #Service(ChromeDriverManager().install()).stop()
def parse_info():
    start_time = datetime.now()
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("window-size=1920,1080")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    webd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wd1 = Parser(webd)
    wd1.openPage('https://alarmmap.online/')
    regions = wd1.getRegions() 
    print(datetime.now() - start_time)
    # print(regions)
    
    return regions

def api_parse_info():
    regions = {}
    headers = {
         "X-API-Key": "4083272368ae9c7a6912cf489ec087de8b162cfd"
    }
    url = 'https://alerts.com.ua/api/states'
    req = requests.get(url, headers=headers)
    res = json.loads(req.text)
    for i in res["states"]:
        if i['alert'] == True:
            name = i['name']
            clear_date = datetime.fromisoformat(i['changed']).strftime("%H:%M %d-%m-%Y")
            regions[name] = clear_date
    return regions

def main():
    # parse_info()
    parse_photo()
    # api_parse_info()

if __name__ == '__main__':
    main()
