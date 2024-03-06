# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 18:59:41 2022

@author: alexf
"""
import copy 
import ville_to_graphe as vg

inf=float('inf')

map1="""1hhhhhhhhthhhhhhhh2
v99999999v99999999v
v9<>9<h>9u9<h>9<>9v
v99999999999999999v
v9<>9n9<hth>9n9<>9v
v9999v999v999v9999v
3hh29xh>9u9<hy91hh4
888v9v9999999v9v888
hhh49u91>9<29u93hhh
9999999v999v9999999
hhh29n93hhh49n91hhh
888v9v9999999v9v888
1hh49u9<hth>9u93hh2
v99999999v99999999v
v9<29<h>9u9<h>91>9v
v99v99999999999v99v
x>9u9n9<hth>9n9u9<y
v9999v999v999v9999v
v9<hhjh>9u9<hjhh>9v
v99999999999999999v
3hhhhhhhhhhhhhhhhh4"""

map1=map1.splitlines()

Dico=vg.dico(map1)
Dist,Direc=vg.adjacence_distance(map1),vg.adjacence_direction(map1)

def mat_adj_to_liste_adj(mat_G):
    #transforme une matrice d'adjacence en liste d'adjacence
    n=len(mat_G)
    res={i:[] for i in range(n)}
    for i in range(n):
        for j in range(n):
            d_ij=mat_G[i][j]
            if d_ij!= inf:
                res[i].append((j,d_ij))
    return res

#implémentation des piles

def depiler(p):
    return p.pop(0)

def empiler(p,x):
    p.append(x)


def plus_proche(a_visiter,distance):
    s_min, mini = a_visiter[0], inf
    for s in range(len(a_visiter)):
        d=distance[a_visiter[s]]
        if d<mini:
            mini=d
            s_min=a_visiter[s]
    return s_min

#dijsktra appliqué 
def plus_court_chemin(g,depart,arr):
    #g en mat d'ajdacence
    #retourne un plus court chemin (liste de sommets) et sa longueur
    n=len(g)
    distance=n*[inf]
    pere=n*[-1] #pour retrouver le chemin et pas juste la dist
    visite=n*[False]
    a_visiter=[depart] 
    pere[depart]=depart
    distance[depart]=0
    
    while a_visiter!=[]:
        s=plus_proche(a_visiter, distance)
        a_visiter.remove(s)
        visite[s]=True
        for v in range(n):
            new_dist=g[s][v]+distance[s]
            if new_dist < distance[v]:
                distance[v]=new_dist
                pere[v]=s
            if not visite[v] and (v not in a_visiter) and new_dist<inf:
                empiler(a_visiter,v)
    chemin=[arr]
    prochain=pere[arr]
    while prochain != depart:
        chemin.append(prochain)
        prochain=pere[prochain]
    chemin.append(depart)
    return distance[arr], list(reversed(chemin))
            
def plus_court_chemin_sans_direction(g, d_interdit, depart,arr):
    #g est la map
    adj=copy.deepcopy(Dist)
    if vg.voisin(g, depart, d_interdit) in Dico.keys():
        adj[depart][Dico[vg.voisin(g, depart, d_interdit)]]=inf
    return plus_court_chemin(adj, depart, arr)
    
    


    

    
  
