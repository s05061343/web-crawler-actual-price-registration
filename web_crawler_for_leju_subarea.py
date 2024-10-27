from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import pandas
import os


def getJson(driver):
    content = driver.find_element(By.TAG_NAME, "pre").text
    decoded_value = content.encode("utf-8")
    parsed_json = json.loads(decoded_value)
    return parsed_json


def get_subareas_list(driver):
    subarea_url = "https://api.leju.com.tw/api/region_price/subarea/list?post_code=320"
    driver.get(subarea_url)
    json = getJson(driver)["data"]
    return json


def get_building_list(driver, subarea):
    subarea_center_url = (
        f'https://api.leju.com.tw/api/region_price/subarea/center/{subarea['id']}'
    )
    driver.get(subarea_center_url)
    j_subarea_center = getJson(driver)

    building_url = f'https://api.leju.com.tw/api/region_price/object/mapRadiusData?latitude={j_subarea_center['lat']}&longitude={j_subarea_center['lng']}&radius=439&building_types=1,2,0,3'
    driver.get(building_url)
    j_building_list = getJson(driver)["data"]
    return j_building_list


def web_crawler():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options)

    all_building_list = []
    for subarea in get_subareas_list(driver):
        building_list = get_building_list(driver, subarea)
        for building in building_list:
            building["subarea"] = subarea["small_area_name"]
        all_building_list += building_list

    newpath = r'./output' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    pandas.DataFrame(all_building_list).to_excel("./temp/subarea.xlsx")
    date_time = datetime.now().strftime("%m-%d-%Y_%H%M%S")
    pandas.DataFrame(all_building_list).to_excel(f"./output/subarea_{date_time}.xlsx")
    driver.quit()


# def web_crawler():
#     options = webdriver.ChromeOptions()
#     options.add_argument("disable-popup-blocking")
#     options.add_argument("--disable-notifications")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     driver = webdriver.Chrome(options)

#     all_building_list = []
#     for subarea in get_subareas_list(driver):
#         building_list = get_building_list(driver, subarea)
#         for building in building_list:
#             address = str.split(building["address"], "、")
#             if len(address) > 0:

#             else:
#                 building["subarea"] = subarea["small_area_name"]
#         all_building_list += building_list

#     pandas.DataFrame(all_building_list).to_excel(f"./temp/subarea.xlsx")
#     driver.quit()
