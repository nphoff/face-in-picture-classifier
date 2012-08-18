import pickle

class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = pickle.load(open(self.filename, "rb"))
        

    def pull_feature_from_unfiltered(self, feature_name):
        for listingID in self.data:
            if feature_name in self.data[listingID]['unfiltered']:
                print "Found one!"
                self.data[listingID][feature_name] = self.data[listingID]['unfiltered'][feature_name]

    def repickle(self, new_filename):
        pickle.dump(self.data, open(new_filename, "wb"))
        pickle.dump(self.data, open("backup_" + new_filename, "wb"))







if __name__ == "__main__":
    a = DataCleaner("first1k_info.p")
    a.pull_feature_from_unfiltered('brightness')
    a.pull_feature_from_unfiltered('hue')
    a.pull_feature_from_unfiltered('saturation')
    a.pull_feature_from_unfiltered('description')
    a.pull_feature_from_unfiltered('views')
    a.repickle("better4k.p")
    
    
