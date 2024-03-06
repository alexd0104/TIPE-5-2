# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 13:57:39 2022

@author: alexf
"""
import random

inf=float('inf')
def init_seed():
    seed = random.randint(0, 2**32 - 1)
    #seed = 2020253812
    random.seed(seed)
    print(seed)

init_seed()

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


inf=float('inf')

def dico(G):
    #G représentation de la carte
    #renvois un dictionnaire faisant correspondre les coordonnées des sommets avec leur numéro
    D={}
    p=0
    m = len(G[1])
    n = len(G)
    for i in range(n):
        for j in range(m):
            if G[i][j]=='9':
                D[(i,j)] = p
                p+=1
    return D

def valeur_to_clef(dico, valeur):
    #on suppose que la valeur a une clef qui est unique
    for clef in dico.keys():
        if dico[clef]==valeur:
            return clef

Dico=dico(map1)

def voisin (G, k, d):
    (i,j) = valeur_to_clef(Dico,k)
    if d == 1:
        return ((i-1)%len(G),j)
    if d == 2:
        return (i,(j+1)%len(G[1]))
    if d == 3:
        return ((i+1)%len(G),j)
    if d == 4:
        return (i,(j-1)%len(G[1]))

def voisin_coord (G, i, j , d):
    if d == 1:
        return ((i-1)%len(G),j)
    if d == 2:
        return (i,(j+1)%len(G[1]))
    if d == 3:
        return ((i+1)%len(G),j)
    if d == 4:
        return (i,(j-1)%len(G[1]))

def voisin_coord_diagonal (G,i,j,d):
    if d == 5:
        return voisin_coord(G,voisin_coord(G,i,j,1)[0],voisin_coord(G,i,j,1)[1],2)
    if d == 6:
        return voisin_coord(G,voisin_coord(G,i,j,2)[0],voisin_coord(G,i,j,2)[1],3)
    if d == 7:
        return voisin_coord(G,voisin_coord(G,i,j,3)[0],voisin_coord(G,i,j,3)[1],4)
    if d == 8:
        return voisin_coord(G,voisin_coord(G,i,j,4)[0],voisin_coord(G,i,j,4)[1],1)

def voisin_plus_loins(G, i, j ,d,n):
    res = (i,j)
    for k in range (n):
        (i,j)=res
        res = voisin_coord(G, i, j, d)
    return res

def voisin_approximatif(G,i,j):
    if G[i][j]=='9' :
        return (i,j)
    else :
        for d in range(1,5):
            (nvi,nvj)=voisin_coord(G,i,j,d)
            if G[nvi][nvj]=='9':
                return (nvi,nvj)
        for d in range(5,8):
            (nvi,nvj)=voisin_coord_diagonal(G,i,j,d)
            if G[nvi][nvj]=='9':
                return (nvi,nvj)
        for d in range(1,5):
            (nvi,nvj)=voisin_plus_loins(G,i,j,d,2)
            if G[nvi][nvj]=='9':
                return (nvi,nvj)
        print("wwshhhhh")
        print(i,j)
        
def adjacence_direction (G):
    #renvoie la matrice d'adjacence avec la direction à emprunter pour aller du sommet i au sommet j
    n=len(Dico)
    direction=[[-1 for j in range(n)] for i in range(n)]
    for k in range(n):
        (i,j) = valeur_to_clef(Dico,k)
        for d in range(1,5):
            if voisin(G, k, d) in Dico.keys() :
                direction[k][Dico[voisin(G, k, d)]]= d
    return direction

def adjacence_distance (G):
    #renvoie la matrice d'adjacence avec les distances (donc des 1) entre les sommets et inf sinon
    n=len(Dico)
    distance=[[inf for j in range(n)] for i in range(n)]
    for k in range(n):
        (i,j) = valeur_to_clef(Dico,k)
        for d in range(5):
            if voisin(G, k, d) in Dico.keys() :
                distance[k][Dico[voisin(G, k, d)]]= 1
    return distance

def dist_euclidienne (i,j,x,y):
    #renvoie la distance associée à la norme 2 entre les vecteur (i,j) et (x,y)
    return (((x-i)**2)+(y-j)**2)**0.5

def random_except(a,b,k):
    #renvoie un nombre aleatoire entre a et b privé de k
    n = random.randint(a,b)
    while n==k:
        n = random.randint(a,b)
    return n
    




