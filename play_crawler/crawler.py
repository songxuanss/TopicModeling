'''
Created on Mar 5, 2014

Required Lib:
	1. beautifulsoup4
	2. httplib2
'''
import Queue
import threading
from urllib2 import Request
import time
from bs4 import BeautifulSoup
import httplib2
import json

__author__ = 'pauls'

class PlayCrawler:
    def __init__(self):
        pass

    def getTopFree(self, num):
        print "getting apk from google site..."

        url = 'https://play.google.com/store/apps/collection/topselling_free?hl=en&num=%s'
        h = httplib2.Http()
        (resp, content) = h.request(url % num, 'GET')

        rs = self.parser(content)
        print "finish getting apk from google site"
        return rs

    def parser(self, result):
        soup = BeautifulSoup(result)
        apklist = soup.find_all('div', {'data-docid':True, 'class':'card no-rationale square-cover apps small'})
        apks = []

        for apk in apklist:
            # Parse version infomation
            h = httplib2.Http()
            sub_url = 'https://play.google.com/store/apps/details?id=%s&hl=en'
            (resp, content) = h.request(sub_url % apk['data-docid'], 'GET')
            version = self.getVersion(content)
            apks.append('\t'.join([apk['data-docid'], version.get_text().strip() if version is not None else '']))
        return apks

    def getVersion(self, content):
        sub_soup = BeautifulSoup(content)
        version = sub_soup.find('div', {'class':'content', 'itemprop':'softwareVersion'})
        return version

class WandoujiaCrawler():

    def __init__(self):
        pass

    def getTopFree(self, num):
        apks = []
        i = 0
        while num / 20 > 0:
            num = num - 20
            apks.extend(self.getApks(i, 20))
            i = i + 20
        if num % 20 > 0:
            apks.extend(self.getApks(i, num % 20))
        return apks

    def getApks(self, start, count):
        url = 'http://apps.wandoujia.com/api/v1/apps?\
        type=weeklytopapp&max=%s&start=%s&opt_fields=stat.weeklyStr,likesCount,reason,ad,title,\
        packageName,apks.size,icons.px68,apks.superior,installedCountStr,snippet,apks.versionCode,tags.*&_=1394082542549'
        h = httplib2.Http()
        (resp, content) = h.request(url % (count, 0), "GET",
                                    headers={ 'Content-Type': 'text/javascript', 'charset': 'UTF-8'})
        res = json.loads(content)
        apks = []
        for item in res:
            apks.append(item['packageName'])

        return apks

if __name__ == "__main__":
    crawler = PlayCrawler()
    data = crawler.getTopFree(10)
    print len(data)

    for item in data:
        print item


