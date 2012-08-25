import pickle

from operator import itemgetter


def createTagDict():
    all_tags = {}
    with open('../cached/backup_better4k.p', 'rb') as f:
        p = pickle.load(f)
        for attr in p:
            for tag in p[attr]['tags']:
                if tag in all_tags:
                    all_tags[tag] = all_tags[tag] + 1
                else:
                    all_tags[tag] = 1
    pickle.dump(all_tags, open('../cached/all_tags.p', 'wb'))

def getTagSimilarityIndex():
    index = 1
    sim_index = {}
    connected_graph = {}
    with open('../cached/backup_better4k.p', 'rb') as f:
        p = pickle.load(f)
        for attr in p:
            tags = p[attr]['tags']
            tags.sort()
            if len(tags) > 0:
                for i in range(0,len(tags)):
                    if tags[i] not in connected_graph:
                        connected_graph[tags[i]] = tags[:i] + tags[i+1:]
                    else:
                        for tag in tags:
                            if tag != tags[i] and tag not in connected_graph[tags[i]]:
                                connected_graph[tags[i]] += [tag]
                    for j in range (i+1, len(tags)):
                        if tags[i] + "<>" + tags[j] in sim_index:
                            sim_index[tags[i] + "<>" + tags[j]] = sim_index[tags[i] + "<>" + tags[j]] + 1
                        else:
                            print index
                            index = index + 1
                            sim_index[tags[i] + "<>" + tags[j]] = 1
    pickle.dump(sim_index, open('../cached/sim_index.p', 'wb'))
    pickle.dump(connected_graph, open('../cached/connected_graph.p', 'wb'))

def getWeightedSimilarityIndex():
#The weighted similarity index is found by AB/(A+B-AB)
    index = 1
    weighted_simdex = {}
    with open('../cached/all_tags.p', 'rb') as f:
        with open('../cached/sim_index.p', 'rb') as g:
            all_tags = pickle.load(f)
            simdex = pickle.load(g)
            for pair in simdex:
                print index
                index = index + 1
                pairlist = pair.split('<>')
                weight = (float(simdex[pair])) / (all_tags[pairlist[0]] + all_tags[pairlist[1]] + simdex[pair])
                weighted_simdex[pair] = weight
    pickle.dump(weighted_simdex, open('../cached/weighted_simdex.p', 'wb'))

def cullConnectedGraph(max_size):
    #TODO: find a smarter way to cull the connected graph
    connected_graph = pickle.load(open('../cached/connected_graph.p', 'rb'))
    weighted_simdex = pickle.load(open('../cached/weighted_simdex.p', 'rb'))

    size_map = {}
    for tag in connected_graph:
        if len(connected_graph[tag]) > max_size:
            size_map[tag] = len(connected_graph[tag])
    print size_map

    #Converting the weighted simdex to a sorted list of tuples
    sorted_simdex = sorted(weighted_simdex.items(), key=itemgetter(1))
    n = len(sorted_simdex)
    found = 0
    notfound = 0
    for i in range(0, n):
        print i
        #this will cut the connections between the lowest weighted connections
        pairlist = sorted_simdex[i][0].split('<>')
        try:
            connected_graph[pairlist[0]].remove(pairlist[1])
            try:
                size_map[pairlist[0]] = size_map[pairlist[0]] - 1
            except:
                pass

            connected_graph[pairlist[1]].remove(pairlist[0])
            try:
                size_map[pairlist[1]] = size_map[pairlist[1]] - 1
            except:
                pass

            found = found + 1
        except:
            notfound = notfound + 1
            #either one doesn't exist.
            continue

        size_map = dict((k, v) for k, v in size_map.iteritems() if v > max_size)
        print "length %s" %len(size_map)
        if len(size_map) == 0:
            break
    print "n %s" %n
    print "found %s" % found
    print "not found %s" % notfound
    pickle.dump(connected_graph, open('../cached/culled_connected_graph.p', 'wb'))
    
def makeTagFeatureVector():
    sets = pickle.load(open("../cached/culled_connected_graph_sets.p", "rb"))
    listings = pickle.load(open("../cached/better_face4k.p", "rb"))
    feature_vectors = []
    n = len(sets)
    k = 0
    for listingID in listings:
        print k
        k = k + 1
        local_vector = []
        for i in range(0, n):
            if [j for j in listings[listingID]['tags'] if j in sets[i]]:
                local_vector.append(1)
            else:
                local_vector.append(0)
        if listings[listingID]['face'] == True:
            local_vector.append(1)
        else:
            local_vector.append(0)
        if listings[listingID]['days_listed'] < 30:
            local_vector.append(1)
        else:
            local_vector.append(0)
        feature_vectors.append(local_vector)
    pickle.dump(feature_vectors, open("../cached/face_feature_vector.p", "wb"))
    print "Feature vectors are organized as follows: "
    print "Indices 0 - %d are tag clusters (order preserved.)" % (n-1)
    print "Index %d is a boolean for face" % (n)
    print "Index %d is the victory condition." % (n+1)

def makeFeatureVector(filename, outfile, max_days):
    listings = pickle.load(open(filename, "rb"))
    x_feature_vectors = []
    y_vector = []
    feature_list = ['hue', 'saturation', 'views', 'tags_length', 'description_length', 'title_length', 'materials_length', 'brightness', 'is_black_and_white', 'currency_code_bool']
    #feature_list = ['hue', 'saturation', 'views', 'tags_length', 'description_length', 'title_length', 'materials_length', 'brightness']
    n = len(feature_list)
    k = 0
    rejected = 0
    outflag = False
    for listingID in listings:
        local_vector = []
        #print k
        for feature in feature_list:
            if feature in listings[listingID].keys() and listings[listingID][feature] != None:
                local_vector.append(max(listings[listingID][feature],0))
            else:
                #print("Cap'n, we've lost one!")
                outflag = True
                rejected +=1
                continue
            
        if outflag == True:
            outflag = False
            continue
        if listings[listingID]['face'] == True:
            local_vector.append(1)
        else:
            local_vector.append(0)
            
        if listings[listingID]['sales'] > 0:
            y = 1
        else:
            y = -1
        # if listings[listingID]['days_listed'] >= max_days:
        x_feature_vectors.append(local_vector)
        y_vector.append(y)
        #     k = k + 1
        
    pickle.dump(x_feature_vectors, open("../cached/" + outfile + "_x_feature_vectors.p", "wb"))
    pickle.dump(y_vector, open("../cached/" + outfile + "_y_vector.p", "wb"))


    print "Feature vectors are organized as follows: "
    print feature_list
    print "Number of vectors: %d" % len(y_vector)
    print "This should match. %d" % len(x_feature_vectors)
    print "Number of rejects: %d" % rejected

def merge_two_feature_vectors(x_feature_vector_file1, x_feature_vector_file2, y_vector1, y_vector2,output):
    ax = pickle.load(open(x_feature_vector_file1, "rb"))
    ay = pickle.load(open(y_vector1, "rb"))
    bx = pickle.load(open(x_feature_vector_file2, "rb"))
    by = pickle.load(open(y_vector2, "rb"))
    x = ax + bx
    y = ay + by
    assert len(x) == len(y)
    pickle.dump(x, open("../cached/" + output + "_x_feature_vectors.p", "wb"))
    pickle.dump(y, open("../cached/" + output + "_y_vector.p", "wb"))
        
def main():
    #createTagDict()
    #getTagSimilarityIndex()
    #getWeightedSimilarityIndex()
    #cullConnectedGraph(20)
    #makeTagFeatureVector()
    m_days = 1
    makeFeatureVector("../cached/sundress_done.p", 'sundress',m_days)
    makeFeatureVector("../cached/face_done.p", 'face4k',m_days)
    merge_two_feature_vectors("../cached/sundress_x_feature_vectors.p", "../cached/face4k_x_feature_vectors.p",
                              "../cached/sundress_y_vector.p", "../cached/face4k_y_vector.p", "merged")
    print "done!"


if __name__ == '__main__':
    main()
