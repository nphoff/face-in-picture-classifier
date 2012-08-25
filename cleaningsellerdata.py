import pickle
import datetime

class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename

        self.data = pickle.load(open(self.filename, "rb"))
        

    def pull_feature_from_unfiltered(self, feature_name):
        not_found = 0
        for listingID in self.data:
            ## FIX: Sometimes the 'unfiltered' ends up as a one element list.
            if feature_name in self.data[listingID]['unfiltered'][0]:
                self.data[listingID][feature_name] = self.data[listingID]['unfiltered'][0][feature_name]
            elif feature_name in self.data[listingID]['unfiltered']:
                self.data[listingID][feature_name] = self.data[listingID]['unfiltered'][feature_name]
            else:
                not_found += 1
        print("%d listings did not contain %s" %( not_found, feature_name))

    def pull_length_of_feature_from_unfiltered(self, feature_name):
        not_found = 0
        for listingID in self.data:
            ## FIX: Sometimes the 'unfiltered' ends up as a one element list.
            if feature_name in self.data[listingID]['unfiltered'][0]:
                if self.data[listingID]['unfiltered'][0][feature_name] == None:
                    not_found += 1
                    self.data[listingID][feature_name + 'length'] = 0
                else:
                    self.data[listingID][feature_name + '_length'] = len(self.data[listingID]['unfiltered'][0][feature_name])
            elif feature_name in self.data[listingID]['unfiltered']:
                self.data[listingID][feature_name + '_length'] = len(self.data[listingID]['unfiltered'][feature_name])
            else:
                self.data[listingID][feature_name + '_length'] = 0
                not_found += 1
        print("%d listings did not contain %s, defaulting to length of zero feature." %(not_found,feature_name))
        
    def pull_boolean_of_feature_from_unfiltered(self, feature_name, truth_value):
        not_found = 0
        for listingID in self.data:
            ## FIX: Sometimes the 'unfiltered' ends up as a one element list.
            if feature_name in self.data[listingID]['unfiltered'][0]:
                if truth_value == self.data[listingID]['unfiltered'][0][feature_name]:
                    self.data[listingID][feature_name + '_bool'] = 1
                else:
                    self.data[listingID][feature_name + '_bool'] = 0
            elif feature_name in self.data[listingID]['unfiltered']:
                if truth_value == self.data[listingID]['unfiltered'][feature_name]:
                    self.data[listingID][feature_name + '_bool'] = 1
                else:
                    self.data[listingID][feature_name + '_bool'] = 0
            else:
                self.data[listingID][feature_name + '_bool'] = 0
                not_found += 1
        print("%d listings did not contain %s, defaulting to value 0" %(not_found,feature_name))

    def pull_boolean_feature_from_unfiltered(self, feature_name):
        not_found = 0
        for listingID in self.data:
            ## FIX: Sometimes the 'unfiltered' ends up as a one element list.
            if feature_name in self.data[listingID]['unfiltered'][0]:
                if self.data[listingID]['unfiltered'][0][feature_name]:
                    self.data[listingID][feature_name] = 1
                else:
                    self.data[listingID][feature_name] = 0
            elif feature_name in self.data[listingID]['unfiltered']:
                if self.data[listingID]['unfiltered'][feature_name]:
                    self.data[listingID][feature_name] = 1
                else:
                    self.data[listingID][feature_name] = 0
            else:
                self.data[listingID][feature_name] = 0
                not_found += 1
        print("%d listings did not contain %s, defaulting to value 0" %(not_found,feature_name))

    def difference_in_days(self, start, finish, name):
        for listingID in self.data:
            time1 = datetime.datetime.fromtimestamp(self.data[listingID][start])
            time2 = datetime.datetime.fromtimestamp(self.data[listingID][finish])
            days_difference = time2-time1
            self.data[listingID][name] = days_difference.total_seconds()/60/60/24

    def time_since_date(self, feature, date, name):
        for listingID in self.data:
            time = datetime.datetime.fromtimestamp(self.data[listingID][feature])
            
            days_difference = date-time
            self.data[listingID][name] = int(days_difference.total_seconds()/60/60/24)

    def repickle(self, new_filename):
        pickle.dump(self.data, open(new_filename, "wb"))
        #pickle.dump(self.data, open("backup_" + new_filename, "wb"))

if __name__ == "__main__":
    a = DataCleaner("../cached/active_sundress_listings.p")
    a.pull_feature_from_unfiltered('brightness')
    a.pull_feature_from_unfiltered('hue')
    a.pull_feature_from_unfiltered('saturation')
    a.pull_feature_from_unfiltered('description')
    a.pull_feature_from_unfiltered('views')
    a.pull_boolean_feature_from_unfiltered('is_black_and_white')
    a.pull_length_of_feature_from_unfiltered('description')
    a.pull_length_of_feature_from_unfiltered('tags')
    a.pull_length_of_feature_from_unfiltered('title')
    a.pull_length_of_feature_from_unfiltered('materials')
    a.pull_boolean_of_feature_from_unfiltered('currency_code', 'USD')
    a.pull_feature_from_unfiltered('creation_tsz')
    a.pull_feature_from_unfiltered('ending_tsz')
    ## This is the date of the scrape for the sundresses.
    scrape_date = datetime.datetime(2012,8,4,14,0)
    a.time_since_date('creation_tsz', scrape_date, 'days_listed')
    #a.difference_in_days('creation_tsz', 'ending_tsz', 'days_listed')
    a.repickle("../cached/better_active_sundress_listings.p")
    
    
