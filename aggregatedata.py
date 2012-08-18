import csv
import datetime
import time
import pickle


def aggregate_seller_data(seller_tsv_filename):
    sellers = csv.reader(open(seller_tsv_filename, 'r'), delimiter = '\t')
    aggregate_dict = {}
    i = 0
    timeformat = '%Y-%m-%d %H:%M:%S'
    for row in sellers:
        i += 1
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
        else:
            weighted_listed_time = aggregate_dict[row[1]]['sales'] * aggregate_dict[row[1]]['days_listed']
            aggregate_dict[row[1]]['sales'] += int(row[2])
            aggregate_dict[row[1]]['days_listed'] = int((weighted_listed_time + days_listed) / aggregate_dict[row[1]]['sales'])
    
    pickle.dump(aggregate_dict, open("sellers_listings.p", 'wb'))


def trim_date(date):
    c = date.find('.')
    d = date.find('+')
    if c == -1:
        return date[:d]
    return date[:c]

if __name__ == "__main__":
    aggregate_seller_data("etsydata/listings.tsv")
