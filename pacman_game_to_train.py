# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:50:14 2024

@author: alexf
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 22:56:47 2022

@author: alexf
"""
import time
import pygame
import ville_to_graphe as vg
import fonctions_de_graphes_TIPE as fg
import copy
import random
pygame.init()


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

Coord = {0:[(15,9),1], 1:[(7,9),1], 2:[(9,9),1], 3:[(9,8),1],4:[(9,10),1]}
#coordonnées, direction
#pac man, rouge, rose, bleu, jaune

def beau(D):
    fg.afficher_mieux_mat(D)

def g(x):
    if x==1 or x==2:
        return 0
    if x==3 or x==4:
        return 1

def opposite (x):
    if x == 1:
        return 3
    if x == 2:
        return 4 
    if x == 3 :
        return 1 
    if x == 4 :
        return 2


Dico=vg.dico(map1)
Dist,Direc=vg.adjacence_distance(map1),vg.adjacence_direction(map1)

def modif_map(G,M,D,k,i,j):
    M2=copy.deepcopy(M)
    D2=copy.deepcopy(D)
    M2[Dico.get((i,j))][Dico.get((vg.prochain_sommet(G,i,j,k)))]= inf
    D2[Dico.get((i,j))][Dico.get((vg.prochain_sommet(G,i,j,k)))]= 0
    return M2,D2


def bouger_perso(i,j,f):
    if f==1:
        return i-1,j
    elif f==2:
        return i,j+1
    elif f==3:
        return i+1,j
    else:
        return i,j-1

def bouger_pac_man(i,j,f): 
    return bouger_perso(i,j,f)

def bouger_fantome_bleu(i,j,f):
    return bouger_perso(i,j,f)

def bouger_fantome_rouge(i,j,f): 
    return bouger_perso(i,j,f)

def bouger_fantome_rose(i,j,f):
    return bouger_perso(i,j,f)

def bouger_fantome_jaune(i,j,f):
    return bouger_perso(i,j,f)

def aleatoire (n, m):
    #renvoie un nombre aleatoire entre 0 et n privé de m
    k=random.randint(0,n)
    while k !=m:
        k=random.randint(0,n)
    return k 

def chemin_pacman (G,k,Coord) :
    #k est le sommet final
    kpm=Dico[Coord[0][0]]
    chemin_pm = fg.plus_court_chemin(Dist,kpm,k)
    chemin=[]
    for i in range(len(chemin_pm[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_pm[1][i]))
    return chemin

def chemin_fantome_rouge_chase (G,Coord):
    kfrouge=Dico[Coord[1][0]]
    chemin_frouge = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[1][1]),kfrouge,Dico[Coord[0][0]])
    chemin=[]
    for i in range(len(chemin_frouge[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_frouge[1][i]))
    return chemin
    
def chemin_fantome_rose_chase (G,Coord):
    kfrose=Coord[2][0]
    kpm=Coord[0][0]
    (ipm,jpm)=kpm
    d=Coord[0][1]
    k = vg.voisin_plus_loins(G, ipm, jpm, d, 4)
    (i,j)=k
    cible = vg.voisin_approximatif(G, i,j )
    cible = Dico[cible]
    chemin_frose = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[2][1]),Dico[kfrose],cible)
    chemin=[]
    for i in range(len(chemin_frose[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_frose[1][i]))
    return chemin
    
def chemin_fantome_bleu_chase (G,Coord):
    kfrouge=Dico[Coord[1][0]]
    (ir,jr)=vg.valeur_to_clef(Dico, kfrouge)
    kfbleu=Dico[Coord[3][0]]
    kpm=Coord[0][0]
    d=Coord[0][1]
    k= vg.voisin_plus_loins(G, kpm[0],kpm[1], d, 2)
    (i,j)=k
    cible = vg.voisin_approximatif(G, i,j )
    [ik,jk]=cible
    cible = [ik,jk]
    x = jr - jk
    if x > 0 :
        cible[0] = vg.voisin_approximatif(G,vg.voisin_plus_loins(G, cible[0],cible[1], 4, abs(x))[0],vg.voisin_plus_loins(G, cible[0],cible[1], 4, abs(x))[1])[0]
    elif x < 0 :
        cible[0] = vg.voisin_approximatif(G,vg.voisin_plus_loins(G, cible[0],cible[1], 2, abs(x))[0],vg.voisin_plus_loins(G, cible[0],cible[1], 2, abs(x))[1])[0]
    y = ir - ik
    if y > 0 :
        cible[1] = vg.voisin_approximatif(G,vg.voisin_plus_loins(G, cible[0],cible[1], 3, abs(y))[0],vg.voisin_plus_loins(G, cible[0],cible[1], 3, abs(y))[1])[1]
    elif y < 0 :
        cible[1] = vg.voisin_approximatif(G,vg.voisin_plus_loins(G, cible[0],cible[1], 1, abs(y))[0],vg.voisin_plus_loins(G, cible[0],cible[1], 1, abs(y))[1])[1]
    cible = vg.voisin_approximatif(G,cible[0],cible[1])
    chemin_fbleu = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[3][1]),kfbleu,Dico[cible])
    chemin=[]
    for i in range(len(chemin_fbleu[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_fbleu[1][i]))
    return chemin

def chemin_fantome_jaune_chase (G,Coord):
    kfjaune=Dico[Coord[4][0]]
    (ij,jj) = vg.valeur_to_clef(Dico, kfjaune)
    kpm=Dico[Coord[0][0]]
    (ik,jk) = vg.valeur_to_clef(Dico, kpm)
    if vg.dist_euclidienne (ij,ij,ik,jk) > 8 :
        chemin_fjaune = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[4][1]),kfjaune,Dico[Coord[0][0]])
        chemin=[]
        for i in range(len(chemin_fjaune[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_fjaune[1][i]))
        return chemin
    else : 
        return chemin_fantome_jaune_scatter (G,Coord)

def chemin_fantome_rose_scatter (G,Coord):
    kfrose=Dico[Coord[2][0]]
    if kfrose != 0 :
        chemin_frose = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[2][1]),kfrose,0)
        chemin=[]
        for i in range(len(chemin_frose[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_frose[1][i]))
        return chemin
    else :
        chemin_frose = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[2][1]),kfrose,25)
        chemin=[]
        for i in range(len(chemin_frose[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_frose[1][i]))
        return chemin

def chemin_fantome_rouge_scatter (G,Coord):
    kfrouge=Dico[Coord[1][0]]
    if kfrouge != 15 :
        chemin_frouge = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[1][1]),kfrouge,15)
        chemin=[]
        for i in range(len(chemin_frouge[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_frouge[1][i]))
        return chemin
    else :
        chemin_frouge = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[1][1]),kfrouge,35)
        chemin=[]
        for i in range(len(chemin_frouge[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_frouge[1][i]))
        return chemin

def chemin_fantome_jaune_scatter (G,Coord):
    kfjaune=Dico[Coord[4][0]]
    if kfjaune != 172 :
        chemin_fjaune = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[4][1]),kfjaune,172)
        chemin=[]
        for i in range(len(chemin_fjaune[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_fjaune[1][i]))
        return chemin
    else :
        chemin_fjaune = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[4][1]),kfjaune,157)
        chemin=[]
        for i in range(len(chemin_fjaune[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_fjaune[1][i]))
        return chemin

def chemin_fantome_bleu_scatter (G,Coord):
    kfbleu=Dico[Coord[3][0]]
    if kfbleu != 188 :
        chemin_fbleu = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[3][1]),kfbleu,188)
        chemin=[]
        for i in range(len(chemin_fbleu[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_fbleu[1][i]))
        return chemin
    else :
        chemin_fbleu = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[3][1]),kfbleu,165)
        chemin=[]
        for i in range(len(chemin_fbleu[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_fbleu[1][i]))
        return chemin

def state (n):
    if n < 8 :
        return 0
    if n < 28:
        return 1
    if n < 35:
        return 0
    if n < 45:
        return 1
    if n < 50:
        return 0
    if n < 70:
        return 1
    if n < 75 :
        return 0
    else :
        return 1
#0 : scatter
#1 : chase

def pac_man_catch(Coord):
    res = False
    for k in range(1, 5):
        if Coord[0][0]==Coord[k][0]:
            res = True
    return res

def play():
    Coord = {0:[(15,9),1], 1:[(7,9),1], 2:[(9,9),1], 3:[(9,8),1],4:[(9,10),1]}
    tour = 0            
    while not (pac_man_catch(Coord)):
        tour+=1 
        n= vg.random_except(0,188,Dico[Coord[0][0]])
        chemin_pm = chemin_pacman(map1, n, Coord)
        d= Direc[Dico[Coord[0][0]]][Dico[chemin_pm[1]]]
        bouger_pac_man(Coord[0][0][0], Coord[0][0][1], d)
        Coord[0][0]=chemin_pm[1]
        Coord[0][1]=d
        
        if state(tour)==0:
            
            chemin_frouge=chemin_fantome_rouge_scatter(map1,Coord)
            d= Direc[Dico[Coord[1][0]]][Dico[chemin_frouge[1]]]
            bouger_fantome_rouge(Coord[1][0][0], Coord[1][0][1], d)
            Coord[1][0]=chemin_frouge[1]
            Coord[1][1]=d
                    
            chemin_frose=chemin_fantome_rose_scatter(map1,Coord)
            d= Direc[Dico[Coord[2][0]]][Dico[chemin_frose[1]]]
            bouger_fantome_rose(Coord[2][0][0], Coord[2][0][1], d)
            Coord[2][0]=chemin_frose[1]
            Coord[2][1]=d
                    
            chemin_fbleu=chemin_fantome_bleu_scatter(map1,Coord)
            d= Direc[Dico[Coord[3][0]]][Dico[chemin_fbleu[1]]]
            bouger_fantome_bleu(Coord[3][0][0], Coord[3][0][1], d)
            Coord[3][0]=chemin_fbleu[1]
            Coord[3][1]=d
                    
            chemin_fjaune=chemin_fantome_jaune_scatter(map1,Coord)
            d= Direc[Dico[Coord[4][0]]][Dico[chemin_fjaune[1]]]
            bouger_fantome_jaune(Coord[4][0][0], Coord[4][0][1], d)
            Coord[4][0]=chemin_fjaune[1]
            Coord[4][1]=d
                    
        else :
            
            chemin_frouge=chemin_fantome_rouge_chase(map1,Coord)
            d= Direc[Dico[Coord[1][0]]][Dico[chemin_frouge[1]]]
            bouger_fantome_rouge(Coord[1][0][0], Coord[1][0][1], d)
            Coord[1][0]=chemin_frouge[1]
            Coord[1][1]=d
            
            chemin_frose=chemin_fantome_rose_chase(map1,Coord)
            d= Direc[Dico[Coord[2][0]]][Dico[chemin_frose[1]]]
            bouger_fantome_rose(Coord[2][0][0], Coord[2][0][1], d)
            Coord[2][0]=chemin_frose[1]
            Coord[2][1]=d
            
            chemin_fbleu=chemin_fantome_bleu_chase(map1,Coord)
            d= Direc[Dico[Coord[3][0]]][Dico[chemin_fbleu[1]]]
            bouger_fantome_bleu(Coord[3][0][0], Coord[3][0][1], d)
            Coord[3][0]=chemin_fbleu[1]
            Coord[3][1]=d
                
            chemin_fjaune=chemin_fantome_jaune_chase(map1,Coord)
            d= Direc[Dico[Coord[4][0]]][Dico[chemin_fjaune[1]]]
            bouger_fantome_jaune(Coord[4][0][0], Coord[4][0][1], d)
            Coord[4][0]=chemin_fjaune[1]
            Coord[4][1]=d
                    
    return tour        


def temps_moyen_par_partie(n):
    t=0
    tours=0
    for game in range(n):
        t0=time.time()
        tours+=play()
        t1=time.time()
        t+=(t1-t0)
        print(t)
    return t/n, tours/n


        



