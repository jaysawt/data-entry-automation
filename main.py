import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


#----------DECLARING CONSTANTS-----------------#
CHROME_PATH = "C:\Developer\chromedriver.exe"
ZILLO_FORM = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Whitefield%20Bangalore%20Karnataka%20Bangalore%2C%20IN%2056006%22%2C%22mapBounds%22%3A%7B%22north%22%3A37.823218826102305%2C%22east%22%3A-122.3093536530128%2C%22south%22%3A37.66603118142228%2C%22west%22%3A-122.57920533758312%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A403470%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%2C%22mapZoom%22%3A12%7D"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSczhQ-eP0ciXhwSWQ1hXIDHRzwbZXUtp8gDG55bmXtu1rk5XQ/viewform?usp=sf_link"
FINAL_FORM = "https://docs.google.com/forms/u/0/"



#----------DRIVER INITIALISATION-----------------#
ser = Service(CHROME_PATH)
option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ser, options=option)


# ----------------GET WEBSITE DETAILS AS (RESPONSE METHOD) IS GIVING TIMEOUT ERROR------------------#
def scrap_zillo():
        driver.get(ZILLO_FORM)
        html_content = driver.page_source
        with open("site_data.txt", "w", encoding='utf-8') as fp:
            fp.write(html_content)

    # # --------------GET WEBSITE DETAILS(NOT WORKING)--------------------------------#
    # header = {
    #     'User-Agent': "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
    #     'Accept-Language': 'en-US, en;q=0.5'
    # }
    # response = requests.get(url=ZILLO_FORM, headers=header, timeout=10)
    # response.raise_for_status()
    # data = response.text
    # return data


# #--------------SCRAP THE WEBSITE----------------#
def soup_website():
    with open("site_data.txt", "r", encoding='utf-8') as fp:
        data = fp.read()
    soup = BeautifulSoup(data, "html.parser")
    return soup.select(selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0")


# ---------------FILL FORM AND DIRECTLY LOAD RESPONSES TO EXISTING SHEET----------------------------#
def fill_form(addressT, linksT, rentT):
    driver.get(GOOGLE_FORM)
    sleep(5)
    i = 0
    while i != len(address):
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(addressT[i])
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(rentT[i])
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(linksT[i])
        submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.lRwqcd div span")))
        submit.click()
        another_response = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.c2gzEf  a")))
        another_response.click()
        i += 1
    driver.quit()

if __name__ == '__main__':
    scrap_zillo()
    infos = soup_website()
    sleep(5)

    # ----------------DETAILS OF APARTMENT-------------------#
    address = [
        info.select_one(selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0 div.property-card-data a address").string for
        info
        in infos]

    rent = [info.select_one(selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0 div.property-card-data div span").string
            for info
            in infos]
    links = [info.select_one(selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0 div.property-card-data a").get('href')
             if "https://www.zillow.com" in info.select_one(
        selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0 div.property-card-data a").get('href')
             else "https://www.zillow.com" + info.select_one(
        selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0 div.property-card-data a").get('href')
             for info in infos]

    # EXPLAINATION FOR ABOVE LINKS LIST
    # for info in infos:
    #     x = info.select_one(selector="div.StyledCard-c11n-8-85-1__sc-rmiu6p-0 div.property-card-data a").get('href')
    #     if "https://www.zillow.com" in x:
    #         print(x)
    #     else:
    #         print("https://www.zillow.com" + x)


    fill_form(address, links, rent)
