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

def get_listings(limit):
	url = 'http://openapi.etsy.com/v2/listings/active?limit=' + str(limit) + '&api_key=' + api_key + '&category=clothing/dress/sundress'
	r = requests.get(url)
	j = r.json['results']
	with open('../cached/sundress_listings.txt','w') as f:
		for k in j:
			f.write(str(k)+"\n")

def main():
	limit = 10
	get_listings(limit)

if __name__ == '__main__':
	main()

# get all transactions, 
