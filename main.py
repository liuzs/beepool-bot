# coding : UTF-8

import json
import requests
import csv
import random
import socket
import http.client
import time


def get_content(url):  # 获取网页数据
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        #        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64 '
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text


def get_data(html_text):  # 从json文件中处理数据
    str_json = json.loads(html_text)
    activelist = str_json.get("data").get("miner").get("activeWorkers").get("list")
    inactivelist = str_json.get("data").get("miner").get("inactiveWorkers").get("list")
    list2 = str_json.get("data").get("last_24_hour_income")
    result1 = []
    result2 = []
    for i in activelist:
        result1.append(i.get("name"))  # 存名字
    for i in activelist:
        result2.append((i.get("avg_hashrate")) / 1000000)  # 存24小时算力，并转换格式
    for i in inactivelist:
        result1.append(i.get("name"))  # 存名字
    for i in inactivelist:
        result2.append((i.get("avg_hashrate")) / 1000000)  # 存24小时算力，并转换格式
    result1.append("last_24_hour_income")
    result1.append("time")
    result2.append(list2)
    result2.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    final = [result1, result2]
    return final


def write_data(data, name):  # 写入csv表格
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


if __name__ == '__main__':  # 主程序
    url = 'https://www.beepool.com/get_miner?coin=eth&wallet=chouuvrenqusi'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'C:\minee.csv')  # csv保存地址
