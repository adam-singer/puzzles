import sys
import os
import re
import bktree
import cPickle
import bktree
import random
arch = os.uname()[4]
sys.path.append(arch + '/lib/python2.5/site-packages')
import editdist

words = []
for word in file(sys.argv[1]):
    word = word.strip().lower()
    words.append(word)

random.seed()
random.shuffle(words)
tree = bktree.BKtree(iter(words),editdist.distance)
output = open('fbdictionary.dat', 'wb')
cPickle.dump(tree, output, -1)
output.close()
