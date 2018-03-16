#!/usr/bin/env python
# -*- coding: utf-8 -*-

import log
import config
import queryPetOnSale
import genAndBuy

def main():
	query = queryPetOnSale.QueryPetOnSale(config.config.config)
	pets = query.query()
	print 'pets number:',len(pets)
	if pets:
		# pets按价格低到高来的，再排序一下，等级高的放到前面
		rankPets = []
		for rareDegree in [5,4,3,2,1,0]:
			for pet in pets:
				if pet["rareDegree"] == rareDegree:
					rankPets.append(pet)
		buy = genAndBuy.GenAndBuy(rankPets)
		buy.buy()

if __name__ == '__main__':
	main()
