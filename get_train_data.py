# -*- coding:utf-8 -*-
"""
Author: BigCat
"""
import os
import json
import requests
from bs4 import BeautifulSoup
import config


def get_current_number():
    """获取最新一期数字
    :return: int
    """
    r = requests.get("{}{}".format(config.URL, "history.shtml"))
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    current_num = soup.find("div", class_="wrap_datachart").find("input", id="end")["value"]
    return current_num


def spider(start, end):
    """爬取历史数据
    :param start 开始一期
    :param end 最近一期
    :param mode 模式
    :return:
    """
    url = "{}{}{}".format(config.URL, config.path.format(start), end)
    r = requests.get(url=url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    trs = soup.find("tbody", attrs={"id": "tdata"}).find_all("tr")
    data = []
    for tr in trs:
        item = dict()
        item[u"期数"] = tr.find_all("td")[0].get_text().strip()
        item[u"红球号码_1"] = tr.find_all("td")[1].get_text().strip()
        item[u"红球号码_2"] = tr.find_all("td")[2].get_text().strip()
        item[u"红球号码_3"] = tr.find_all("td")[3].get_text().strip()
        item[u"红球号码_4"] = tr.find_all("td")[4].get_text().strip()
        item[u"红球号码_5"] = tr.find_all("td")[5].get_text().strip()
        item[u"红球号码_6"] = tr.find_all("td")[6].get_text().strip()
        item[u"蓝球"] = tr.find_all("td")[7].get_text().strip()
        item[u"快乐星期天"] = tr.find_all("td")[8].get_text().strip()
        item[u"奖池奖金(元)"] = tr.find_all("td")[9].get_text().strip()
        item[u"一等奖_注数"] = tr.find_all("td")[10].get_text().strip()
        item[u"一等奖_奖金(元)"] = tr.find_all("td")[11].get_text().strip()
        item[u"二等奖_注数"] = tr.find_all("td")[12].get_text().strip()
        item[u"二等奖_奖金(元)"] = tr.find_all("td")[13].get_text().strip()
        item[u"总投注额(元)"] = tr.find_all("td")[14].get_text().strip()
        item[u"开奖日期"] = tr.find_all("td")[15].get_text().strip()
        data.append(item)

    with open('{}{}'.format(config.train_data_path, config.train_data_file), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == "__main__":
    print("[INFO] 最新一期期号：{}".format(get_current_number()))
    print("[INFO] 正在获取数据。。。")
    if not os.path.exists(config.train_data_path):
        os.mkdir(config.train_data_path)
    spider(1, get_current_number())
    print("[INFO] 数据获取完成，请查看data/data.json文件。")
