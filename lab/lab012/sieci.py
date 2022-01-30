from turtle import left
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np
from rich.progress import track

G = nx.Graph()

N = 2277 # liczba wierzchołków
E = 31421 # liczba krawędzi

G.add_node(N)



l=0
r=0
left = True
                    # KRAWĘDZIE
with open('musae_chameleon_edges.csv', 'r') as edges:

    edges = csv.reader(edges, delimiter=',')  
    for line in edges:
        for word in line:
            if left:
                l = int(word) + 1
                left = False
            else:
                r = int(word) + 1
                left = True

        G.add_edge(l, r)




############ rozkład stopni wierzchołków ##############
degrees = list(G.degree)
degrees.sort(key = lambda x: x[1])

x=[]
y=[]
y_all=[]
sum = 0
prev = 0
i = 1
for line in degrees:
    a, b = line

    if (b == prev):
        for p in range(i):
            y_all.pop()
        for p in range(i):
            y_all.append(i+1)
        i = i + 1
    else:
        i = 1

    y_all.append(i)
    x.append(b)
    sum = sum + b
    prev = b

for i in y_all:                 # zamiana na %
    y.append(i*i*100/sum)

plt.plot(x, y)
plt.xlabel("k")
plt.ylabel("P(k) [%]")
plt.title("Rozkład stopni wierzchołków")
plt.savefig('rozklad_stopni_wierzcholkow.png')

print (f'1 spójna składowa o liczbie węzłów: {N} oraz krawędzi: {E}')


##################### shortest path ###############################

av = 0
nn = 1
max_path = 1

for i in track(range(N)):
    for n in range(N-nn+1):
        n = n+1
        spl = nx.shortest_path_length(G, n, nn)
        av = av + spl

        if max_path < spl:
            max_path = spl

    nn = nn + 1

av = av / (N*N)
print(f'Średnia najkrótsza ścieżka: {av}')

print(f'Najdłuższa najkrótsza ścieżka: {max_path}')

####################################################################
plt.close()

fig = plt.figure(1, figsize=(200, 80), dpi=60)
nx.draw(G, with_labels=True, font_weight='normal')
plt.savefig('graph.png')

