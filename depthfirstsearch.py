import pickle

class DepthFirstSearch(object):
    #depth first search done on object where each node has a list of
    #associated nodes, output is connected sets of nodes.
    #Expects an un-directed graph (ie. each connected node has a
    #reference all nodes it is connected to.)
    
    def __init__(self):
        self.stack = []
        self.visited = []
        self.connected_sets = []
        self.filename = ""
    
    def import_pickled(self, pickled_filename):
        self.filename = pickled_filename
        self.node_data = pickle.load(open(self.filename, 'rb'))
        self.nodes = self.node_data.keys()
        
    def find_connected(self, start_node):
        visited = []
        visited.append(start_node)
        self.stack += self.node_data[start_node]
        while self.stack:
            if self.stack[-1] not in visited:
                self.current_node = self.stack.pop()
                if self.current_node in self.node_data:
                    self.stack += self.node_data[self.current_node]
                visited.append(self.current_node)
            else:
                self.stack.pop()
        self.connected_sets.append(visited)
        self.visited += visited
    
    def find_all_connected(self):
        for node in self.nodes:
            if node not in self.visited:
                self.find_connected(node)

    def pickle_results(self):
        if self.filename:
            pickle.dump(open(self.filename[:-2] + "_sets.p", "wb"))
        else:
            pickle.dump(open("../cached/connected_sets.p", "wb"))
        pickle.dump(open("../cached/backup_connected_sets.p", "wb"))

    
if __name__ == "__main__":
    a = DepthFirstSearch()
    # a.node_data = { 'A' : ['B'],
    #                 'B' : ['A', 'C'],
    #                 'C' : ['F','B'],
    #                 'D' : ['E'],
    #                 'E' : ['D', 'F'],
    #                 'F' : ['C', 'E']
    #                 }
    # a.nodes = ['A','B','C','D','E', 'F']
    a.import_pickled("../cached/connected_graph.p")
    a.find_all_connected()
    a.pickle_results()
    print a.connected_sets
