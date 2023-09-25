from collections import deque
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
parser.add_argument('strings', nargs='*', help='List of strings.')
parser.add_argument('filename', help='Name of the file.')
args = parser.parse_args()
verbose_mode = args.verbose
patterns  = args.strings
input_filename = args.filename

with open(input_filename, 'r') as file:
    for line in file:
        text = line.strip()


def reverse_string(string):
    reversed_string = ""
    for i in range(len(string) - 1, -1, -1):
        reversed_string += string[i]
    return reversed_string

def reverse_patterns(patterns) :
    reversed = list()
    for pattern in patterns:
        reversed.append(reverse_string(pattern))
    return reversed

class Node:
    def __init__(self, char):
        self.char = char #character or l
        self.prev = None #previous character or root 
        self.next = None #next character/characters or None if it terminal
        self.level = 0 #dephf d()
        self.is_word_end = False #marks the node as terminal
        self.children = {} # a dict with the nodes as keys and their children as values
        self.failure = None # contains the node whitch this node refers in the failure table
        self.number = None # the number of the nodes determid by the dfs traversal to demostrate the same results
class PrefixTree:
    def __init__(self):
        self.root = Node("0") 
        self.patterns = None # the patterns that made the trie
        self.paths = None # contains each path tha represent a word in the trie, every path is made of nodes
        self.failure = {} 
        self.set1 = {}
        self.set2 = {}
        self.s1 = {}
        self.s2 = {}
        self.pmin = None
    
    def constructtrie(self,patterns):
        number = 0
        self.patterns = patterns
        for pattern in patterns:
            current = self.root
            current.number = number
            prev = current
            for char in pattern:
                if char not in current.children:
                    number = number + 1
                    new = Node(char)
                    new.level = prev.level +1
                    new.number = number
                    if new.level <= 1:
                        new.failure = 0
                    new.prev = prev
                    if prev :
                        prev.next = new
                    current.children[char] = new
                prev = current.children[char]
                current = current.children[char]
            current.is_word_end = True
    def findmin(self,patterns):
        m = len(patterns[0])
        for p in patterns:
            if len(p) < m:
                m = len(p)
        self.pmin = m

    def find_paths(self):
        self.paths = []

        def dfs(node, path):
            if node is None:
                return

            if node.is_word_end:
                self.paths.append(path)

            for child in node.children.values():
                dfs(child, path + [child])

        dfs(self.root, [])

    def HasChild(self,u,t):
        if not u.is_word_end:
            for child in u.children.values():
                if child.char == t :
                    return True
        return False
    def GetChild(self,u,t):
        if not u.is_word_end:
            for child in u.children.values():
                if child.char == t :
                    return child
        return None
    # construct rt table bug?
    def creatert(self,text,patterns):
        rt = {}
        appering = set()
        everychar = set()
        
        for pattern in self.patterns:
            for c in pattern:
                if c not in appering:
                    appering.add(c)
        for t in text:
            if t not in everychar:
                everychar.add(t)
        disapearing = everychar - appering
        for c in disapearing:
            rt[c] = m 
        max = len(appering |  everychar)
        for pattern in patterns:
            for c in pattern:
                rt[c] = -1
        temp = {}

        for pattern in patterns:
            
            m = len(pattern)
            for i in range(0,m-1):
                temp[pattern[i]] = m - i - 1
            for i in range(0,m-1):
                if temp[pattern[i]] > rt[pattern[i]]:
                    rt[pattern[i]] = temp[pattern[i]] -1

        return rt   
#display the trie structure
    # def display_trie(self,node, indent=''):
    #     if node is None:
    #         return
    #     print(indent + '- ' + str(node))
    #     for child in node.children.values():
    #         self.display_trie(child, indent + '  |')
    def initfailure(self):
        queue = deque()
        visited = {}
        inqueue = {}
        for path in self.paths:
            for node in path:
                visited[node] = False
                inqueue[node] = False
        current = self.root
        queue.append(current)
        inqueue[current] = True
        while queue:
            c = queue.popleft()
            inqueue[c] = False
            visited[c] = True
            if c.level <= 1:
                self.failure[c] = c.failure
            for child in c.children.values():
                if not visited[child] and not inqueue[child]:
                    queue.append(child)
                    inqueue[child] = True
    def Createfailure(self):
        queue = deque()
        visited = {}
        inqueue = {}
        for path in self.paths:
            for node in path:
                visited[node] = False
                inqueue[node] = False
        current = self.root
        queue.append(current)
        inqueue[current] = True
        while queue:
            u = queue.popleft()
            inqueue[u] = False
            visited[u] = True
            #if u.level >= 1:
            for char,child in u.children.items():
                if not visited[child] and not inqueue[child]:
                    queue.append(child)
                    inqueue[child] = True
                    if u is self.root:
                        child.failure = self.root
                    else:
                        u1 = u.failure
                        while u1 and char not in u1.children:
                            u1 = u1.failure
                        if u1:
                            child.failure = u1.children[char] 
                        else:
                            child.failure = self.root
                    #self.failure[child] = child.failure
    def make_failure_table(self):
        for path in self.paths:
            for node in path:
                self.failure[node] = node.failure
                
    def make_set1(self):
        def getkey(d,value):
            for key,val in d.items():
                if value is val:
                    return key
            return None

        for key,value1 in self.failure.items():
            flag = False  
            setofnodes = set()
            for value in self.failure.values():
                if key == value:
                    flag = True
                    setofnodes.add(getkey(self.failure, value))
            if flag:
                self.set1[key] =setofnodes
                
        
    def make_set2(self):
        for key,value in self.set1.items():
            setofnodes = set()
            for v in value:
                if v.is_word_end:
                    setofnodes.add(v)
            if setofnodes:
                self.set2[key] = setofnodes


    def dfs_traversal(self, node):
        if node is None:
            return
        if node is self.root:
            self.s1[node] = 1
            self.s2[node] = self.pmin

        else:
            if node in self.set1:
                setofnodes = set()
                for s in self.set1[node]:
                    setofnodes.add(abs(node.level - s.level)) 
                setofnodes.add(self.pmin)
                self.s1[node] = min(setofnodes)
            else:
                self.s1[node] = self.pmin 
            if node in self.set2:
                setofnodes = set()
                for s in self.set2[node]:
                    setofnodes.add(abs(node.level - s.level)) 
                if node.prev in self.s2:
                    setofnodes.add(self.s2[node.prev])
                self.s2[node] = min(setofnodes)
            else:
                self.s2[node] = self.s2[node.prev]
        for child_node in node.children.values():
            self.dfs_traversal(child_node)
    def make_s1(self):

        self.dfs_traversal(self.root)
#construct trie stucture
def construct_trie():
    trie = PrefixTree()
    trie.findmin(patterns)
    trie.constructtrie(reverse_patterns(patterns))
    trie.find_paths()
    rt = {}
    rt = trie.creatert(text,patterns)
    trie.Createfailure()
    trie.make_failure_table()
    trie.make_set1()
    trie.make_set2()
    trie.make_s1()
    return  trie,rt

def CommentzWalter(verbose_mode):
    trie , rt = construct_trie()
    res = deque() #contains search pattern and the indices of whitch it is found in the test
    i = trie.pmin - 1 #text variable
    j = 0 #trie variable
    u = trie.root #trie node variable
    m =  ''#current match
    while i < len(text) :
        while trie.HasChild(u,text[i-j]):
            u = trie.GetChild(u,text[i-j])
            m = m + text[i-j] 
            j = j + 1
            if u.is_word_end:
                res.append((reverse_string(m),i - j + 1))
        if j > i :
            j = i
        s = min(trie.s2[u],max(trie.s1[u],rt[text[i-j]] - j -1 ))
        i = i +s
        j = 0
        u = trie.root
        m = ''
    if verbose_mode:
        for key1,value1 in sorted(trie.s1.items(), key = lambda item: item[0].number):
            for key2,value2 in sorted(trie.s2.items(), key = lambda item: item[0].number):
                if key1 is key2:
                    print(f"{key1.number} : {value1} , {value2}")

    return res

res = deque()
res = CommentzWalter(verbose_mode)
for item1,item2 in res:
    print(item1,item2)