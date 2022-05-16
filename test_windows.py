import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import redis
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from parser import Parser
from imagePreparator import ImagePreparator
import json

def  parse_photo():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("window-size=1920,1080")
        options.add_argument('--log-level=3')
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        webd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wd = Parser(webd)
        wd.openPage('https://alerts.in.ua/')
        wd.setLocalStorage('darkMode', 'true')
        wd.setLocalStorage('liteMap', 'false')
        wd.wait('//div[@id="map"]/*[name()="svg"]/*[name()="g"]//*[@id="a"]')
        time.sleep(1)
        wd.getImage('screenshot.png')
        image = ImagePreparator()
        image.cutImage('screenshot.png')
    except Exception as ex:
        with open('log/parser-log.txt', 'a') as file:
            file.write(str(ex))

def parse_info():
    try:
        start_time = datetime.now()
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        webd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wd1 = Parser(webd)
        wd1.openPage('https://alarmmap.online/')
        regions = wd1.getRegions() 
        print(datetime.now() - start_time)
        # print(regions)
        
        return regions
    except Exception as ex:
        with open('log/parser-log.txt', 'a') as file:
            file.write(str(ex))

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