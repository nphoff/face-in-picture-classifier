from random import randint
from numpy import *
from math import sqrt
import pickle
from sklearn import svm
from sklearn.feature_selection import RFE
from random import shuffle

def pegasos(x,y):
    accuracy = 0.90
    confidence = 0.89
    feat_x, feat_y = array(x), array(y)
    #incorporate a bias term!
    l = 0.0001
    num_iterations = int(float(1)/(accuracy*confidence*l))
    assert len(feat_y) == len(feat_x)
    num_examples, num_features = feat_x.shape
    #print num_iterations,num_examples, num_features 
    weight =  zeros([num_features], float)
    #weight.fill(1/(num_features*sqrt(l)))
    for it in xrange(1, num_iterations + 1):
        i = randint(0, num_examples - 1)
        random_feat = feat_x[i]
        if feat_y[i] * dot(random_feat,weight) < 1:
            weight = (1 - float(1)/it) * weight + \
                     (float(1)/(l * it)) * feat_y[i] * random_feat
            #print '1',weight
        else:
            weight = (1 - float(1)/it) * weight
            #print '2',weight
    return weight
    
def getAccuracy(Ytest,Ypredict):
    assert len(Ytest) == len(Ypredict)
    score, fail = 0, 0
    for i in range(0,len(Ytest)):
        if Ytest[i] * Ypredict[i] > 0:
            score += 1
        else:
            fail += 1
    return float(score)/(score+fail)

if __name__=="__main__":
    X = pickle.load(open('../cached/merged_x_feature_vectors.p', 'rb'))
    Y = pickle.load(open('../cached/merged_y_vector.p', 'rb'))
    k = 10
    SVM_accuracy = 0
    pegasos_accuracy = 0
    weight = []
    expected = max(1 - float(len([i for i in Y if i>0]))/float(len(Y)), float(len([i for i in Y if i>0]))/float(len(Y)))
    print "expected %f" %expected
    X_shuf = []
    Y_shuf = []
    index_shuf = range(len(X))
    print len(X)
    print len(Y)
    shuffle(index_shuf)
    for i in index_shuf:
        X_shuf.append(X[i])
        Y_shuf.append(Y[i])
    X = X_shuf
    Y = Y_shuf
    for i in range(k):
        lower_bound = i*len(X)/k
        upper_bound = (i+1)*len(X)/k
        Xtest = X[lower_bound:upper_bound]
        Ytest = Y[lower_bound:upper_bound]
        Xtrain = X[0:lower_bound] + X[upper_bound:len(X)]
        Ytrain = Y[0:lower_bound] + Y[upper_bound:len(X)]
        clf = svm.SVC(kernel='rbf') #change params here
        clf.fit(Xtrain,Ytrain)
        Ypredict1 = clf.predict(Xtest)
        SVM_accuracy += getAccuracy(Ytest, Ypredict1)
        weight = pegasos(Xtrain,Ytrain)
        Ypredict2 = []
        for Xrow in Xtest:
            Ypredict2.append(dot(Xrow,weight))
        pegasos_accuracy += getAccuracy(Ytest, Ypredict2)
    SVM_accuracy /= k
    pegasos_accuracy /= k

    print "accuracy for sklearn SVM is %f" % SVM_accuracy
    print "accuracy for pegasos is %f" % pegasos_accuracy

    '''
    feature_list = [[1,1,0,0],[1,1,3,0],[0,0,1,1],[0,0,1,1],[1,1,0,0]]
    label_list = [1,1,-1,-1,1]
    weight = pegasos(feature_list,label_list)
    tfeature_list = [[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1],[1,1,0,0]]
    tlabel_list = [1,1,-1,-1,1]
    '''

