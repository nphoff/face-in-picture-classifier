import pickle

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
                for i in range(0,len(tags)-1):
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

def cullConnectedGraph(threshold):
    connected_graph = pickle.load(open('../cached/connected_graph.p', 'rb'))
    weighted_simdex = pickle.load(open('../cached/weighted_simdex.p', 'rb'))
    for pair in weighted_simdex:
        if weighted_simdex[pair] > 0: print weighted_simdex[pair]
        # if weighted_simdex[pair] < threshold:
        #     pairlist = pair.split('<>')
        ##so close!! do this tomorrow :D    
        

def main():
    #createTagDict()
    getWeightedSimilarityIndex()
    #cullConnectedGraph(12)
    print "done!"


if __name__ == '__main__':
    main()
