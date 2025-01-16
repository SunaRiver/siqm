from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time 
import sys
import urllib3
import keyboard
import pandas as pd


#Setting Thingspeak
baseURL3 = 'http://api.thingspeak.com/update?api_key=D77QLEJ1ZRC1CLTG'
http = urllib3.PoolManager()

#Going to Local Web of DVB TVheadend
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome("chromedriver", options=options)

driver.get("http://raspberrypi.local:9981/extjs.html")
print(driver.title)
#try:
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ext-gen144")))
element.click()
#finally:
#    driver.quit()
#print(element)

#Yang bener 170
#table_id = WebDriverWait(driver, 10).until(
#    EC.presence_of_element_located((By.ID, "ext-gen170"))
#    )
#print(table_id)
flag = 1
while (True):
    try:
        wait = WebDriverWait(driver, 10)
        table_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ext-gen174")))
        #print(table_id)
        #tutorial_soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        n_baris = str(len(rows))
        #print("Jumlah baris : " + n_baris)
        wait = WebDriverWait(driver, 10)
        for row in rows: # Get the columns (all the column 2)
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            n_kolom = str(len(cols))
            stream = cols[2].text
            stream_freq = stream[0:3]
            ber = cols[6].text
            snr = cols[12].text
            ss = cols[13].text
            print("Device : " + cols[1].text)
            print("Stream : " + stream[0:3] + " MHz")
            print("BER : " + ber[0:6])
            print("SNR : " + snr[0:4] + " dB")
            print("Signal Strength : " + ss[0:5] + " dBm")
            
            if(stream_freq == "650" and snr !="Unknown"):
                print("Send Success")
                data = pd.DataFrame({"SNR":[snr[0:4]],"SS":[ss[0:5]]})
                data.to_csv("data.csv")
                #f = http.request('GET', baseURL3 + "&field2=" + snr[0:4] + "&field4=" + ber[0:6] + "&field3=" + ss[0:5])
            print("")
            #f.read()
            #f.close()
            #Delay 15 second for non-premium thingspeak
        #if keyboard.is_pressed('q'):
        #           print("\n Now Exiting...")
        #            sys.exit(0)
        continue
    except:
        pass
