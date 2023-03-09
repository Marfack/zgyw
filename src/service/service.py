from multiprocessing import Queue
import requests
from lxml import etree
import time

def doService(id: str, username: str, password: str, q: Queue, idx: int):
    session = requests.Session()
    try:
        dom = etree.HTML(session.get('http://59.69.102.9/zgyw/index.aspx').text)
        __VIEWSTATE = dom.xpath(r'//*[@id="__VIEWSTATE"]/@value')[0]
        response = session.post('http://59.69.102.9/zgyw/index.aspx', data={
            '__VIEWSTATE': __VIEWSTATE,
            'ctl00$ContentPlaceHolder1$name': username,
            'ctl00$ContentPlaceHolder1$pwd': password,
            'ctl00$ContentPlaceHolder1$login': '登录'
        })
    except Exception:
        q.put(['网络故障，检查是否连接校园网或使用校园网VPN'])
        exit()

    if response.status_code == 200:
        while 1:
            try:
                res = etree.HTML(session.get("http://59.69.102.9/zgyw/index.aspx").text).xpath(r'//*[@id="ctl00_ContentPlaceHolder1_lblonlineTime"]')[0].xpath(r'string(.)').split()
                if res == None:
                    q.put(['登录失败'])
                    exit()
            except:
                q.put(['登录失败或连接超时'])
                exit()
            try:
                session.get('http://59.69.102.9/zgyw/study/LearningContent.aspx?type=5&id=28&learningid=3039')
            except:
                q.put(['连接超时'])
                exit()
            t = eval(res[0][:-1]) + eval(res[1][:-1]) / 60
            q.put([id, username, '{:.2f}min'.format(t), idx])
            for _ in range(90):
                time.sleep(1)
                t += 1/60
                if not q.full():
                    q.put([id, username, '{:.2f}min'.format(t), idx])