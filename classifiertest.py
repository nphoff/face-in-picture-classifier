import cv
import requests
import pickle

from imagegrabber import ImageGrabber
from faceinpictureclassifier import FaceInPictureClassifier

class ClassifierTest():

    def __init__(self):
        #add in classifiers here
        self.FIPC = FaceInPictureClassifier()
        self.classifiers = ["haarcascade_eyes_22_5.xml",
                            "haarcascade_eyes_45_11.xml",
                            "haarcascade_eye.xml",
                            "haarcascade_frontal_eyes.xml",
                            "haarcascade_frontalface_alt2.xml",
                            "haarcascade_frontalface_alt_tree.xml",
                            "haarcascade_frontalface_alt.xml",
                            "haarcascade_frontalface_default.xml",
                            "haarcascade_fullbody.xml",
                            "haarcascade_head_and_shoulders.xml",
                            "haarcascade_profileface.xml"
                            ]
    def manual_make_test(self):
        training_data = {}
        blind_test = {}
        a = FaceInPictureClassifier()
        a.get_listing_ids_from_file("../cached/active_sundress_listing_ids.txt")
        cv.NamedWindow("Contains a face? (y/n)")
        print "Making a manual test set for recognizing faces."
        print "Please press y if a picture contains a full face, n otherwise."
        print "To quit, press q."
        for i in range(0,199):
            # print a.listingIds[i]
            if i < 100:
                training_data[int(a.listingIds[i])] = {}
            else:
                blind_test[int(a.listingIds[i])] = {}
            a.imgGrabber.get_listing_image(a.listingIds[i])
            cv.ShowImage("Contains a face? (y/n)", a.imgGrabber.cvImage)
            c = 0
            print "Processing image %d of 200" % (i + 1)
            while(1):
                c = cv.WaitKey(0)
                if i < 100:
                    if c == 121:
                        training_data[int(a.listingIds[i])]['face'] = True
                        print "Previous image had face."
                        break
                    if c == 110:
                        training_data[int(a.listingIds[i])]['face'] = False
                        print "Previous image had no face."
                        break
                else:
                    if c == 121:
                        blind_test[int(a.listingIds[i])]['face'] = True
                        print "Previous image had face."
                        break
                    if c == 110:
                        blind_test[int(a.listingIds[i])]['face'] = False
                        print "Previous image had no face."
                        break
                if c == 113:
                    print "received kill command, exiting program."
                    return 0
        pickle.dump(training_data, open("testing/training_data.p", "wb"))
        pickle.dump(blind_test, open("testing/blind_test.p", "wb"))

    def run_tests(self):
        training_data_faces = 0
        detection_frontal = 0
        false_positive_frontal = 0
        detection_profile = 0
        false_positive_profile = 0
        detection_both = 0
        detection_either = 0
        false_positive_both = 0
        false_positive_either = 0

        training_data = pickle.load(open("testing/blind_test.p", "rb"))
        blind_test = pickle.load(open("testing/blind_test.p", "rb"))
        frontal_face_results = pickle.load(open("results/frontalface_alt.p", "rb"))
        profile_face_results = pickle.load(open("results/frontalface_alt2.p", "rb"))
        for listing in training_data:
            realFace = training_data[listing]['face']
            frontFace = frontal_face_results[int(listing)]['face']
            profileFace = profile_face_results[int(listing)]['face']
            if realFace:
                training_data_faces = training_data_faces + 1
            if realFace and frontFace:
                detection_frontal = detection_frontal + 1
            if realFace and profileFace:
                detection_profile = detection_profile + 1
            if frontFace and profileFace:
                if realFace:
                    detection_both = detection_both + 1
                else:
                    false_positive_both = false_positive_both + 1
            if frontFace or profileFace:
                if realFace:
                    detection_either = detection_either + 1
                else:
                    false_positive_either = false_positive_either + 1
            if frontFace and not realFace:
                false_positive_frontal = false_positive_frontal + 1
            if profileFace and not realFace:
                false_positive_profile = false_positive_profile + 1

        print("Test results:")
        print("Out of a possible %d faces." % training_data_faces)
        print("Frontal Face Classifier: \n%d detected, %d false positives" % (detection_frontal, false_positive_frontal))
        print("Profile Face Classifier: \n%d detected, %d false positives" % (detection_profile, false_positive_profile))
        print("Both Face Classifiers: \n%d detected, %d false positives" % (detection_both, false_positive_both))
        print("Either Face Classifier: \n%d detected, %d false positives" % (detection_either, false_positive_either))

    def make_new_test_data(self):
        training_data = pickle.load(open("testing/training_data.p", "rb"))
        blind_test_data = pickle.load(open("testing/blind_test.p", "rb"))
        trainingListIds = [int(x) for x in training_data]
        blindTestIds = [int(x) for x in blind_test_data]
        trainingListIds += blindTestIds
        self.FIPC.set_listing_ids(trainingListIds)
        for classifier in self.classifiers:
            print("Beginning classification for %s" % classifier[12:-4])
            self.FIPC.check_for_faces("classifiers/" + classifier)
            pickle.dump(self.FIPC.listingStatistics, open("results/" + classifier[12:-4]+ ".p", "wb"))

    def show_results(self):
        training_data = pickle.load(open("testing/blind_test.p", "rb"))
        self.classifierData = []
        trainingListIds = [int(x) for x in training_data]
        #single results:
        for classifier in self.classifiers:
            print("Classifier: %s returned the following:" % classifier)
            temp = pickle.load(open("results/" + classifier[12:-4] + ".p", "rb"))
            classifierResults = self.single_test(training_data, temp)
            classifierData.append[temp]
            print("Correct: %d" % classifierResults['Correct'])
            print("Detections: %d" % classifierResults['Detections'])
            print("False Positives: %d" % classifierResults['False Positives'])
        #mixed results:
        

    def single_test(self, training_data, test_data):
        testResults = {'Correct': 0,
                       'Detections': 0,
                       'False Positives': 0}
        
        for listingId in training_data:
            real = training_data[listingId]['face']
            test = test_data[int(listingId)]['face']
            if real == test:
                testResults['Correct'] += 1
            if real and test:
                testResults['Detections'] += 1
            if not real and test:
                testResults['False Positives'] += 1
        return testResults
            
    def merge_two_tests_and(self, test_data1, test_data2):
        mergedTestData = {}
        for listing in test_data1:
            mergedTestData[listing] = {}
            mergedTestData[listing]['face'] = test_data1[listing]['face'] and test_data2[listing]['face']
        return mergedTestData

if __name__ == '__main__':
    #manual_make_tests()
    a = ClassifierTest()
    #a.make_new_test_data()
    a.run_tests()
    #a.show_results()
