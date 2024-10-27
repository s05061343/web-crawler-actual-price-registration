import pandas
import os.path
import json
from datetime import datetime


def merge_subarea(file):
    file_subarea = "./temp/subarea.xlsx"
    if os.path.exists(file):
        df = pandas.read_excel(
            file,
            header=[0],
            # usecols=["鄉鎮市區", "交易標的", "土地位置建物門牌"],
            # nrows=300,
        )
        # df = pandas.read_excel(file, header=[0])
        df = df[df["鄉鎮市區"].str.contains("中壢區")]
        df = df[df["交易標的"].str.contains("房")]
        # print(df)

        df_subarea = pandas.read_excel(file_subarea, header=[0])
        # print(df_subarea)

        list = json.loads(df.to_json(orient="records"))
        for item in list:
            item["土地位置建物門牌"] = (item["土地位置建物門牌"]).translate(
                str.maketrans("０１２３４５６７８９", "0123456789")
            )

            subs = []
            for subItem in json.loads(df_subarea.to_json(orient="records")):
                for address in str.split(subItem["address"], "、"):
                    if address in item["土地位置建物門牌"]:
                        subs.append(subItem)

            # subs = [
            #     subItem
            #     for subItem in json.loads(df_subarea.to_json(orient="records"))
            #     if subItem["address"] in item["土地位置建物門牌"]
            # ]

            if subs:
                # print(subs)
                item["商圈"] = subs[0]["subarea"]
                item["建案"] = subs[0]["title"]
            else:
                item["商圈"] = ""
                item["建案"] = ""

        print(list)
        return list


def data_export(df):
    date_time = datetime.now().strftime("%m-%d-%Y_%H%M%S")
    pandas.DataFrame(df).to_excel(f"./output/data_export_{date_time}.xlsx")
