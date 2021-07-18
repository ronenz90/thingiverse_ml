from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

chrome_driver_path = 'Drivers/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--incognito')
chrome_options.add_argument("--headless")
url = "https://www.thingiverse.com/"

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
driver.get(url)

arr_main = []


def get_results():
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'Pagination')]")))

    except:
        print("No Result Found")
        return

    links = driver.find_elements_by_xpath("//a[contains(@class,'ThingCardBody')]")
    likes = driver.find_elements_by_xpath("//a[contains(@class, 'CardActionItem__contentItem--1Un1W')]")

    for i in range(len(links)):
        link = links[i].get_attribute("href")
        like = 0
        try:
            like = int(likes[(i * 3) - 2].text)
        except:
            like = 0

        driver2 = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        driver2.get(links[i].get_attribute("href"))
        try:
            WebDriverWait(driver2, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'ThingPage__createdBy')]")))
            pass
        except Exception as ex2:
            print(ex2)
            driver2.close()
            driver2.quit()
            pass
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
        print(tags)
        arr = [link, str(like), tags, header_title, date_created, description]
        arr_main.append(arr)

        driver2.close()
        driver2.quit()
    idx = 1000
    pd.DataFrame(arr_main).to_csv(str(idx) + "_file.csv")
    try:
        driver.find_element_by_xpath("//div[contains(@class,'Pagination__more')]").click()
        active_current = driver.find_element_by_xpath("//a[contains(@class,'Pagination__active')]").text
        statement = True
        while statement:
            active = driver.find_element_by_xpath("//a[contains(@class,'Pagination__active')]").text
            if active != active_current:
                print(" Value")
                statement = False
                get_results()
            else:
                pass
    except Exception as ex:
        print(ex)
        print("No More Results")


get_results()
driver.close()
driver.quit()
