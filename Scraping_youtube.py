from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from warnings import simplefilter
simplefilter(action='ignore', category=ValueError) #

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())


############################################################ DATA COLLECTION PART #####################################################
# print(os.getcwd())
os.chdir(r'C:\webdrivers') # going to path to run chromedriver which create instant of chrome from where it fetch all data
# print(os.getcwd())

pd.set_option('display.max_columns', None)
df = pd.DataFrame(columns = ['link', 'title', 'Description', 'Category'])

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal" #page will load fully
driver = webdriver.Chrome(ChromeDriverManager().install(),desired_capabilities= caps)
categories= ['Science', 'Food', 'Travel', 'Songs']

for category in categories:
    url= 'https://www.youtube.com/results?search_query='+category # using this url for multiple category
    driver.get(url)
    # driver.get('https://www.youtube.com/results?search_query=science&sp=EgIQAQ%253D%253D') # used for one category
    time.sleep(5) # using this to manually scroll down all page
    # print(url)

    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    links = []
    for i in user_data:
        if i.get_attribute('href') == None:
            continue
        else:
            links.append(i.get_attribute('href')) # fetch the “href” attribute of the anchor tag we searched for.
            # print(links)
        # print(len(links))

    wait = WebDriverWait(driver, 10)

    v_category = category
    i = 1
    for x in links:
                driver.get(x)
                v_id = x.strip('https://www.youtube.com/watch?v=')
                # wait = WebDriverWait(driver, 10)
                v_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ytd-video-primary-info-renderer"))) # using this which give all info like views, share, title etc
                v_description =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text #will give description
                v_title = v_title.text #converting into string
                if v_title.startswith('#'): # this is title of each video
                    v_title= v_title.split('\n')[1]
                else:
                    v_title= v_title.split('\n')[0]
    #             # print(v_title)
    #             # print(v_description)
    #             # print(f'{i}.Title is {v_title} and description is {v_description}')
    #             # print(f'{i}.Description is {v_description}')
                i+=1
                df.loc[len(df)] = [v_id, v_title, v_description, v_category]


df.to_csv(r'C:\Users\egoeshu\Desktop\testingdoc\Youtube classifer ML\youtube_classifier_data_latest.csv', index=False) # data collecting in csv file total 223 records came.
