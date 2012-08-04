# This function will pull in images from etsy.com and
# Throw them into a database to be later pulled from
# to determine whether or not they have faces.

import requests
import oauth2 as oauth
import urllib
import cv
#import simplejson as json

#grabbing the authentication key from keys file
#If using this file from another source, uncomment the
#following line and include your own api key
#v2 = 'YOURAPIKEYHERE'

#comment this line if you re-defined v2
from keys import v2 as apiKey

MAX_ITEMS = 5

class ImageGrabber(object):
    def __init__(self,sandbox=False):
        if sandbox:
            self.baseUrl = 'http://sandbox.openapi.etsy.com/v2'
        else:
            self.baseUrl = 'http://openapi.etsy.com/v2'
        self.urlPayload = {'api_key': apiKey}
        self.listing_ids = []
        self.targets = []
        self.target_ids = []
    
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
        payload['limit'] = MAX_ITEMS
        s = requests.get(self.baseUrl + "/listings/active/" + category,
                         params=payload)
        

    def get_listing_image(self, listing_id):
        im = requests.get(self.baseUrl + "/listings/" + str(listing_id) + "/images",
                          params=self.urlPayload)
        results = im.json['results']
        i = 0
        for entry in results:
            imageUrl = entry['url_570xN']
            if i == 0:
                break
        urllib.urlretrieve(imageUrl, 'temp')
        tempimage = cv.LoadImage('temp')
        cv.NamedWindow('Boo!')
        cv.ShowImage('Boo!',tempimage)
        cv.WaitKey(0)
        
               
if __name__ == '__main__':
    a = ImageGrabber()
    a.get_listing_image(101188906)
