# This function will pull in images from etsy.com and
# Throw them into a database to be later pulled from
# to determine whether or not they have faces.

import requests
import urllib
import cv


#grabbing the authentication key from keys file
#If using this file from another source, uncomment the
#following line and include your own api key
#v2 = 'YOURAPIKEYHERE'

#comment this line if you re-defined v2
from keys import v2 as apiKey



class ImageGrabber(object):
    def __init__(self,maxItems=5,sandbox=False):
        if sandbox:
            self.baseUrl = 'http://sandbox.openapi.etsy.com/v2'
        else:
            self.baseUrl = 'http://openapi.etsy.com/v2'
        self.urlPayload = {'api_key': apiKey}
        self.listingIds = []
        self.targets = []
        self.target_ids = []
        self.maxItems = maxItems
        self.tags = []
        
    def get_category_id(self, topCategory, subCategory=None,
                        subSubCategory = None):
        if subCategory:
            if subSubCategory:
                r = requests.get(self.baseUrl + "/categories/" +  topCategory
                                 + "/" + subCategory + "/" + subSubCategory,
                                 params=self.urlPayload)
            else:
                r = requests.get(self.baseUrl + "/categories/" + topCategory +                                 "/" + subCategory,
                                 params=self.urlPayload)
        else:
            r = requests.get(self.baseUrl + "/categories/" + topCategory,
                             params=self.urlPayload)
        return r.json['results']['category_id']

    def get_category_listing_ids(self,category):
        payload = self.urlPayload
        payload['limit'] = self.maxItems
        payload['category'] = category
        s = requests.get(self.baseUrl + "/listings/active/",
                         params=payload)
        for entry in s.json['results']:
            self.listingIds.append(entry['listing_id'])

    def get_listing_image(self, listing_id):
        try:
            self.cvImage = cv.LoadImage("/home/nathan/coding/cached/images/" + str(listing_id))
        except IOError as e:
                im = requests.get(self.baseUrl + "/listings/" + str(listing_id) + "/images",
                                  params=self.urlPayload)
                results = im.json['results']
                i = 0
                for entry in results:
                    imageUrl = entry['url_570xN']
                    break #take one.
                urllib.urlretrieve(imageUrl, "../cached/images/" + str(listing_id))
                self.cvImage = cv.LoadImage("../cached/images/" + str(listing_id))
        #cv.NamedWindow('debug_window')
        #cv.ShowImage('debug_window',tempimage)
        #cv.WaitKey(0)
                
    def set_listing_ids(self, inputListingIdList):
        self.listingIds = inputListingIdList

    def get_listing_tags(self, listing_id):
        self.tags = []
        tagdata = requests.get(self.baseUrl + "/listings/" + str(listing_id),
                               params=self.urlPayload)
        results = tagdata.json['results']
        self.unfiltered_results = results
        for attr in results:
            if 'tags' in attr:
                tags = attr['tags']
                self.tags = tags
        
if __name__ == '__main__':
    cv.NamedWindow("debug_window")
    a = ImageGrabber(20)
    a.get_category_listing_ids('clothing/dress/sundress')
    for image in a.listingIds:
        a.get_listing_image(image)
        cv.ShowImage('debug_window', a.cvImage)
        cv.WaitKey(0)
