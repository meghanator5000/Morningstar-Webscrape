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
DETAILS_JSON_FILE = "details.json"

# load links_list json dictionary
with open('links.json') as json_file:
    links_list = json.load(json_file)

# execute driver as function   
def new_driver():
    driver = webdriver.Chrome(executable_path=r"/Users/meghanmokate/Desktop/dated date/chromedriver 2")
    driver.maximize_window()  # maximize so all elements are clickable
    return driver

def get_details(driver, link_index):
    details = [] 
    time.sleep(2)
    link = links_list[link_index]["Frame Link"] 
    cusip = links_list[link_index]["CUSIP"]
    try:
        cap_purpose = driver.find_element_by_css_selector('#msqt_issue > table > tbody:nth-child(3) > tr:nth-child(15) > td:nth-child(2)').text
    except: 
        cap_purpose = '-'
    try:
        collat_pledge = driver.find_element_by_css_selector('#msqt_issue > table > tbody:nth-child(3) > tr:nth-child(14) > td:nth-child(2)').text
    except: 
        collat_pledge = '-'
    try:
        use_proceeds = driver.find_element_by_css_selector('#msqt_classification > table > tbody > tr:nth-child(8) > td:nth-child(2)').text
    except: 
        use_proceeds = '-'
    try:
        coupon_type = driver.find_element_by_css_selector('#msqt_bond > table > tbody:nth-child(3) > tr:nth-child(5) > td:nth-child(2)').text
    except: 
        coupon_type = '-'
    try:
        bond_type = driver.find_element_by_css_selector('#msqt_classification > table > tbody > tr:nth-child(1) > td:nth-child(2)').text
    except: 
        bond_type = '-'
    try:
        sec_code = driver.find_element_by_css_selector('#msqt_classification > table > tbody > tr:nth-child(9) > td:nth-child(2)').text
    except: 
        sec_code = '-'
    try:
        fed_tax = driver.find_element_by_css_selector('#msqt_tax > table > tbody > tr:nth-child(1) > td:nth-child(2)').text
    except: 
        fed_tax = '-'
    try:
        state_tax = driver.find_element_by_css_selector('#msqt_tax > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
    except: 
        state_tax = '-'
    try:
        bank_qualified = driver.find_element_by_css_selector('#msqt_tax > table > tbody > tr:nth-child(3) > td:nth-child(2)').text
    except: 
        bank_qualified = '-'
    try:
        amt = driver.find_element_by_css_selector('#msqt_tax > table > tbody > tr:nth-child(4) > td:nth-child(2)').text
    except: 
        amt = '-'
    try:
        last_trade = driver.find_element_by_css_selector('#price').text
    except: 
        last_trade = '-'
    try:
        last_yield = driver.find_element_by_css_selector('#msqt_summary > div:nth-child(3) > table > tbody > tr > td:nth-child(2) > span').text
    except: 
        last_yield = '-'
    detail = { 
        "CUSIP": cusip, 
        "Link": link, 
        "Capital Purpose": cap_purpose,
        "Collateral Pledge": collat_pledge,
        "Use of Proceeds": use_proceeds,
        "Coupon Type": coupon_type,
        "Type of Bond": bond_type,
        "Security Code": sec_code,
        "Federal Tax": fed_tax,
        "State Tax": state_tax,
        "Bank Qualified": bank_qualified,
        "Alternative Minimum Tax": amt,
        "Last Trade Price": last_trade,
        "Last Yield Price": last_yield
        }
    details.append(detail)
    return details

# execute functions on webpage
if __name__ == "__main__":
    details = [] 
    driver = new_driver()
    for i in range(len(links_list)):
        # every 10 cusip write to json to see if it's working
        if i % 10 == 0:
            print("writing latest version of details to json", i)
            # overwrite to result file using the 'w' flag
            details_json_file = open(DETAILS_JSON_FILE, 'w')
            json.dump(details, details_json_file, indent=4)    
            details_json_file.close()

        #time.sleep(.5)
        driver.get(links_list[i]['Frame Link'])
        details.extend(get_details(driver, i))
         
    with open(DETAILS_JSON_FILE, 'w') as details_json_file:
        json.dump(details, details_json_file, indent=4)

    print("all details processes done")