#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import log

# 定义config类
class Config(object):
	"""
	配置以json格式保存，读取配置信息初始化，配置有修改时保存到文件
	"""
	def __init__(self, fileName):
		self.config = {}
		self.fileName = fileName
		if os.path.isfile(fileName):
			with open(fileName) as fp:
				fileSize = os.path.getsize(fileName)
				content = fp.read(fileSize)
				contentMap = json.loads(content, encoding='utf-8')
				for k,v in contentMap.items():
					self.config[k.encode("utf8")] = v

	def info(self):
		if self.config:
			content = json.dumps(self.config, ensure_ascii=False)
			logger.info(content)
		else:
			logger.warn('config is null')

	def change(self,level,point,isCheck):
		if level not in self.config.keys():
			self.config[level] = {}
		self.config[level]["point"] = point
		self.config[level]["onoff"] = isCheck
		content = json.dumps(self.config, ensure_ascii=False)
		fp = open(self.fileName, 'w')
		fp.write(content)
		fp.close()


# 全局参数
logger = log.Log('pet-chain.log')
# 这个不同的用户cookie不一样
cookie = ""  # 填入cookie
config = Config("config.json")




# 初始化配置
if __name__ == '__main__':
	c = Config("config.json")
	c.change('普通', 200, 2)
	c.change('稀有', 350, 1)
	c.change('卓越', 800, 1)
	c.change('史诗', 1500, 1)
	c.change('神话', 2000, 1)
	c.change('传说', 3000, 1)
	c.info()
