import cv
import requests

##function will check an image and return true or false

def find_face(image, debug_mode=False, listing_id=None,
              classifier="classifiers/haarcascade_frontalface_default.xml"):
    hc = cv.Load(classifier)

    faces = cv.HaarDetectObjects(image,hc,cv.CreateMemStorage(), 1.3, 3, 0, (0,0))

    ##just for debugging
    if debug_mode:
        for (x,y,w,h),n in faces:
            cv.Rectangle(image, (x,y), (x+w, y+h), 255)
        cv.SaveImage("../cached/" + classifier[12:-4] + "/"+ str(listing_id) + '.jpg', image)
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
