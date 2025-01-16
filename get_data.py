from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time 
import os, sys, subprocess
import urllib3 
import keyboard


def get_signal():
    
    #Setting Thingspeak
    #baseURL3 = 'http://api.thingspeak.com/update?api_key=4OJ3IJ6IZQOKJBDQ'    #Location1
    baseURL3 = 'http://api.thingspeak.com/update?api_key=D77QLEJ1ZRC1CLTG'  #Location2
    http = urllib3.PoolManager()

    # Going to Local Web of DVB TVheadend
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)

    driver.get("http://admin:admin@raspberrypi.local:9981/extjs.html")
    print(driver.title)
    #try:

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ext-gen138"))
        )
    element.click()


    table_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ext-gen168")))

    rows = table_id.find_elements(By.TAG_NAME, "tr")
    for row in rows: # Get the columns (all the column 2)
        cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
        #n_kolom = str(len(cols))
        #print("number of column : " + n_kolom)
        
        #Get data from Table to list
        device_name = cols[1].text
        stream_ch = cols[2].text
        bandwidth = cols[5].text
        ber = cols[6].text 
        snr = cols[11].text
        sss = cols[12].text
        
        ber_score = ber[0:6]
        snr_score = snr[0:4]
        sss_score = sss[0:5]
        print(sss_score)
                

        f = http.request('GET', baseURL3 + "&field2=" + str(round(snr,1)) + "&field3=" + str(round(sss,1)) + "&field4=" + bandwidth[1:6])
        

get_signal()
