import cv
import requests
from findface import find_face
from imagegrabber import ImageGrabber
from keys import v2 as apiKey

a = ImageGrabber(5)
cv.NamedWindow("Double Checking")
a.get_category_listing_ids('clothing/dress/sundress')
for picture in a.listingIds:
    a.get_listing_image(picture)
    print find_face(a.cvImage)
    cv.ShowImage("Double Checking", a.cvImage)
    cv.WaitKey(0)
