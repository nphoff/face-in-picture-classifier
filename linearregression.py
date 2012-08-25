import pickle

from sklearn import linear_model

clf = linear_model.LinearRegression()
data = pickle.load(open("../cached/new_face_feature_vector.p", "rb"))
yvals = []
for i in range(0, len(data)):
    yvals.append(data[i].pop())

clf.fit(data, yvals)
print clf.coef_
    
