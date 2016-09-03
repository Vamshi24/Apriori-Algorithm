from math import *
import sys
import itertools
import sets
import fileinput
from sets import Set

class Trie:

    def __init__(self,val="root",count=1):
        	self.val = val
        	self.count = count
        	self.nodes = {}

    def insert(self, item, count):
		node = self.nodes
		for i in item:
			if i  not in node:
				temp = Trie(i, count)
				node[i] = temp
			else:
				node = node[i].nodes

    def insert_total(self, dict2, count):
		l = len(dict2)
		for i in range(0,l):
			self.insert(dict2[i], count[i])
				
    def search(self, item):
		node = self.nodes
		for i in item:
			if i not in node:
				return False
			else:
				node = node[i].nodes
		
		return True

    def get_items(self, dict3):
		for i in self.nodes:
			a = dict3 + [i]
			yield a
			for j in self.nodes[i].get_items(a):
				yield j

    def getCount(self, dict3):
		node = self.nodes
		for i in dict3:
			node1 = node[i]
			node = node[i].nodes
		return node1.count

    def print_total(self, k):
		for i in self.nodes:
			a = k + i
			print a
			self.nodes[i].print_total(a + ",")

dict1 = {}
f = open("config.csv")
for row in f:
	a = row.strip().split(",")
	dict1[a[0]] = a[1]

sys.stdout = open(dict1["output"], 'w')

dict2 = {}
f = open(dict1["input"])
count_total = 0
for row in f:
	row = row.strip().split(",")
	for i in row:
		if i in dict2:
			dict2[i] = dict2[i] + 1
		else:
			dict2[i] = 1
	count_total = count_total + 1

dict3 = []
dict3count = []
print "Vamshi"

for i in dict2:
	minrows = ceil(count_total * float(dict1["support"]))
	if dict2[i] >= minrows:
		a = [i]
		print i
		dict3.append(a)
		dict3count.append(dict2[i])

tree = Trie()
tree.insert_total(dict3, dict3count)
dict3.sort()
current = dict3
l = len(current)

def generate(dict3):
    i = 0
    j = 1
    dict4 = []
    l = len(dict3)
    while i < l:
        j = i + 1
        while j < l:
            temp = []
            if dict3[i][:-1] == dict3[j][:-1]:
                temp = dict3[i][:]
                temp.append(dict3[j][-1])
                dict4.append(temp)
                j += 1
            else:
                break
        i += 1
    return dict4

def subsets(a):
    x = []
    l = len(a)
    for i in range(0,l):
        c = a[:i] + a[i+1:]
        x.append(c)
    #print x
    return x

def prune(f,dict3):
    g = []
    for i in dict3:
        sub= subsets(i)
        flag = True
        for j in sub:
            if not f.search(j):
                flag = False
                break
        if flag:
            g.append(i)
    return g

def set_count(f,dict3):
    cnt = []
    l = len(dict3)
    f = open(f)
    for i in range(0,l):
        cnt.append(0)
    for row in f:
        row1 = row.strip().split(",")
        current = Set(row1)
        for i in range(0,l):
            a = dict3[i][:]
            row2 = Set(a)
            if current.issuperset(row2):
                cnt[i] += 1
    return cnt

def Associate(f,cou):
    cnt = 0
    for i in f.get_items([]):
        for j in range(1,len(i)):
            for k in itertools.combinations(i, j):
                y = float(f.getCount(i)) / float(f.getCount(k))
                if y >= cou :
                    print (',').join(k) + "=>" + (',').join(set(i) - set(k))
                    cnt += 1
    return cnt

while True:
	dict4 = generate(current)
	pruned = prune(tree, dict4)
	l1 = len(pruned)
	if l1 == 0:
		break;
	cnts = set_count(dict1["input"], pruned)
	items = []
	itemcounts = []
	for i in range(l1):
		if cnts[i] >= minrows:
			print (",").join(pruned[i])
			items.append(pruned[i])
			itemcounts.append(cnts[i])
	l2 = len(itemcounts)
	if l2 == 0:
		break;
	tree.insert_total(items, itemcounts)
	current = items
	l += len(current)

if int(dict1["flag"]) == 1:
	print "Sai"
	x = float(dict1["confidence"])
	Rules = Associate(tree, x)

sys.stdout.close()

for line in fileinput.input(dict1["output"],inplace=1):
    if "Sai" in line and int(dict1["flag"]) == 1:
		line=line.replace(line,str(Rules) + "\n")
    elif "Vamshi" in line:
    	line=line.replace(line,str(l) + "\n")
    print line,
