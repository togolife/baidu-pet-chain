#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import json
import urllib2
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class QueryPetOnSale(object):
	url = "https://pet-chain.baidu.com/data/market/queryPetsOnSale"
	header_dict = {'content-type': 'application/json'}
	degree_map = {0:'普通',1:'稀有',2:'卓越',3:'史诗',4:'神话',5:'传说'}
	
	@staticmethod
	def packPost(pageNo):
		post = {}
		post["appId"] = 1
		post["pageNo"] = pageNo
		post["pageSize"] = 20
		post["querySortType"] = "AMOUNT_ASC"
		post["requestId"] = int(time.time() * 1000)
		post["lastAmount"] = None
		post["lastRareDegree"] = None
		post["nounce"] = None
		post["petIds"] = []
		post["timeStamp"] = None
		post["token"] = None
		post["tpl"] = ""
		return json.dumps(post)

	def __init__(self, config):
		self.config = config

	def query(self):
		check = False
		max_point = 0
		# 检查config配置，如果都关闭了则没必要去查询
		for k,v in self.config.items():
			if v["onoff"] == 1:
				check = True
			if v["point"] > max_point:
				max_point = v["point"]
		if check == False:
			return []
		pets = []
		pageNo = 0
		while True:
			pageNo += 1
			postStr = QueryPetOnSale.packPost(pageNo)
			config.logger.info(postStr)
			req = urllib2.Request(url=QueryPetOnSale.url,data=postStr,headers=QueryPetOnSale.header_dict)
			res = urllib2.urlopen(req)
			res = res.read()
			config.logger.info(res)

			res = json.loads(res, encoding='utf-8')
			if res['errorNo'] != "00":
				config.logger.error(res['errorMsg'])
				break
			elif not res['data']['petsOnSale'] or \
				res['data']['hasData'] == False:
				config.logger.info("data is null, has no data!")
				break
			else:
				petsOnSale = res['data']['petsOnSale']
				isEnd = False
				for pet in petsOnSale:
					rareDegree = pet['rareDegree']  # 稀有度  0普通 1稀有 2卓越 3史诗 4神话 5传说
					point = float(pet['amount'])    # 卖多少积分
					if point > max_point:
						isEnd = True
					if  QueryPetOnSale.degree_map[rareDegree] in self.config.keys() and \
						self.config[QueryPetOnSale.degree_map[rareDegree]]["onoff"] == 1 and \
						self.config[QueryPetOnSale.degree_map[rareDegree]]["point"] >= point:
						pets.append(pet)

				if isEnd:
					config.logger.info('query pet on sale is end!')
					break
		return pets
