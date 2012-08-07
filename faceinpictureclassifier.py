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
        

    def check_for_faces(self, classifier="haarcascade_frontalface_default.xml"):
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
    a.get_listing_ids_and_tags_from_listings("../cached/active_sundress_listings.txt")
    classifiers = [
                   'haarcascade_profileface.xml'
                   ]
    for classifier in classifiers:
        a.check_for_faces(classifier)
        pickle.dump(a.listingStatistics, open("sundress_info"+classifier[:-4] + '.p', "wb"))
    
    
