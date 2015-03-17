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
		self.__top100free__ = 'https://play.google.com/store/apps/collection/topselling_free?hl=en&num=%s'
		self.__top10000free__ = 'https://play.google.com/store/apps/collection/topselling_free?hl=en&authuser=0'
		self.__apkdetail__ = 'https://play.google.com/store/apps/details?id=%s&hl=en'

	def getTop100Free(self, num):
		print "getting apk from google site..."
		url = self.__top100free__
		h = httplib2.Http()
		(resp, content) = h.request(url % num, 'GET')
		rs = self.parser(content)
		print "finish getting apk from google site"
		return rs

	def parser(self, result):
		soup = BeautifulSoup(result)
		apklist = soup.find_all('div', {'data-docid': True, 'class': 'card no-rationale square-cover apps small'})
		apks = []

		for apk in apklist:
			# Parse version infomation
			h = httplib2.Http()
			sub_url = self.__apkdetail__
			(resp, content) = h.request(sub_url % apk['data-docid'], 'GET')
			version = self.__getVersion(content)
			apks.append('\t'.join([apk['data-docid'], version.get_text().strip() if version is not None else '']))
		return apks

	def __getVersion(self, content):
		assert isinstance(content, str)
		sub_soup = BeautifulSoup(content)
		version = sub_soup.find('div', {'class': 'content', 'itemprop': 'softwareVersion'})
		return version



if __name__ == '__main__':
	p = PlayCrawler()
	rs = p.getTopFree(100)
	apklist = p.parser(rs)
	print apklist