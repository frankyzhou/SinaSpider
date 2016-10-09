# encoding=utf-8
import json
import base64
import requests

myWeiBo = [
    {'no': u'13162508269', 'psw': u'zljabhbhwan37'},
    # {'no': 'shudieful3618@163.com', 'psw': 'a123456'},
]


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = 'https://xueqiu.com/user/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
        'Host': 'xueqiu.com',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Cache-Conrol': 'no-cache',
        'Referer': 'http://xueqiu.com/P/ZH003694',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        login_post_data = {
            'username': u"",
            'areacode': '86',
            'telephone': account,
            'remember_me': '0',
            'password': password
        }
        login_response = requests.post(loginURL, cookies=cookies, data=login_post_data,
                                            headers=headers)
        cookies.append(login_response.cookies)
        print login_response.cookies
        print login_response.headers
    return cookies


cookies = getCookies(myWeiBo)
print "Get Cookies Finish!( Num:%d)" % len(cookies)
