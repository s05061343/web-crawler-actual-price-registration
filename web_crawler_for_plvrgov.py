from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os.path
import zipfile


def web_crawler():
    download_dir = os.path.abspath("./temp/")
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_dir,
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)
    options.add_argument("disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options)

    driver.get("https://plvr.land.moi.gov.tw/DownloadOpenData")
    time.sleep(1)
    fileFormatId = Select(driver.find_element(By.ID, "fileFormatId"))
    fileFormatId.select_by_value("xls")
    time.sleep(1)
    downloadTypeId2 = driver.find_element(By.ID, "downloadTypeId2")
    downloadTypeId2.click()

    H_lvr_land_A = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[2]/input",
    )
    H_lvr_land_A.click()
    H_lvr_land_B = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[3]/input",
    )
    H_lvr_land_B.click()

    downloadBtn = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[3]/a[2]",
    )
    downloadBtn.click()
    time.sleep(5)

    driver.quit()


def extract_download_zip():
    file = "./temp/download.zip"
    ZIP = zipfile.ZipFile(file)
    ZIP.extractall("./temp/")
    ZIP.close()
    time.sleep(3)

    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist")
