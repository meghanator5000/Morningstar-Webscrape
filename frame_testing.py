import json
from queue import Empty
import time
import multiprocessing as mp
import sys
import os
import glob
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,StaleElementReferenceException,TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# generate details json
DETAILS_JSON_FILE = "links.json"

# load cusip_list json dictionary
with open('cusip_list.json') as json_file:
    cusip_list = json.load(json_file)

# execute driver as function   
def new_driver():
    driver = webdriver.Chrome(executable_path=r"/Users/meghanmokate/Desktop/dated date/chromedriver 2")
    driver.maximize_window()  # maximize so all elements are clickable
    return driver

# find CUSIP to search for from cusip list
def search_CUSIP(driver, i):
    try:
        search_bar = driver.find_element_by_id('ms-finra-autocomplete-box')
        search_bar.send_keys(cusip_list[i]['CUSIP'])
        search_bar.send_keys(Keys.RETURN)
    except Exception as e:
        print(e)    

def get_link(driver, cusip_index):
    details = [] 
    time.sleep(2)
    cusip = cusip_list[cusip_index]["CUSIP"]
    try:
        iframe = driver.find_element_by_css_selector('#ms-bond-detail-iframe')
    except:
        print('frame not found')
    try:
        iframe_link = iframe.get_attribute('src')
    except:
        print('link not found')
    detail = {
            "CUSIP": cusip, 
            "Frame Link": iframe_link
        }
    details.append(detail)
    return details

# execute functions on webpage
if __name__ == "__main__":
    details = [] 
    driver = new_driver()
    for i in range(len(cusip_list)):
        # every 10 cusip write to json to see if it's working
        if i % 10 == 0:
            print("writing latest version of details to json", i)
            # overwrite to result file using the 'w' flag
            details_json_file = open(DETAILS_JSON_FILE, 'w')
            json.dump(details, details_json_file, indent=4)    
            details_json_file.close()
        # add in functions
        driver.get("http://finra-markets.morningstar.com/BondCenter/BondDetail.jsp?ticker=M16917827153779&symbol=")
        try:
            search_CUSIP(driver, i)
            details.extend(get_link(driver, i))
        except:
            details.extend(get_link(driver, i))
         
    # try:
    #     with open(DETAILS_JSON_FILE) as details_json_file:
    #         details = json.load(details_json_file)
    #         if details is None or len(details) == 0:
    #             raise FileNotFoundError
    # except (FileNotFoundError, json.decoder.JSONDecodeError):
    #     print(f"no {DETAILS_JSON_FILE}...scraping website for new data")

    with open(DETAILS_JSON_FILE, 'w') as details_json_file:
        json.dump(details, details_json_file, indent=4)

    print("all details processes done")