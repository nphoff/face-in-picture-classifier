import cv
import requests

hc = cv.Load("haarcascade_frontalface_default.xml")
##function will check an image and return true or false

def find_face(image):
    faces = cv.HaarDetectObjects(image,hc,cv.CreateMemStorage(), 1.4, 3, 1, (0,0))

    ##just for debugging
    # for (x,y,w,h),n in faces:
    #     cv.Rectangle(image, (x,y), (x+w, y+h), 255)

    # cv.NamedWindow("debug_window")
    # cv.ShowImage("debug_window", image)
    # cv.WaitKey(0)

    if faces:
        return True
    else:
        return False
if __name__ == '__main__':
    im = cv.LoadImage('temp')
    print find_face(im)
