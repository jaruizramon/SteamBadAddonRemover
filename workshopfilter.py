# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:15:00 2020

@author: josep
"""


from bs4 import BeautifulSoup as sopa

import pandas as pd
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

''' START '''

''' This is the URL for the first page for the link-finding '''

init_page = 'https://steamcommunity.com/id/YaBoyPipo/myworkshopfiles/?appid=255710&browsefilter=mysubscriptions'

options = Options()
    
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("user-data-dir=selenium") 

    
driver = webdriver.Chrome(options=options)

soup = sopa(driver.page_source, 'lxml')

driver.get(init_page)

try:
    
    loginner = soup.find('div',class_='mainLoginPanel')
    print("You have to log in!")

except:
    
    print("You are already logged in!")
    
    

sleep(1)

pageXPATH = '/html/body/div[1]/div[7]/div[2]/div[1]/div[1]/div[7]/div[2]/div/div[27]/div[2]/a[2]'

page30 = driver.find_element_by_xpath(pageXPATH)
page30.click()

total_pagesXPATH = '/html/body/div[1]/div[7]/div[2]/div[1]/div[1]/div[7]/div[2]/div/div[67]/div[1]/a[3]'

total = driver.find_element_by_xpath(total_pagesXPATH)

print(total.text)


total_int = int(total.text)

links = list()

checky = 'https://steamcommunity.com/sharedfiles/filedetails/?id='

# total_int+1

for page in range(1, total_int+1):
    
    print(page)
    
    url_in_page = init_page + '&p=' + str(page) + '&numperpage=30'
    
    driver.get(url_in_page)
    soup = sopa(driver.page_source, 'lxml')
    
    randy = random.random()
    
    print(page)
    
    
    
    flag = False
    
    while(flag == False):
    
        try:
            
            for link in soup.find_all('a',href=True):
                temp = link['href']
                if (checky in temp):
                    print(temp)
                    links.append(temp)
                    sleep(.02)
                else:
                    pass
                # While loop END
                
            flag = True
            break
        except:
            flag = False
            driver.get(driver.current_url)
               
    # page loop END
    
links = list(dict.fromkeys(links))

print(links)

addon_names = list()
dep_stats = list()

sleep(2)

for link in links:
    
    try:
        
        sorry_cherry = False
        
        for attempt in range(2):
            driver.get(link)
            soup = sopa(driver.page_source, 'lxml')
            if (soup.find('h1').text != 'Sorry!'):
                sorry_cherry = False
                break
            else:
                sorry_cherry = True
                sleep(2)
        
        if(sorry_cherry == True):
            dep_stats.append('BROKEN PAGE')
            
        else:
            pass
            
        
        randy = random.random()
        sleep(1.10 + randy)
        
        mod_name_temp = soup.find('h1').text
        mod_name = mod_name_temp.replace('Subscribe to download','')
        addon_names.append(mod_name)
        
        check_depre = driver.find_element_by_class_name('incompatibleNotification')
        
        if (check_depre.is_displayed()):
            
            unsub_btnXPATH = '/html/body/div[1]/div[4]/div[13]/div/div[1]/div/a'
            unsub_btn = driver.find_element_by_xpath(unsub_btnXPATH)
            unsub_btn.click()
            print("%s IS OUTDATED." % (mod_name))
            
            dep_stats.append("DEPRECATED/OUTDATED")
            
        else:
            print("%s IS UP TO DATE" % (mod_name))
            dep_stats.append("UP TO DATE")
        
    except:
        pass
        

        
        
final_data = pd.DataFrame({'ADDON_NAME' : addon_names,
                           'DEPRECATION': dep_stats,
                           'URL' : links})

final_data.append(final_data, ignore_index = True)

try:
    
    csv_dir = 'C:\\Users\\josep\\Desktop\\listofyouraddons.csv'
    
    final_data.to_csv(csv_dir)
    
    print(final_data)

except:
    print("File Save Failed")
            

    
    
    







    

    
    

