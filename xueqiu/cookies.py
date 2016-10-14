# encoding=utf-8
import requests


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
        cookies = login_response.cookies

    return get_str_cookies(cookies)


def get_str_cookies(cookies):
    """
    获取cookies
    frankyzhou add @ 2016/06/01
    :return:
    """
    str_cookies = ""
    for item in cookies.items():
        str_cookies = str_cookies + item[0] + "=" + item[1] + "; "
    return str_cookies

