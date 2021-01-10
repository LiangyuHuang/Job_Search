import requests
from time import sleep
import random
import pandas as pd


def get_cookies():
    url = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/p-city_215?&cl=false&fromSearch=true&labelWords=&suginput='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'referer': 'https://www.lagou.com/',
    }
    response = requests.get(url=url, headers=headers)
    cookies = response.cookies
    print(cookies)
    return cookies


def spiders():
    def get_info(dic):
        df = pd.DataFrame(
            columns=['positionName', 'companyLabelList', 'address', 'companyFullName', 'companySize', 'education',
                     'salary', 'workYear'])
        result = dic['content']['positionResult']['result']
        for index, i in enumerate(result):
            positionName = i['positionName']  # 职位
            companyLabelList = i['companyLabelList']  # 福利
            address = i['city'] + i['district']  # 地址
            companyFullName = i['companyFullName']  # 公司名字
            companySize = i['companySize']  # 公司规模
            education = i['education']  # 要求学历
            salary = i['salary']  # 工资
            workYear = i['workYear']  # 工作经验
            print('职位：{},福利：{},地址：{},公司名字：{},公司规模：{},学历：{},工资：{},工作经验：{}'
                  .format(positionName, companyLabelList, address, companyFullName, companySize, education, salary,
                          workYear))
            df.loc[index] = [positionName, companyLabelList, address, companyFullName, companySize, education, salary,
                             workYear]
        df.to_csv('output.csv')

    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-length': '75',
        'origin': 'https://www.lagou.com',
        'referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same - origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'x-anit-forge-code': '0',
        'x-anit-forge-token': 'None',
        'x-requested-with': 'XMLHttpRequest',
    }
    cookies = get_cookies()
    sid = 'a3fd2ca16fe44f1ab29614e6de60b6f3'
    for pn in range(1, 10):
        data = {
            'first': 'false',
            'pn': str(pn),
            'kd': '数据分析',
        }
        if pn == 1:
            data['first'] = 'true'
            response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
            json = response.json()
            data['sid'] = json['content']['showId']
            # print(data)
            # print(json)
            get_info(json)
            sleep(random.randint(3, 6))
        elif pn % 4 == 0:
            try:
                response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
                json = response.json()
                print(json)
                get_info(json)
                sleep(random.randint(3, 6))
            except:
                sleep(5)
                cookies = get_cookies()
                response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
                json = response.json()
                print(json)
                get_info(json)
                sleep(random.randint(3, 6))
        else:
            try:
                cookies = get_cookies()
                response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
                json = response.json()
                print(json)
                get_info(json)
                sleep(random.randint(3, 6))
            except:
                sleep(5)
                cookies = get_cookies()
                response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
                json = response.json()
                print(json)
                get_info(json)
                sleep(random.randint(3, 6))


def main():
    spiders()


if __name__ == '__main__':
    main()
