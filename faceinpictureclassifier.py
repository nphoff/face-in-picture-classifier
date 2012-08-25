import cv
import requests
import pickle
import numpy

import sqlite3 as lite

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
    
    def get_listing_data_from_pickled(self, pickle_filename, listing_id_list_filename, start, limit):
        self.pickle_file = pickle.load(open(pickle_filename,"rb"))
        listing_id_list = pickle.load(open(listing_id_list_filename, "rb"))
        
        for j in range(start,start+limit):
            listing_id = int(listing_id_list[j])
            print("Processing Listing ID number %d: %d" % (j, listing_id))
            self.listingIds.append(listing_id)
            if listing_id not in self.listingStatistics:
                self.listingStatistics[listing_id] = self.pickle_file[str(listing_id)]
            self.imgGrabber.get_listing_tags(listing_id)
            self.listingStatistics[listing_id]['tags'] = self.imgGrabber.tags
            self.listingStatistics[listing_id]['unfiltered'] = self.imgGrabber.unfiltered_results
        #self.check_for_faces()
    
    def get_listing_data_from_database(self, database_file, start, limit):
        con = lite.connect(database_file)
        with con:
            make_columns_flag = False
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute('PRAGMA TABLE_INFO(Listings)')
            labels = cur.fetchall()
            for label in labels:
                print label
                if 'tags' in label or 'unfiltered' in label:
                    make_columns_flag = True
                    break
            if not make_columns_flag:
                cur.execute('ALTER TABLE Listings ADD COLUMN tags BLOB')
                cur.execute('ALTER TABLE Listings ADD COLUMN unfiltered BLOB')
            cur.execute('SELECT * FROM Listings WHERE id >= ? AND id < ?', (start, start+limit))
            rows = cur.fetchall()
            for row in rows:
                listing_id = row['listingid']
                self.listingIds.append(listing_id)
                if listing_id not in self.listingStatistics:
                    self.listingStatistics[listing_id] = {}
                    for i in range(2,len(row)):
                        self.listingStatistics[listing_id][labels[i][1]] =row[i]
                self.imgGrabber.get_listing_tags(listing_id)
                self.listingStatistics[listing_id]['tags'] = self.imgGrabber.tags
                self.listingStatistics[listing_id]['unfiltered'] = self.imgGrabber.unfiltered_results
                cur.execute('INSERT INTO Listings(tags, unfiltered) VALUES (?, ?)', (self.listingStatistics[listing_id]['tags'], self.listingStatistics[listing_id]['unfiltered']))
            con.commit()
                
    def check_face_for_pickled(self, pickle_filename, classifier="haarcascade_frontalface_alt.xml"):
        self.pickle_data = pickle.load(open(pickle_filename,"rb"))
        i = 0
        n = len(self.pickle_data)
        for listingId in self.pickle_data:
            print("Processing %d of %d images." % (i,n))
            i = i + 1
            self.imgGrabber.get_listing_image(listingId)
            self.pickle_data[listingId]['face'] = find_face(self.imgGrabber.cvImage, True, listingId, classifier)
            

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
            self.listingStatistics[listingId]['unfiltered'] = [singleListing]
        

    def check_for_faces(self, classifier="haarcascade_frontalface_alt.xml"):
        n = len(self.listingIds)
        i = 0
        faces = 0
        non_faces = 0
        for listingId in self.listingIds:
            if listingId not in self.listingStatistics:
                self.listingStatistics[listingId] = {}
            print("Processing %d of %d images." % (i,n))
            i = i + 1
            self.imgGrabber.get_listing_image(listingId)
            self.listingStatistics[listingId]['face'] = find_face(self.imgGrabber.cvImage, True, listingId, classifier)
            if self.listingStatistics[listingID]['face']:
                faces += 1
            else:
                non_faces += 1

        print("%d faces found, %d not found." % (faces, non_faces))


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

    def determine_face_sales_correlation(self, data_filename):
        data = pickle.load(open(data_filename, "rb"))
        #The naive approach at determining the effect of a face on purchasability:
        face_sales = 0
        face_average_days_listed = 0
        no_face_sales = 0
        no_face_average_days_listed = 0
        total_faces = 0
        non_faces = 0
        face_sales_list = []
        no_face_sales_list = []
        face_days_list = []
        no_face_days_list = []
        for entry in data:
            if data[entry]['face']:
                total_faces += 1
                face_sales += data[entry]['sales']
                face_average_days_listed += data[entry]['days_listed'] * data[entry]['sales']

                face_sales_list.append(data[entry]['sales'])
                for j in range(0,data[entry]['sales']):
                    face_days_list.append(data[entry]['days_listed'])

            else:
                non_faces += 1
                no_face_sales += data[entry]['sales']
                no_face_average_days_listed += data[entry]['days_listed'] * data[entry]['sales']
                
                no_face_sales_list.append(data[entry]['sales'])
                for j in range(0,data[entry]['sales']):
                    no_face_days_list.append(data[entry]['days_listed'])

        maxfacedayslist = max(sorted(face_days_list))
        maxnofacedayslist = max(sorted(no_face_days_list))
        print "max face %s" % maxfacedayslist
        print "max no face %s" % maxnofacedayslist

        face_average_days_listed /= face_sales
        no_face_average_days_listed /= no_face_sales
        
        print("There were a total of %d images with faces, %d without." % (total_faces, non_faces))
        print("The number of sales for listings with faces is: %d with an average number of days is %d" % (face_sales, face_average_days_listed))
        print("The number of sales for listings without faces is: %d with an average number of days is %d" % (no_face_sales, no_face_average_days_listed))
        print("The average sales per listing was %d with a standard error of %d for listings with faces." % (numpy.average(face_sales_list), numpy.std(face_sales_list)/numpy.sqrt(non_faces)))
        print("The average sales per listing was %d with a standard error of %d for listings without faces." % (numpy.average(no_face_sales_list), numpy.std(no_face_sales_list)/numpy.sqrt(non_faces)))
        print("The average days per listing was %d with a standard error of %d for listings with faces." % (numpy.average(face_days_list), numpy.std(face_days_list)/numpy.sqrt(non_faces)))
        print("The average days per listing was %d with a standard error of %d for listings without faces." % (numpy.average(no_face_days_list), numpy.std(no_face_days_list)/numpy.sqrt(non_faces)))

    def determine_face_views_sales_correlation(self, data_filename):
        data = pickle.load(open(data_filename, "rb"))
        #The naive approach at determining the effect of a face on purchasability:
        face_sales = 0
        face_average_views = 0
        no_face_sales = 0
        no_face_average_views = 0
        total_faces = 0
        non_faces = 0
        face_sales_list = []
        no_face_sales_list = []
        face_views_list = []
        no_face_views_list = []
        for entry in data:
            if 'views' in data[entry].keys():
                if data[entry]['face']:
                    total_faces += 1
                    face_sales += data[entry]['sales']
                    face_sales_list.append(data[entry]['sales'])
                    face_views_list.append(data[entry]['views'])

                else:
                    non_faces += 1
                    no_face_sales += data[entry]['sales']
                    no_face_sales_list.append(data[entry]['sales'])
                    no_face_views_list.append(data[entry]['views'])

        
        max_views_face_list = numpy.max(face_views_list)
        max_views_no_face_list = numpy.max(no_face_views_list)
        print("max of views with a face: %d, without: %d" % (max_views_face_list, max_views_no_face_list))
        

        print("There were a total of %d images with faces, %d without." % (total_faces, non_faces))
        # print("The number of sales for listings with faces is: %d with an average number of views is %d" % (face_sales, face_average_views))
        # print("The number of sales for listings without faces is: %d with an average number of days is %d" % (no_face_sales, no_face_average_views)
        print("The average sales per listing was %d with a standard error of %d for listings with faces." % (numpy.average(face_sales_list), numpy.std(face_sales_list)/numpy.sqrt(total_faces)))
        print("The average sales per listing was %d with a standard error of %d for listings without faces." % (numpy.average(no_face_sales_list), numpy.std(no_face_sales_list)/numpy.sqrt(non_faces)))
        print("The average views per listing was %d with a standard error of %d for listings with faces." % (numpy.average(face_views_list), numpy.std(face_views_list)/numpy.sqrt(total_faces)))
        print("The average views per listing was %d with a standard error of %d for listings without faces." % (numpy.average(no_face_views_list), numpy.std(no_face_views_list)/numpy.sqrt(non_faces)))


if __name__ == "__main__":
    a = FaceInPictureClassifier()
    # classifier = "classifiers/haarcascade_frontalface_alt.xml"
    #a.get_listing_data_from_pickled("../cached/big_sellers_listings.p","../cached/listingID_list.p", 0,4000)
    #pickle.dump(a.listingStatistics, open("../cached/first4k.p", "wb"))
    #a.get_listing_ids_and_tags_from_listings("../cached/active_sundress_listings.txt")
    #pickle.dump(a.listingStatistics, open("../cached/active_sundress_listings.p","wb"))
    # b = FaceInPictureClassifier()
    # b.get_listing_ids_and_tags_from_listings("../cached/test.txt")
    # pickle.dump(b.listingStatistics, open("../cached/test.p", "wb"))
    # #a.check_for_faces(classifier)
    a.check_face_for_pickled("../cached/better_active_sundress_listings_sales.p")
    pickle.dump(a.pickle_data, open("../cached/better_face_active_sundresses_sales.p", "wb"))
    #a.determine_face_views_sales_correlation("../cached/better_face_active_sundresses.p")
    #a.get_listing_data_from_database("../cached/FIP.db", 1,50)
