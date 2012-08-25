import csv
import datetime
import time
import pickle

import sqlite3 as lite

def aggregate_seller_data(seller_tsv_filename):
    sellers = csv.reader(open(seller_tsv_filename, 'r'), delimiter = '\t')
    aggregate_dict = {}
    i = 0
    timeformat = '%Y-%m-%d %H:%M:%S'
    for row in sellers:
        i += 1
        if i % 1000 == 0:
            print("At transaction %d" % i)
        try:
            posted_date = datetime.datetime.strptime(trim_date(row[4]),timeformat)
            sold_date = datetime.datetime.strptime(trim_date(row[3]),timeformat)
            days_listed = int((sold_date - posted_date).total_seconds()/(24*60*60))
        except:
            continue
        if row[1] not in aggregate_dict:
            aggregate_dict[row[1]] = {}
            aggregate_dict[row[1]]['sales'] = int(row[2])
            aggregate_dict[row[1]]['time_posted'] = trim_date(row[4])
            aggregate_dict[row[1]]['days_listed'] = days_listed
            aggregate_dict[row[1]]['max_listing_length'] = days_listed
        else:
            weighted_listed_time = aggregate_dict[row[1]]['sales'] * aggregate_dict[row[1]]['days_listed']
            aggregate_dict[row[1]]['sales'] += int(row[2])
            aggregate_dict[row[1]]['days_listed'] = int((weighted_listed_time + days_listed) / aggregate_dict[row[1]]['sales'])
            if days_listed > aggregate_dict[row[1]]['max_listing_length']:
                aggregate_dict[row[1]]['max_listing_length'] = days_listed
    for listing in aggregate_dict:
        aggregate_dict[listing]['average_sale_time'] = float(aggregate_dict[listing]['max_listing_length']) / aggregate_dict[listing]['sales']
    pickle.dump(aggregate_dict, open("../cached/big_sellers_listings.p", 'wb'))


def make_listingID_list(pickled_aggregate_dict_filename):
    #This makes an iterable list of listings such that if more data is desired,
    #it can be obtained without taking duplicates.  (just take a certain range from
    #this list.)
    listingID_list = []
    aggregate_dict = pickle.load(open(pickled_aggregate_dict_filename, "rb"))
    for entry in aggregate_dict:
        listingID_list.append(entry)
    print listingID_list
    print len(listingID_list)
    pickle.dump(listingID_list, open("../cached/listingID_list.p", "wb"))

def trim_date(date):
    c = date.find('.')
    d = date.find('+')
    if c == -1:
        return date[:d]
    return date[:c]

def create_database_from_pickled_files(pickled_data_filename, pickled_listings_filename):
    data = pickle.load(open(pickled_data_filename, 'rb'))
    listingID_list = pickle.load(open(pickled_listings_filename, 'rb'))
    con = lite.connect("../cached/FIP.db")
    with con:
        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS Listings')
        cur.execute('CREATE TABLE IF NOT EXISTS Listings(id INTEGER PRIMARY KEY autoincrement, listingid INT, sales INT, time_posted TEXT, days_listed INT, max_listing_length INT, average_sale_time INT)')
    i = 0
    for listingID in data:
        
        cur.execute('INSERT INTO Listings(listingid, sales, time_posted, days_listed, max_listing_length, average_sale_time) VALUES(?,?,?,?,?,?)', ( listingID, data[listingID]['sales'],data[listingID]['time_posted'], data[listingID]['days_listed'], data[listingID]['max_listing_length'], data[listingID]['average_sale_time']))
    con.commit()
    

def add_sales_to_dict_of_listings(sales_pickle_file, dict_of_listings, output_file):
    listings = pickle.load(open(dict_of_listings, 'rb'))
    sales_dict = pickle.load(open(sales_pickle_file, 'rb'))
    found = 0
    not_found = 0
    for listingID in listings:
        if str(listingID) in sales_dict:
            listings[listingID]['sales'] = sales_dict[str(listingID)]['sales']
            listings[listingID]['average_sale_time'] = sales_dict[str(listingID)]['average_sale_time']
            found += 1
        else:
            listings[listingID]['sales'] = 0
    
            not_found +=1
    print("%d listings found, %d not found." %(found, not_found))
    pickle.dump(listings, open(output_file, 'wb'))

if __name__ == "__main__":
    #aggregate_seller_data("/home/nathan/coding/FaceInPictureClassifier/etsydata/listings.tsv")
    #make_listingID_list("../cached/big_sellers_listings.p")
    #create_database_from_pickled_files("../cached/big_sellers_listings.p", "../cached/listingID_list.p")
    #add_sales_to_dict_of_listings("../cached/big_sellers_listings.p", "../cached/better_face_active_sundresses_sales.p", "../cached/sundress_done.p")                
    add_sales_to_dict_of_listings("../cached/big_sellers_listings.p", "../cached/best_face4k.p", "../cached/face_done.p")                
