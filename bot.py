import threading
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

df1 = pd.read_csv("links.csv")
links_ = df1["Links"]

arr_main = []

idx_get = 0


def save_data():
    global arr_main
    pd.DataFrame(arr_main).to_csv(str(idx_run) + "_file.csv")
    arr_main.clear()


def get_data():
    chrome_driver_path = 'Drivers/chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--headless")

    global idx_get
    global links_
    global arr_main

    driver2 = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    links = links_[idx_get]

    if idx_get < len(links_):
        pass
    else:
        return

    print("Running:" + str(idx_get))

    print(links_[idx_get])
    idx_get = idx_get + 1
    driver2.get(links_[idx_get])
    try:
        WebDriverWait(driver2, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'ThingPage__createdBy')]")))
        pass
    except Exception as ex2:
        print(ex2)
        driver2.close()
        driver2.quit()
        pass
    like = 0
    try:
        like = int(driver2.find_element_by_xpath("//a[contains(@class, 'CardActionItem__contentItem--1Un1W')]")[
                       1].text)
    except:
        like = 0
    header_title = ""
    try:
        header_title = driver2.find_element_by_class_name("ThingPage__modelName--3CMsV").text
    except:
        pass
    date_created = ""
    try:
        date_created = driver2.find_element_by_class_name("ThingPage__createdBy--1fVAy").text
    except:
        pass
    description = ""
    try:
        description = driver2.find_element_by_class_name("ThingPage__description--14TtH").text
    except:
        pass
    tags = ""
    try:
        tag_ = driver2.find_element_by_class_name("Tags__widgetBody--19Uop").find_elements_by_tag_name("a")
        tmp = ""
        for idx_tag in range(len(tag_)):
            delimiter = ","
            if idx_tag == 0:
                delimiter = ""
            tmp = tmp + delimiter + tag_[idx_tag].text
        tags = tmp
    except:
        pass
    arr = [links, str(like), tags, header_title, date_created, description]
    arr_main.append(arr)
    driver2.close()
    driver2.quit()


print("Size of Idx:" + str(int(len(links_) / 5)))

start_idx = 40

idx_get = (start_idx * 5)
if start_idx != 0:
    idx_get = idx_get - 5

print(idx_get)

for idx_run in range(int(len(links_) / 5)):
    if idx_run < start_idx:
        print("Skipped Index" + str(idx_run))
    else:
        t1 = threading.Thread(target=get_data)
        t2 = threading.Thread(target=get_data)
        t3 = threading.Thread(target=get_data)
        t4 = threading.Thread(target=get_data)
        t5 = threading.Thread(target=get_data)
        t1.start()
        time.sleep(0.5)
        t2.start()
        time.sleep(0.5)
        t3.start()
        time.sleep(0.5)
        t4.start()
        time.sleep(0.5)
        t5.start()
        time.sleep(0.5)
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        print("Done Idx : " + str(idx_run))
        threading.Thread(target=save_data).start()
