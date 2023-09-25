#lexigraph 
import sys
import argparse
from collections import deque
arg = sys.argv
task = arg[1]
input_filename = arg[2]
#creates the graph from the text file
graph = dict()
with open(input_filename, "r") as file:
    for line in file:
        node1 , node2 = line.strip().split()
        node1 = int(node1)
        node2 =int(node2)
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append(node2)
        graph[node2].append(node1)

#lexigraph 
# create a class to represent a node: a node is always a set
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
# create a class to represent a doubly linked list
class DoublyLinkedList:
    def __init__(self):
        self.head = None
    def viewhead(self):
        return self.head
# append a node to a specific index
    def append(self, data, index):
        new_node = Node(data)
        if index == 0:
            if self.head:
                new_node.next = self.head
                self.head.prev = new_node
            self.head = new_node
        else:
            current = self.head
            current_index = 0
            while current and current_index < index - 1:
                current = current.next
                current_index += 1
            if current_index == index - 1:
                new_node.prev = current
                new_node.next = current.next

                if current.next:
                    current.next.prev = new_node
                current.next = new_node
            else:
                raise IndexError("Invalid index")
# print the result       
    def display(self,lex):
        current = self.head
        strlink = ""
        while current:
            strlink = strlink + str(current.data) + " "
            current = current.next
        strlex = str(lex).replace("[","(").replace("]",")")
        full = strlex + " " + "[" + strlink + "]"
        print(full)
# finds where a node is in the list and returns the index of its set
    def findnodeinset(self,nod):
        current = self.head
        index = -1
        while current:
            index = index +1
            if nod in current.data:
                return index
            current = current.next
        return None
# removes an empty set from the list
    def removeemptysets(self):
        current = self.head
        while current:
            if not current.data:
                break
            current= current.next
        if current is None:
            return
        if current.next:
            current.next.prev = current.prev
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        del current
    def is_empty(self):
        return self.head is None

    def selectnodefromset(self):
        setfirst = self.viewhead()
        setfirst = setfirst.data
        sortinglist = list(setfirst)
        sortinglist.sort()
        el = sortinglist[0]
        setfirst.remove(el)
        return el
# removes node from a set at a specidic index
    def removenodefromset(self,node,index):
        current = self.head
        current_index = 0
        while current and current_index < index:
            current = current.next
            current_index += 1
        if current_index == index:
            currentset = current.data
            currentset.remove(node)
            current.data = currentset
        else:
            raise IndexError("Invalid index")
# creates the new set with all the neightbours of u which are on the same set on the list
    def createsv2(self,neigh,index):
        current = self.head
        current_index = 0
        while current and current_index < index:
            current = current.next
            current_index += 1
        if current_index == index:
            currentset = current.data
            sv2 = currentset & neigh
            return sv2
        else:
            raise IndexError("Invalid index")
#returns set of neighours of node than we have not visited
def setofneightbours(node,graph,visited):
    neightbours= set(graph[node])
    neightbours = neightbours - visited
    return neightbours
def lexbfs(graph):
    #initialize dataset from graph as a set       
    node_set = set(graph.keys())
    #initialize the lexigraph sorting arraylist
    sortedlex = []
    #initialize visited set which is empty at first
    visited = set()
    # create list S(named node_que)that contains all the nodes of the graph
    node_que = DoublyLinkedList()
    node_que.append(node_set,0)

    # while list s is not empty 
    while not node_que.is_empty():
        u = node_que.selectnodefromset()
        sortedlex.append(u)
        node_que.removeemptysets()
        visited.add(u)
        neightbours = setofneightbours(u,graph,visited)
        sv2 = set()
        neightboursinsameset = set()
        for v in neightbours:
            if v not in neightboursinsameset:
                index = node_que.findnodeinset(v)
                sv2 = node_que.createsv2(neightbours,index)
                neightboursinsameset |= sv2
                for n in sv2:
                    node_que.removenodefromset(n,index)
                node_que.append(sv2,index)
                node_que.removeemptysets()
        #node_que.display(sortedlex)
    
    return sortedlex
#chordal
def chordal(graph,sortedlex):
    # find the neightbours of a node
    def neightbours(graph,node):
        neightbours= set(graph[node])
        return neightbours
    # find the neightbours that come after a node 
    def rn(nodeindex,revlex,neigh):
        start = nodeindex + 1
        sllist = revlex[start:]
        setoflistnodes = set(sllist)
        result = setoflistnodes & neigh
        return result
    #find the first neightbour of node in the revlex list,if it does exist
    def firstneightbour(nodeindex,revlex,neigh):
        start = nodeindex + 1
        sllist = revlex[start:]
        for node in sllist:
            if node in neigh:
                return node
        return None
    # determine if a graph is chordal
    def ischordal(Rn_u,v,set2):
        ss = set()
        ss.add(v)
        set1 = Rn_u - ss
        chordal = set1 <= set2
        return chordal

    revlex = list()
    revlex = sortedlex[::-1]
    # we innitialize as if the graph is chordal
    chordal = True
    for i in range(len(revlex)):
        u = revlex[i]
        neigh = neightbours(graph,u)
        v = firstneightbour(i,revlex,neigh)
        if v is not None:
            Rn_u = rn(i,revlex,neigh)
            indexv = revlex.index(v)
            neigh = neightbours(graph,v)
            Rn_v = rn(indexv,revlex,neigh)
            chordal = ischordal(Rn_u,v,Rn_v)
            if not chordal:
                break
    
    return chordal
def interval(graph,chordal):
    # interval
    def graphforcomponent(graph, node): 
        graph2 = dict()  
        for key,values in graph.items():
            graph2[key] = values
        neigh = set(graph2[node])
        graph2.pop(node)
        for n in neigh:
            graph2.pop(n)
        for node,nei in graph2.items():
            setofgraph = set(nei)
            setofremove = set(neigh)
            listofremaining = list(setofgraph-setofremove)
            listofremaining.sort()
            graph2[node] = listofremaining
        return graph2

    def hol(new):
        visited = set()
        component_list = []
        for node in new:
            if node not in visited:
                component = bfs(new, node)
                visited.update(component)
                component_list.append(component)
        component_list.sort()
        return component_list
    def bfs(graph, start_node):
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)

        while queue:
            node = queue.popleft()

            neighbors = graph.get(node, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        return visited
    #find node in set and return index of set
    def findnodeinset(node,componentvalues):
        s =set()
        for i in range(len(componentvalues)):
            s = componentvalues[i]
            if node in s:
                return i+1
        return 0
    # name the components as first digit the node they belong and second the position of the set they belong +1 
    def creatematrix(components):

        size = len(components)
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                com = findnodeinset(j,components[i])
                if com == 0:
                    row.append(com)
                else:
                    st = str(i)
                    st = st + str(com)
                    row.append(st)
            matrix.append(row)
        return matrix


    def validposition(matrix, row, col):
        size = len(matrix)
        valid = 0 <= row < size and 0 <= col < size
        if matrix[row][col] == 0:
            valid = False
        return valid
            

    def hasasteroidtriplets(matrix,components):
        size = len(matrix)
        nonneightbourslist = list()
        for i in range(size):
            for j in range(size):
                element = matrix[i][j]
                if element == 0:
                    continue
                if isinstance(element,str):
                    u = int(element[0])
                    position = int(element[1]) -1
                    componentvalues = components[u]
                    nonneightbourslist = list(componentvalues[position])
                    for z in range(len(nonneightbourslist)):
                        if z+1 <=  len(nonneightbourslist)-1:
                            v = nonneightbourslist[z]
                            w = nonneightbourslist[z+1]
                            triplet = (matrix[u][v] == matrix[u][w] and matrix[v][u] == matrix[v][w] and matrix[w][u] == matrix[w][v])
                            if triplet:
                                return True

        return False

    #find components and make a dictionary with u as a key and its components as values
    components = dict()
    componentelements = list()
    for node in graph:
        new = graphforcomponent(graph, node)
        componentelements = hol(new)
        components[node] = componentelements
    #create matrix C
    matrix = creatematrix(components)
    # determine if it has astreroid triplets
    hastriplets = hasasteroidtriplets(matrix,components)
    print(not hastriplets and chordal)
# run
if task == "lexbfs":
    sortedlex = lexbfs(graph)
    print(sortedlex)
elif task == "chordal":
    sortedlex = lexbfs(graph)
    c = chordal(graph,sortedlex)
    print(c)
elif task =="interval":
    sortedlex = lexbfs(graph)
    c = chordal(graph,sortedlex)
    interval(graph,c)
else:
    print("task not given or incorect")
