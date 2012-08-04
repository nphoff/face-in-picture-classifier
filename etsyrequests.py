import requests
import json
from keys import v2 as api_key

def get_users(limit):
	url = 'http://openapi.etsy.com/v2/users?limit=' + str(limit) + '&api_key=' + api_key
	r = requests.get(url)
	j = r.json['results']
	for k in j:
		print k['user_id']

def get_shops(limit):
	url = 'http://openapi.etsy.com/v2/shops?limit=' + str(limit) + '&api_key=' + api_key
	r = requests.get(url)
	j = r.json['results']
	for k in j:
		print k['shop_id']

def get_active_listings(limit):
	with open('../cached/active_sundress_listings.txt','w') as f:
		for offset in range(0, 10000, 100):
			print offset
			url = 'http://openapi.etsy.com/v2/listings/active?limit=' + str(limit) + '&api_key=' + api_key + '&category=clothing/dress/sundress&offset=' + str(offset)
			r = requests.get(url)
			j = r.json['results']
			for k in j:
				f.write(str(k) + '\n')

def get_sellers_for_listings():
	with open('../cached/active_sundress_listings.txt','r') as f:
		with open('../cached/active_sundress_sellers.txt','w') as g:
			for line in f:
				listing_id = eval(line)
				g.write(str(listing_id['user_id']) + '\n')

def get_shops_for_sellers(limit):
	numshops = 0
	with open('../cached/active_sundress_sellers.txt','r') as f:
		with open('../cached/active_sundress_shops.txt','w') as g:
			for user_id in f:
				print numshops
				user_id = user_id.strip()
				url = 'http://openapi.etsy.com/v2/users/' + str(user_id) + '/shops?limit=' + str(limit) + '&api_key=' + api_key
				r = requests.get(url)
				j = r.json['results']
				for k in j:
					numshops = numshops + 1
					g.write(str(k['shop_id']) + '\n')

def get_transactions_for_shops(limit):
	numtrans = 0
	with open('../cached/active_sundress_shops.txt','r') as f:
		with open('../cached/active_sundress_transactions.txt','w') as g:
			for shop_id in f:
				print numtrans
				shop_id = shop_id.strip()
				url = 'http://openapi.etsy.com/v2/shops/' + str(shop_id) + '/transactions?limit=' + str(limit) + '&api_key=' + api_key
				r = requests.get(url)
				print r.content
				j = r.json['results']
				for k in j:
					numtrans = numtrans + 1
					g.write(str(k['transaction_id']) + '\n')

def main():
	limit = 100
	#get_active_listings(limit) #comment out after cached
	#get_sellers_for_listings()
	#get_shops_for_sellers(limit)
	get_transactions_for_shops(limit)
	print "done!"


if __name__ == '__main__':
	main()

# get all transactions, 
