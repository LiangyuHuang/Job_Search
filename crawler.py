import requests
import math
import time
import pandas as pd
import random
from urllib import request


def getjson(url, num):  # 传入两个参数url，页数
    """
    从指定的url中通过requests请求携带请求头和请求体获取网页中的信息,
    :return:
    """
    # 另外一种方法
    # handler = request.ProxyHandler({"https":"222.76.74.183:41309"})
    # opener = request.build_opener(handler)
    proxies_ip = {"http": "https://222.76.74.183:41309"}  # 代理ip
    url1 = 'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput='  # 关键词python开发工程师
    # 模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        # 'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
        # 'X-Anit-Forge-Code': '0',
        # 'X-Anit-Forge-Token': 'None',
        # 'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'first': 'true',
        'pn': num,  # 页数
        'kd': '数据分析'}  # 关键字
    s = requests.Session()
    print('建立session：', s, '\n\n')
    s.get(url=url1, headers=headers, proxies=proxies_ip, timeout=3)  # 3秒内没有从基础套接字上接收到任何字节的数据时，将返回异常
    cookie = s.cookies
    print('获取cookie：', cookie, '\n\n')
    res = requests.post(url, headers=headers, proxies=proxies_ip, data=data, cookies=cookie, timeout=3)
    # res = opener.post(url, headers=headers,proxies=proxies, data=data, cookies=cookie, timeout=3)
    res.raise_for_status()  # 响应码抓取 正常为200
    res.encoding = 'utf-8'
    pdata = res.json()  # 处理json数据返回到pdata
    print('请求响应结果：', pdata, '\n\n')
    return pdata


def getpnum(num):
    """
    计算要抓取的页数，通过在拉勾网输入关键字信息，可以发现最多显示30页信息,每页最多显示15个职位信息
    :return:
    """
    pnum = math.ceil(num / 15)  # ceil返回整数
    if pnum > 30:
        return 30
    else:
        return pnum


def getp(list):  # 传入一个形参职位列表
    """
    获取职位
    :param jobs_list:
    :return:
    """
    plist = []  # 生成一个总页面列表
    for page in list:  # 循环每一页所有职位信息
        jobmgs = []  # 生成一个工作信息列表
        jobmgs.append(page['companyFullName'])  # 把公司的名字追加到工作信息列表中
        jobmgs.append(page['companyLabelList'])  # 把公司福利加到工作信息列表中
        jobmgs.append(page['city'])  # 公司城市加到列表中
        plist.append(jobmgs)  # 把职位追加到总列表中
    return plist


def main():
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'  # json数据url F12 network 重新加载json 可以看见
    shouye = getjson(url, 1)  # 第一页
    pnum = shouye['content']['positionResult']['totalCount']  # 页面的总数赋值
    num = getpnum(pnum)  # 总数调用函数后等于当前的页面数
    kong = []  # 生成一个空的总职位列表
    time.sleep(random.randint(10, 15))
    print("数据分析相关职位总数:{},总页数为:{}".format(pnum, num))
    for num in range(1, num + 1):
        # 获取每一页的职位相关的信息
        pdata = getjson(url, num)  # 获取响应json
        jobs = pdata['content']['positionResult']['result']  # 获取每页的所有python相关的职位信息
        pinfo = getp(jobs)  # 把当前页所有的公司名字，福利，地址保存后，赋给当前页的信息
        print("每一页python相关的职位信息:%s" % pinfo, '\n\n')
        kong += pinfo  # 当前页+总页并赋值给总页
        print('已经爬取到第{}页，职位总数为{}'.format(num, len(kong)))
        time.sleep(20)
        # total_info爬的数据与cloumns里的数据一一对应
        # 将总数据转化为data frame再输出,然后在写入到csv各式的文件中
        df = pd.DataFrame(data=kong,
                          columns=['公司全名', '公司福利', '城市'])
        df.to_csv('Date.csv', index=False)  # 保存到csv中 否保存索引
        print('数据分析相关职位信息已保存')


if __name__ == '__main__':
    main()