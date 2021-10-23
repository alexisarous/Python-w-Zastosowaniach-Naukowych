import argparse
from os import linesep
from ascii_graph import Pyasciigraph
import numpy as np

graph = Pyasciigraph()

parser = argparse.ArgumentParser(description="Opis")

parser.add_argument('file', help='name of file')
parser.add_argument('-n', '--number', help='number of words', type=int, default = 10)
parser.add_argument('-l', '--lenght', help='minimal lenght of word', type=int, default = 0)
parser.add_argument('-i', '--ignored', help='ignored words', type=str, default=[])
args = parser.parse_args()

print(args.ignored)

n = args.number  # parametr określający, dla ilu wyrazów wykreślić histogram
l = args.lenght  # minimalna długość histogramowanego słowa

lst = {}

with open(args.file, encoding = 'utf8') as f: # 'pan-tadeusz.txt' --> args.file

    for line in f:
        for word in line.split():
            if len(word) >= l:       
                if word in lst:
                    k = lst[word] + 1
                    lst[word] = k
                else:
                    lst[word] = 1

k = 0
data = []

for w in sorted(lst, key=lst.get, reverse=True):
    if (k < n):
        #print(w, lst[w])
        data.append ((w, lst[w]))
        k = k + 1


for line in graph.graph('Histogram', data):
    print(line)


    