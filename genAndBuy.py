#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import urllib2
import base64
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class GenAndBuy(object):
	def __init__(self, pets):
		self.pets = pets

	@staticmethod
	def packGenPost():
		post = {}
		post["appId"] = 1
		post["requestId"] = int(time.time() * 1000)
		post["nounce"] = None
		post["timeStamp"] = None
		post["token"] = None
		post["tpl"] = ""
		return json.dumps(post)

	def gen(self, petid):
		genUrl = "https://pet-chain.baidu.com/data/captcha/gen"
		genHeader = {'content-type': 'application/json', 'Cookie': config.cookie}
		postStr = GenAndBuy.packGenPost()
		req = urllib2.Request(url=genUrl,data=postStr,headers=genHeader)
		res = urllib2.urlopen(req)
		res = res.read()
		res = json.loads(res, encoding='utf-8')
		if res['data']['img']:
			pic = base64.b64decode(res['data']['img'])
			fp = open("./vercode/" + petid + '.jpeg', 'wb')
			fp.write(pic)
			fp.close()
			seed = res['data']['seed']
			return True, seed
		else:
			config.logger.error("没有获取到验证码")
			return False, None

	@staticmethod
	def packCreatePost(petid, point, seed, rareDegree):
		degree_map = {0:'普通',1:'稀有',2:'卓越',3:'史诗',4:'神话',5:'传说'}
		print petid, point, degree_map[rareDegree].decode('utf8')
		post = {}
		post["appId"] = 1
		post["nounce"] = None
		post["timeStamp"] = None
		post["token"] = None
		post["tpl"] = ""
		post["validCode"] = ""
		post["requestId"] = int(time.time() * 1000)
		post["petId"] = petid
		post["amount"] = str(point)
		post["seed"] = seed
		post["captcha"] = raw_input("input the verification code:")
		postStr = json.dumps(post)
		return postStr

	def create(self, petid, point, seed, rareDegree):
		createUrl = "https://pet-chain.baidu.com/data/txn/create"
		createHeader = {'content-type': 'application/json', 'Cookie': config.cookie}
		postStr = GenAndBuy.packCreatePost(petid, point, seed, rareDegree)
		os.remove("./vercode/" + petid + '.jpeg')  # 删除下载的验证码图片
		req = urllib2.Request(url=createUrl,data=postStr,headers=createHeader)
		res = urllib2.urlopen(req)
		res = res.read()
		res = json.loads(res, encoding='utf-8')
		if res['errorNo'] == "00":
			return True
		else:
			config.logger.error(res["errorMsg"])
			return False

	def buy(self):
		for pet in self.pets:
			res, seed = self.gen(pet["petId"])
			if res == True:
				res = self.create(pet["petId"], pet["amount"], seed, pet["rareDegree"])
				if res == True:
					config.logger.info("buy pet %s success!" % pet["petId"])
					break
			else:
				config.logger.error("petid %s gen failed!" % pet["petId"])
