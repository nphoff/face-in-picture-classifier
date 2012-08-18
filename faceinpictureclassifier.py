import cv
import requests
import pickle

from findface import find_face
from imagegrabber import ImageGrabber


class FaceInPictureClassifier(object):

    def __init__(self):
        self.listingIds = []
        self.imgGrabber = ImageGrabber()
        self.listingStatistics = {}

    def get_listing_ids_from_file(self,listingIdFilename):
        self.listingIdFile = open(listingIdFilename, 'r')
        for line in self.listingIdFile:
            if line.strip() not in self.listingStatistics:
                self.listingStatistics[line.strip()] = {}
                self.listingIds.append(line.strip())
        self.listingIdFile.close()
    
    def get_listing_data_from_pickled(self, pickle_filename, limit):
        self.pickle_file = pickle.load(open(pickle_filename,"rb"))
        i = 0
        for listing_id in self.pickle_file:
            i += 1
            print("Processing Listing ID number %d: %d" % (i, int(listing_id)))
            self.listingIds.append(int(listing_id))
            if int(listing_id) not in self.listingStatistics:
                self.listingStatistics[int(listing_id)] = self.pickle_file[listing_id]
            self.imgGrabber.get_listing_tags(int(listing_id))
            self.listingStatistics[int(listing_id)]['tags'] = self.imgGrabber.tags
            self.listingStatistics[int(listing_id)]['unfiltered'] = self.imgGrabber.unfiltered_results
            if i > limit:
                break
        #self.check_for_faces()
        
    def check_face_for_pickled(self, pickle_filename):
        self.pickle_data = pickle.load(open(pickle_filename,"rb"))
        i = 0
        n = len(self.pickle_data)
        for listingId in self.pickle_data:
            print("Processing %d of %d images." % (i,n))
            i = i + 1
            try:
                self.imgGrabber.get_listing_image(listingId)
                self.pickle_data[listingId]['face'] = find_face(self.imgGrabber.cvImage, True, listingId, classifier)
            except:
                self.pickle_data[listingId]['face'] = None


    def get_listing_ids_and_tags_from_listings(self, listingFilename):
        self.listingFile = open(listingFilename, 'r')
        for line in self.listingFile:
            singleListing = eval(line)
            listingId = singleListing['listing_id']
            tags = singleListing['tags']
            if listingId not in self.listingStatistics:
                self.listingStatistics[listingId] = {}
                self.listingIds.append(listingId)
            self.listingStatistics[listingId]['tags'] = tags
        

    def check_for_faces(self, classifier="classifiers/haarcascade_frontalface_alt.xml"):
        n = len(self.listingIds)
        i = 0
        for listingId in self.listingIds:
            if listingId not in self.listingStatistics:
                self.listingStatistics[listingId] = {}
            print("Processing %d of %d images." % (i,n))
            i = i + 1
            self.imgGrabber.get_listing_image(listingId)
            self.listingStatistics[listingId]['face'] = find_face(self.imgGrabber.cvImage, True, listingId, classifier)
                
    def set_listing_ids(self, listingIdList):
        self.listingIds = listingIdList

    def reset_statistics(self):
        self.listingStatistics = {}
    # with open("../cached/active_sundress_listing_ids.txt",'r') as f:
    #     for line in f:
    #         listingIds.append(line.strip())
            
    #         a = ImageGrabber()
    #         i = 0

    #         for listingId in self.listingIds:
    #             print i + 1
    #             print listingId
    #             i = i+ 1
    #             a.get_listing_image(listingId)
                
    # print find_face(a.cvImage)
    # cv.ShowImage("Double Checking", a.cvImage)
    # cv.WaitKey(0)



if __name__ == "__main__":
    a = FaceInPictureClassifier()
    classifier = "classifiers/haarcascade_frontalface_alt.xml"
    #a.get_listing_data_from_pickled("sellers_listings.p", 4000)
    # a.get_listing_ids_and_tags_from_listings("../cached/active_sundress_listings.txt")
    #a.check_for_faces(classifier)
    a.check_face_for_pickled("better4k.p")
    pickle.dump(a.pickle_data, open("face4k.p", "wb"))
    
    
