# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:12:58 2024

@author: alexf
"""

import time
import pygame
import city_to_graph as vg
import graph_function as fg
import copy
import random
from PIL import Image, ImageSequence
import matplotlib.pyplot as plt
from IPython.display import display # pour afficher dans le notebook
import numpy as np

inf=float('inf')

surface=pygame.display.set_mode((570,650),pygame.HWSURFACE| pygame.DOUBLEBUF)

fantome_rose=pygame.image.load("fantome_rose.png")
fantome_rose=pygame.transform.scale(fantome_rose,(30,30))

fantome_bleu=pygame.image.load("fantome_bleu.png")
fantome_bleu=pygame.transform.scale(fantome_bleu,(30,30))

fantome_rouge=pygame.image.load("fantome_rouge.png")
fantome_rouge=pygame.transform.scale(fantome_rouge,(30,30))

fantome_jaune=pygame.image.load("fantome_jaune.png")
fantome_jaune=pygame.transform.scale(fantome_jaune,(30,30))

pac_man=pygame.image.load("pac_man.png")
pac_man=pygame.transform.scale(pac_man,(30,30))

brique_noire=pygame.image.load("brique_noire.png")
brique_noire=pygame.transform.scale(brique_noire,(30,30))

mur_horizontale=pygame.image.load("mur_horizontale.png")
mur_horizontale=pygame.transform.scale(mur_horizontale,(30,30))

mur_verticale=pygame.image.load("mur_verticale.png")
mur_verticale=pygame.transform.scale(mur_verticale,(30,30))

mur_tournant_1=pygame.image.load("mur_tournant_1.png")
mur_tournant_1=pygame.transform.scale(mur_tournant_1,(30,30))

mur_tournant_2=pygame.image.load("mur_tournant_2.png")
mur_tournant_2=pygame.transform.scale(mur_tournant_2,(30,30))

mur_tournant_3=pygame.image.load("mur_tournant_3.png")
mur_tournant_3=pygame.transform.scale(mur_tournant_3,(30,30))

mur_tournant_4=pygame.image.load("mur_tournant_4.png")
mur_tournant_4=pygame.transform.scale(mur_tournant_4,(30,30))

mur_t1=pygame.image.load("mur_t1.png")
mur_t1=pygame.transform.scale(mur_t1,(30,30))

mur_t2=pygame.image.load("mur_t2.png")
mur_t2=pygame.transform.scale(mur_t2,(30,30))

mur_t3=pygame.image.load("mur_t3.png")
mur_t3=pygame.transform.scale(mur_t3,(30,30))

mur_t4=pygame.image.load("mur_t4.png")
mur_t4=pygame.transform.scale(mur_t4,(30,30))

fin_horizontale_gauche=pygame.image.load("fin_horizontale_gauche.png")
fin_horizontale_gauche=pygame.transform.scale(fin_horizontale_gauche,(30,30))

fin_horizontale_droite=pygame.image.load("fin_horizontale_droite.png")
fin_horizontale_droite=pygame.transform.scale(fin_horizontale_droite,(30,30))

fin_verticale_haut=pygame.image.load("fin_verticale_haut.png")
fin_verticale_haut=pygame.transform.scale(fin_verticale_haut,(30,30))

fin_verticale_bas=pygame.image.load("fin_verticale_bas.png")
fin_verticale_bas=pygame.transform.scale(fin_verticale_bas,(30,30))


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

def creation_map(map1):
    for y, line in enumerate(map1):
        for x, c in enumerate(line):
            coord=(x*30,y*30)
            if c=="9":
                surface.blit(brique_noire,coord)
            elif c=="8":
                surface.blit(brique_noire,coord)
            elif c=="1":
                surface.blit(mur_tournant_1,coord)
            elif c=="2":
                surface.blit(mur_tournant_2,coord)
            elif c=="3":
                surface.blit(mur_tournant_3,coord)
            elif c=="4":
                surface.blit(mur_tournant_4,coord)
            elif c=="h":
                surface.blit(mur_horizontale,coord)
            elif c=="v":
                surface.blit(mur_verticale,coord)
            elif c=="t":
                surface.blit(mur_t1,coord)
            elif c=="x":
                surface.blit(mur_t4,coord)
            elif c=="y":
                surface.blit(mur_t2,coord)
            elif c=="j":
                surface.blit(mur_t3,coord)
            elif c=="<":
                surface.blit(fin_horizontale_gauche,coord)
            elif c==">":
                surface.blit(fin_horizontale_droite,coord)
            elif c=="u":
                surface.blit(fin_verticale_bas,coord)
            elif c=="n":
                surface.blit(fin_verticale_haut,coord)

Dico=vg.dico(map1)
Dist,Direc=vg.adjacence_distance(map1),vg.adjacence_direction(map1)


def modif_map(G,M,D,k,i,j):
    M2=copy.deepcopy(M)
    D2=copy.deepcopy(D)
    M2[Dico.get((i,j))][Dico.get((vg.prochain_sommet(G,i,j,k)))]= inf
    D2[Dico.get((i,j))][Dico.get((vg.prochain_sommet(G,i,j,k)))]= 0
    return M2,D2

def bouger_pac_man(i,j,f):
    coord=(j*30,i*30)
    surface.blit(brique_noire,coord)
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(pac_man,new_coord)
        return i-0.5,j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(pac_man,new_coord)
        return i,j+0.5
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(pac_man,new_coord)
        return i+0.5,j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(pac_man,new_coord)
        return i,j-0.5

def bouger_fantome_bleu(i,j,f):
    coord=(j*30,i*30)
    surface.blit(brique_noire,coord)
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_bleu,new_coord)
        return i-0.5,j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_bleu,new_coord)
        return i,j+0.5
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_bleu,new_coord)
        return i+0.5,j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_bleu,new_coord)
        return i,j-0.5

def bouger_fantome_rouge(i,j,f):
    coord=(j*30,i*30)
    surface.blit(brique_noire,coord)
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_rouge,new_coord)
        return i-0.5,j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_rouge,new_coord)
        return i,j+0.5
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_rouge,new_coord)
        return i+0.5,j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_rouge,new_coord)
        return i,j-0.5

def bouger_fantome_rose(i,j,f):
    coord=(j*30,i*30)
    surface.blit(brique_noire,coord)
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_rose,new_coord)
        return i-0.5,j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_rose,new_coord)
        return i,j+0.5
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_rose,new_coord)
        return i+0.5,j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_rose,new_coord)
        return i,j-0.5

def bouger_fantome_jaune(i,j,f):
    coord=(j*30,i*30)
    surface.blit(brique_noire,coord)
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_jaune,new_coord)
        return i-0.5,j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_jaune,new_coord)
        return i,j+0.5
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_jaune,new_coord)
        return i+0.5,j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_jaune,new_coord)
        return i,j-0.5

def last_coord(i,j,f):
    res=(j*30,i*30)
    if f==1:
        res=(j*30,(i+0.5)*30)
    elif f==2:
         res=((j-0.5)*30,i*30)
    elif f==3:
        res=(j*30,(i-0.5)*30)
    else:
        res=((j+0.5)*30,i*30)
    return res

    

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
    cible = vg.voisin_approximatif(G,i,j )
    cible = Dico[cible]
    chemin_frose = fg.plus_court_chemin_sans_direction(map1,opposite(Coord[2][1]),Dico[kfrose],cible)
    chemin=[]
    for i in range(len(chemin_frose[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_frose[1][i]))
    return chemin
    
def chemin_fantome_bleu_chase (G,Coord):
    (ir,jr)=Coord[1][0]
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
    cible = (cible[0],cible[1])
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

def image_map():
#prise d'un screenshot pour convertir la map en image (=matrice de pixel)
    creation_map(map1)
    img_data = pygame.image.tostring(surface, 'RGB')
    img = Image.frombytes('RGB', (570,650), img_data)
    #plt.rcParams["figure.figsize"] = (15,10)
    img = Image.fromarray(np.array(img)) # le tableau est converti en un objet image
    pygame.quit()
    return np.array(img)
#img=image_map()



def img_map():
    creation_map(map1)
    pixel = pygame.PixelArray(surface)
    color_array = [[surface.unmap_rgb(pixel[x, y]) for x in range(0, surface.get_width())] for y in range(0, surface.get_height())]  
    rgb_array = [[(column.r, column.g, column.b) for column in row] for row in color_array]
    pygame.quit()
    return rgb_array




clock=pygame.time.Clock()

def play():
    pygame.init()
    Coord = {0:[(15,9),1], 1:[(7,9),1], 2:[(9,9),1], 3:[(9,8),1],4:[(9,10),1]}
    creation_map(map1)

    tour = 0
    surface.blit(pac_man,(9*30,15*30))
    surface.blit(fantome_rouge,(9*30,7*30))
    surface.blit(fantome_rose,(9*30,9*30))
    surface.blit(fantome_bleu,(8*30,9*30))
    surface.blit(fantome_jaune,(10*30,9*30))
    pygame.display.flip()
    
    launched=True
    
    while launched:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_a :
                    
                    while not pac_man_catch(Coord) and launched:
                        
                        for event in pygame.event.get():   
                            if event.type == pygame.QUIT:
                                launched=False
                        
                        tour+=1 
                        
                        n= vg.random_except(0,188,Dico[Coord[0][0]])
                        chemin_pm = chemin_pacman(map1, n, Coord)
                        dp= Direc[Dico[Coord[0][0]]][Dico[chemin_pm[1]]]
                        ip,jp=bouger_pac_man(Coord[0][0][0], Coord[0][0][1], dp)
                        Coord[0][0]=chemin_pm[1]
                        Coord[0][1]=dp
                        
                        if tour==1:
                            surface.blit(brique_noire,(9*30,15*30)) #fixe d'un bug d'affichage
                        
                        if state(tour)==0:
                            
                            chemin_frouge=chemin_fantome_rouge_scatter(map1,Coord)
                            drg= Direc[Dico[Coord[1][0]]][Dico[chemin_frouge[1]]]
                            irg,jrg=bouger_fantome_rouge(Coord[1][0][0], Coord[1][0][1], drg)
                            Coord[1][0]=chemin_frouge[1]
                            if Coord[1][0] == (8,9):
                                Coord[1][1]=1
                            else :
                                Coord[1][1]=drg
                            
                            chemin_frose=chemin_fantome_rose_scatter(map1,Coord)
                            drs= Direc[Dico[Coord[2][0]]][Dico[chemin_frose[1]]]
                            irs,jrs=bouger_fantome_rose(Coord[2][0][0], Coord[2][0][1], drs)
                            Coord[2][0]=chemin_frose[1]
                            if Coord[2][0] == (8,9):
                                Coord[2][1]=1
                            else :
                                Coord[2][1]=drs
                            
                            chemin_fbleu=chemin_fantome_bleu_scatter(map1,Coord)
                            db= Direc[Dico[Coord[3][0]]][Dico[chemin_fbleu[1]]]
                            ib,jb=bouger_fantome_bleu(Coord[3][0][0], Coord[3][0][1], db)
                            Coord[3][0]=chemin_fbleu[1]
                            if Coord[3][0] == (8,9):
                                Coord[3][1]=1
                            else :
                                Coord[3][1]=db
                                
                            chemin_fjaune=chemin_fantome_jaune_scatter(map1,Coord)
                            dj= Direc[Dico[Coord[4][0]]][Dico[chemin_fjaune[1]]]
                            ij,jj=bouger_fantome_jaune(Coord[4][0][0], Coord[4][0][1], dj)
                            Coord[4][0]=chemin_fjaune[1]
                            if Coord[4][0] == (8,9):
                                Coord[4][1]=1
                            else :
                                Coord[4][1]=dj
                            
                        else :
                            chemin_frouge=chemin_fantome_rouge_chase(map1,Coord)
                            drg= Direc[Dico[Coord[1][0]]][Dico[chemin_frouge[1]]]
                            irg,jrg=bouger_fantome_rouge(Coord[1][0][0], Coord[1][0][1], drg)
                            Coord[1][0]=chemin_frouge[1]
                            if Coord[1][0] == (8,9):
                                Coord[1][1]=1
                            else :
                                Coord[1][1]=drg
                            
                            chemin_frose=chemin_fantome_rose_chase(map1,Coord)
                            drs= Direc[Dico[Coord[2][0]]][Dico[chemin_frose[1]]]
                            irs,jrs=bouger_fantome_rose(Coord[2][0][0], Coord[2][0][1], drs)
                            Coord[2][0]=chemin_frose[1]
                            if Coord[2][0] == (8,9):
                                Coord[2][1]=1
                            else :
                                Coord[2][1]=drs
                            
                            chemin_fbleu=chemin_fantome_bleu_chase(map1,Coord)
                            db= Direc[Dico[Coord[3][0]]][Dico[chemin_fbleu[1]]]
                            ib,jb=bouger_fantome_bleu(Coord[3][0][0], Coord[3][0][1], db)
                            Coord[3][0]=chemin_fbleu[1]
                            if Coord[3][0] == (8,9):
                                Coord[3][1]=1
                            else :
                                Coord[3][1]=db
                                
                            chemin_fjaune=chemin_fantome_jaune_chase(map1,Coord)
                            dj= Direc[Dico[Coord[4][0]]][Dico[chemin_fjaune[1]]]
                            ij,jj=bouger_fantome_jaune(Coord[4][0][0], Coord[4][0][1], dj)
                            Coord[4][0]=chemin_fjaune[1] 
                            if Coord[4][0] == (8,9):
                                Coord[4][1]=1
                            else :
                                Coord[4][1]=dj
                        
                        pygame.display.flip()
                        #prendre un screen shot
                                    
                        #pour avoir une séquence de deux images et donc que la direction des protagonistes soit visible
                        
                        bouger_pac_man(ip,jp,dp)
                        bouger_fantome_rouge(irg,jrg,drg)
                        bouger_fantome_rose(irs,jrs,drs)
                        bouger_fantome_bleu(ib,jb,db)
                        bouger_fantome_jaune(ij,jj,dj)
                                            
                        pygame.display.flip()
                        #prendre un screen shot
                        #if not launched:
                         #   pygame.quit()
                            
                    while launched:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                launched=False
                            if event.type == pygame.KEYDOWN :
                                if event.key == pygame.K_a :
                                    play()
                    pygame.quit()

#test=play()


