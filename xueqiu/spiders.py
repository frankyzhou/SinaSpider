# encoding=utf-8

import json
import time
from cookies import getCookies
import requests
from MongoDB import *

myWeiBo = [
    {'no': u'13162508269', 'psw': u'zljabhbhwan37'},
    # {'no': 'shudieful3618@163.com', 'psw': 'a123456'},
]
start_urls = [
    7315353232
]
time_stop =60


class XqSpider:
    def __init__(self):
        self.cookie = getCookies(myWeiBo)
        self.scrawl_ID = set(start_urls)
        self.finish_ID = set()
        self.db = MongoDB("xq_spider")
        self.follows = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'xueqiu.com',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
            'Cookie': self.cookie
        }

    def start_requests(self):
        while len(self.finish_ID) < 10000:
            isdone = False
            ID = self.scrawl_ID.pop()
            ID = str(ID)
            self.follows = []
            # # followsItems = FollowsItem()
            # followsItems["_id"] = ID
            # followsItems["follows"] = follows
            # url_follows = "https://xueqiu.com/friendships/groups/members.json?uid=%s&gid=0&page=1" % ID
            url_follows = "https://xueqiu.com/friendships/groups/members.json"
            "关注"
            url_fans = "https://xueqiu.com/friendships/followers.json?pageNo=1&uid=%s&size=20" % ID
            "粉丝"
            url_tweets = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id=%s&page=1&type=" % ID
            "主贴"
            url_information0 = "https://xueqiu.com/%s" % ID
            "个人主页"
            url_articles = "https://xueqiu.com/statuses/original/timeline.json?user_id=%s&page=1" % ID
            "原创文章"
            url_top_count_stock = "https://xueqiu.com/user/top_status_count_stock.json?count=5&uid=%s" % ID
            "最高讨论次数的股票"
            url_stocks_follow = "https://xueqiu.com/stock/portfolio/stocks.json?size=1000&tuid=%s" % ID
            "关注的股票（包括指数）与组合"
            data = {
                "uid": ID,
                "gid": 0,
                "page": 1
            }
            try:
                response = requests.get(url=url_follows, headers=self.headers, params=data)
                self.parse(response.text, ID)
                isdone = True
            except Exception, e:
                print e
                self.scrawl_ID.add(ID)
                print ID + "is wrong. We need to add it to scrawllist again! Let's wait %s s" % time_stop
                time.sleep(time_stop)

            if isdone:
                if len(self.follows) > 0:
                    print ID, len(self.follows)
                    self.db.insert_doc("ff", {ID: self.follows})
                self.finish_ID.add(ID)  # 加入已爬队列

            print "scraw_list is " + str(len(self.scrawl_ID)) + ". finish_list is " + str(len(self.finish_ID))

    def parse(self, response, old_id):
        """ 抓取关注或粉丝 """
        # time.sleep(5)
        url_follows = "https://xueqiu.com/friendships/groups/members.json"
        json_data = json.loads(response)
        # self.db.insert_doc(coll="follwers", info=json_data["users"])
        for elem in json_data["users"]:
            id = elem["id"]
            fans = elem["followers_count"]
            if fans > 50000:
                self.follows.append(id)
                if id not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                    self.scrawl_ID.add(id)
        page, maxp_age = json_data["page"], json_data["maxPage"]

        if page < maxp_age:
            page += 1
            data = {
                "uid": old_id,
                "gid": 0,
                "page": page
            }
            response = requests.get(url=url_follows, headers=self.headers, params=data)
            self.parse(response.text, old_id)

if __name__ == "__main__":
    xq = XqSpider()
    xq.start_requests()