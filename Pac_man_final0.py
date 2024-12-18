
import pygame
import map_to_graphe as vg
import fonctions_de_graphes_TIPE as fg
import random
import ast


dijkstra = open('Dijkstra.txt','r')
dijkstra = dijkstra.read()
dijkstra = ast.literal_eval(dijkstra)

dijkstra_sans_direction = open('Dijkstra_without_direction.txt','r')
dijkstra_sans_direction = dijkstra_sans_direction.read()
dijkstra_sans_direction = ast.literal_eval(dijkstra_sans_direction)

pygame.init()
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

fantome_peur=pygame.image.load("fantome_peur.png")
fantome_peur=pygame.transform.scale(fantome_peur,(30,30))

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

pac_gomme=pygame.image.load("pac_gomme.png")
pac_gomme=pygame.transform.scale(pac_gomme,(30,30))

super_pac_gomme=pygame.image.load("super_pac_gomme.png")
super_pac_gomme=pygame.transform.scale(super_pac_gomme,(30,30))

cerise=pygame.image.load("cerise.png")
cerise=pygame.transform.scale(cerise,(30,30))

fraise=pygame.image.load("fraise.png")
fraise=pygame.transform.scale(fraise,(30,30))


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

def creation_map(map1,gomme):
    for y, line in enumerate(map1):
        for x, c in enumerate(line):
            coord=(x*30,y*30)
            if c=="9":
                if gomme[(y,x)] == 0:
                    surface.blit(brique_noire,coord)
                if gomme[(y,x)] == 1:
                    surface.blit(pac_gomme,coord)
                if gomme[(y,x)] == 2:
                    surface.blit(super_pac_gomme,coord)
                if gomme[(y,x)] == 3:
                    surface.blit(cerise,coord)
                if gomme[(y,x)] == 4:
                    surface.blit(fraise,coord)
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

def bouger_pac_man(i,j,f):
    coord=(j*30,i*30)
    
    if f==0:
        surface.blit(pac_man,coord)
        return i,j
        
    surface.blit(brique_noire,coord)
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(pac_man,new_coord)
        return (i-0.5)%len(map1),j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(pac_man,new_coord)
        return i,(j+0.5)%len(map1[1])
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(pac_man,new_coord)
        return (i+0.5)%len(map1),j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(pac_man,new_coord)
        return i,(j-0.5)%len(map1[1])
        

def bouger_fantome_bleu(i,j,f):
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_bleu,new_coord)
        return (i-0.5)%len(map1),j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_bleu,new_coord)
        return i,(j+0.5)%len(map1[1])
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_bleu,new_coord)
        return (i+0.5)%len(map1),j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_bleu,new_coord)
        return i,(j-0.5)%len(map1[1])

def bouger_fantome_rouge(i,j,f):
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_rouge,new_coord)
        return (i-0.5)%len(map1),j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_rouge,new_coord)
        return i,(j+0.5)%len(map1[1])
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_rouge,new_coord)
        return (i+0.5)%len(map1),j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_rouge,new_coord)
        return i,(j-0.5)%len(map1[1])

def bouger_fantome_rose(i,j,f):
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_rose,new_coord)
        return (i-0.5)%len(map1),j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_rose,new_coord)
        return i,(j+0.5)%len(map1[1])
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_rose,new_coord)
        return (i+0.5)%len(map1),j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_rose,new_coord)
        return i,(j-0.5)%len(map1[1])

def bouger_fantome_jaune(i,j,f):
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_jaune,new_coord)
        return (i-0.5)%len(map1),j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_jaune,new_coord)
        return i,(j+0.5)%len(map1[1])
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_jaune,new_coord)
        return (i+0.5)%len(map1),j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_jaune,new_coord)
        return i,(j-0.5)%len(map1[1])

def bouger_fantome_peur(i,j,f):
    
    if f==1:
        new_coord=(j*30,(i-0.5)*30)
        surface.blit(fantome_peur,new_coord)
        return (i-0.5)%len(map1),j
    elif f==2:
        new_coord=((j+0.5)*30,i*30)
        surface.blit(fantome_peur,new_coord)
        return i,(j+0.5)%len(map1[1])
    elif f==3:
        new_coord=(j*30,(i+0.5)*30)
        surface.blit(fantome_peur,new_coord)
        return (i+0.5)%len(map1),j
    else:
        new_coord=((j-0.5)*30,i*30)
        surface.blit(fantome_peur,new_coord)
        return i,(j-0.5)%len(map1[1])
    
def last_coord_indice(i,j,f):
    if f==1 :
        res = ((i+0.5)%len(map1),j)
    elif f==2:
        res = (i,(j-0.5)%len(map1[1]))
    elif f==3:
        res = ((i-0.5)%len(map1),j)
    else:
        res = (i,(j+0.5)%len(map1[1]))
    return res

def next_coord_indice(i,j,f):
    if f==1:
        res = ((i-0.5)%len(map1),j)
    elif f==2:
        res = (i,(j+0.5)%len(map1[1]))
    elif f==3:
        res = ((i+0.5)%len(map1),j)
    else :
        res = (i,(j-0.5)%len(map1[1]))
    return res
    
    
    
def last_coord(i,j,f):
    if f==1 :
        res = ((i+0.5)%len(map1)*30,j*30)
    elif f==2:
        res = (i*30,(j-0.5)%len(map1[1])*30)
    elif f==3:
        res = ((i-0.5)%len(map1)*30,j*30)
    else:
        res = (i*30,(j+0.5)%len(map1[1])*30)
    return res

def last_coord_indice_entiere(i,j,f):
    if f==1 :
        res = ((i+1)%len(map1),j)
    elif f==2:
        res = (i,(j-1)%len(map1[1]))
    elif f==3:
        res = ((i-1)%len(map1),j)
    else:
        res = (i,(j+1)%len(map1[1]))
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
    chemin_pm=dijkstra[kpm][k][1]
    chemin=[]
    for i in range(len(chemin_pm[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_pm[1][i]))
    return chemin

def chemin_fantome_rouge_chase (G,Coord):
    kfrouge=Dico[Coord[1][0]]
    chemin_frouge = dijkstra_sans_direction[kfrouge][Dico[Coord[0][0]]][opposite(Coord[1][1])-1]
    chemin=[]
    for i in range(len(chemin_frouge[1])):
        chemin.append(vg.valeur_to_clef(Dico,chemin_frouge[1][i]))
    return chemin
    
def chemin_fantome_rose_chase (G,Coord):
    kfrose = Coord[2][0]
    (ipm,jpm) = Coord[0][0]
    d = Coord[0][1]
    k = vg.voisin_plus_loins(G, ipm, jpm, d, 4)
    (i,j)=k
    cible = vg.voisin_approximatif(G, i,j )
    (ic,jc) =  cible
    if cible == kfrose:
        cible = vg.voisin_approximatif_direction(G, ic, jc, Coord[2][1])
    cible = Dico[cible]
    chemin_frose = dijkstra_sans_direction[Dico[kfrose]][cible][opposite(Coord[2][1])-1]
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
    cible = vg.voisin_approximatif(map1,cible[0],cible[1])
    (ic,jc)=cible
    if Dico[cible] == kfbleu:
        cible = vg.voisin_approximatif_direction(G, ic, jc, Coord[3][1])
    cible = Dico[cible]
    chemin_fbleu = dijkstra_sans_direction[kfbleu][cible][opposite(Coord[3][1])-1]
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
        chemin_fjaune = dijkstra_sans_direction[kfjaune][Dico[Coord[0][0]]][opposite(Coord[4][1])-1]
        chemin=[]
        for i in range(len(chemin_fjaune[1])):
            chemin.append(vg.valeur_to_clef(Dico,chemin_fjaune[1][i]))
        return chemin
    else : 
        return chemin_fantome_jaune_scatter (G,Coord)

def chemin_fantome_rose_scatter (G,Coord):
    kfrose=Dico[Coord[2][0]]
    if kfrose != 0 :
        chemin_frose = dijkstra_sans_direction[kfrose][0][opposite(Coord[2][1])-1]
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
        chemin_frouge = dijkstra_sans_direction[kfrouge][15][opposite(Coord[1][1])-1]
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
        chemin_fjaune  = dijkstra_sans_direction[kfjaune][172][opposite(Coord[4][1])-1]
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
        chemin_fbleu = dijkstra_sans_direction[kfbleu][188][opposite(Coord[3][1])-1]
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

def chemin_fantome_frigthtened(i,j,d):
    f = vg.random_except(1, 5, opposite(d))
    while vg.voisin_coord(map1,i,j,f) not in Dico.keys() :
        f = vg.random_except(1, 5, opposite(d))
    return f

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
    f=[]
    for k in range(1, 5):
        if Coord[0][0]==Coord[k][0]:
            res = True
            f.append(k)
    return [res,f]

def redirection(i,j,d):
    if (i,j)==(9,8):
        return 2
    if(i,j)==(9,9):
        return 1
    if (i,j)==(9,10):
        return 4
    if (i,j)==(8,9):
        return 1
    return d

spawn = [(8,9),(9,9),(9,8),(9,10)]

def actions_possibles(i,j,d):
    #d est la précédente direction de pac man 
    #fonction inutile pour l'IA
    res=[]
    if map1[i-1][j]=='9':
        res.append(1)
    elif d==1:
        res.append(1)
        
    if j==len(map1[0])-1 or map1[i][j+1]=='9': #pac man peut être sur la case de téléportation droite
        res.append(2)
    elif d==2:
        res.append(2)
      
    if map1[i+1][j]=='9':
        res.append(3)
    elif d==3:
        res.append(3)
        
    if j==0 or map1[i][j-1]=='9': #...case de téléportation gauche
        res.append(4)
    elif d==4 :
        res.append(4)
    return res

def bouge_dans_mur(i,j,d,lastd):
    #print(i,j,d,lastd)
    #retourne si pac man veut aller dans le mur ou non et quel mouvement cela produit sur le jeu (0=pas de mvt)
    if d==1:
        if map1[i-1][j]!='9':
            if d==lastd:
                return True,0
            else:
                #print(lastd)
                return bouge_dans_mur(i,j,lastd,lastd)
        else:
            return False,d
        
    if d==2:
        if j!=len(map1[0])-1 and map1[i][j+1]!='9': #pac man peut être sur la case de téléportation droite
            if d==lastd:
                return True,0
            else:
                return bouge_dans_mur(i,j,lastd,lastd)
        else:
            return False,d    
    
    
    if d==3:
        if map1[i+1][j]!='9':
            if d==lastd:
                return True,0
            else:
                return bouge_dans_mur(i,j,lastd,lastd)
        else:
            return False,d    
    
    else:
        if j!=0 and map1[i][j-1]!='9': #...case de téléportation gauche
            if d==lastd:
                return True,0
            else:
                return bouge_dans_mur(i,j,lastd,lastd)
        else:
            return False,d    
    
 


def replace(i,j,d,peurs,Gomme):
    (pi,pj)=last_coord_indice_entiere(i, j, d)
    coord = (pj*30,pi*30)
    if Gomme[(pi,pj)] == 1:
        surface.blit(pac_gomme,coord)
    if Gomme[(pi,pj)] == 2:
        surface.blit(super_pac_gomme,coord)
    if Gomme[(pi,pj)] == 0: 
        surface.blit(brique_noire,coord)
    if Gomme[(pi,pj)] == 3: 
        surface.blit(cerise,coord)
    if Gomme[(pi,pj)] == 4: 
        surface.blit(fraise,coord)
    if (pi,pj)==Coord[0][0]:
        surface.blit(pac_man,coord)
    if (pi,pj)==Coord[1][0]:
        if peurs[0]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_rouge,coord)
    if (pi,pj)==Coord[2][0]:
        if peurs[1]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_rose,coord)
    if (pi,pj)==Coord[3][0]:
        if peurs[2]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_bleu,coord)
    if (pi,pj)==Coord[4][0]:
        if peurs[3]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_jaune,coord)

def replace_coord(i,j,peurs,Coord,Gomme):
    coord = (j*30,i*30)
    if Gomme[(i,j)] == 1:
        surface.blit(pac_gomme,coord)
    if Gomme[(i,j)] == 2:
        surface.blit(super_pac_gomme,coord)
    if Gomme[(i,j)] == 0: 
        surface.blit(brique_noire,coord)
    if Gomme[(i,j)] == 3: 
        surface.blit(cerise,coord)
    if Gomme[(i,j)] == 4: 
        surface.blit(fraise,coord)
    if (i,j)==Coord[0][0]:
        surface.blit(pac_man,coord)
    if (i,j)==Coord[1][0]:
        if peurs[0]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_rouge,coord)
    if (i,j)==Coord[2][0]:
        if peurs[1]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_rose,coord)
    if (i,j)==Coord[3][0]:
        if peurs[2]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_bleu,coord)
    if (i,j)==Coord[4][0]:
        if peurs[3]:
            surface.blit(fantome_peur,coord)
        else :
            surface.blit(fantome_jaune,coord)

def replace_global(peurs,Coord,Gomme):
    for (i,j) in Dico.keys():    
        replace_coord(i,j,peurs,Coord,Gomme)

"""fonctions qui modifient directement la fenêtre pygame"""

pygame.init()

def game_reset():
    Gomme=vg.gomme(map1)
    creation_map(map1,Gomme)
    vg.init_seed()
    tour = 0
    points = 0
    peur = 0
    peurs = [False,False,False,False]
    killstreak = 0
    catch = [False,[0]]
    vie=3
    surface.blit(pac_man,(9*30,15*30))
    surface.blit(fantome_rouge,(9*30,7*30))
    surface.blit(fantome_rose,(9*30,9*30))
    surface.blit(fantome_bleu,(8*30,9*30))
    surface.blit(fantome_jaune,(10*30,9*30))
    pygame.display.flip()
    
    Coord = {0:[(15,9),1], 1:[(7,9),1], 2:[(9,9),1], 3:[(9,8),1],4:[(9,10),1]}
    
    return Coord, Gomme, tour, points, peur, peurs, killstreak, catch, vie


def respawn(Gomme,tour,peur,peurs,vie):
    creation_map(map1,Gomme)
    
    points = 0
    killstreak = 0
    catch = (False,[0])
    surface.blit(pac_man,(9*30,15*30))
    surface.blit(fantome_rouge,(9*30,7*30))
    surface.blit(fantome_rose,(9*30,9*30))
    surface.blit(fantome_bleu,(8*30,9*30))
    surface.blit(fantome_jaune,(10*30,9*30))
    pygame.display.flip()
    Coord = {0:[(15,9),1], 1:[(7,9),1], 2:[(9,9),1], 3:[(9,8),1],4:[(9,10),1]}
        
    return Coord, Gomme, tour, points, peur, peurs, killstreak, catch, vie-1

def win(Gomme):
    if vg.compte_gomme(Gomme)==0:
        return True
    return False



clock=pygame.time.Clock()

def take_action(dp,va_jeu):
    Coord, Gomme, tour, points, peur, peurs, killstreak, catch, vie =va_jeu
    points=0
    lastd=Coord[0][1]
    ip,jp=Coord[0][0][0],Coord[0][0][1]
    
    
    mur,dp1=bouge_dans_mur(ip,jp,dp,lastd)
    ip,jp=bouger_pac_man(ip, jp, dp1)
    if dp1!=0:
        dp=dp1
    Coord[0][1]=dp 
    
    coordonnées = []
    for k in range(5):
        coordonnées.append(Coord[k][0])
    
    catch = pac_man_catch(Coord)
    
    if (catch[0] and peur==0) :
        replace_global(peurs,Coord,Gomme)
        return respawn(Gomme,tour,peur,peurs,vie)
    
        
    if (catch[0] and peur > 0):
        if catch[1]!=[]:
            for k in catch[1]:
                k-=1
                if peurs[k]:
                    catch[0]=False
                    peurs[k]=False
                    killstreak +=1
                    if killstreak == 1:
                        points += 200
                    elif killstreak == 2:
                        points += 400
                    elif killstreak == 3:
                        points += 800
                    elif killstreak == 4:
                        points += 1600
                    
                    replace_global(peurs,Coord,Gomme)
                                                
                    if k == 0:
                        Coord[1]=[(7,9),1]
                    if k == 1:
                        Coord[2]=[(9,9),1]
                    if k == 2:
                        Coord[3]=[(9,8),2]
                    if k == 3:
                        Coord[4]=[(9,10),4]
                    
                else :
                    return respawn(Gomme,tour,peur,peurs, vie)
    catch[1]=[]
    
    tour+=1 
    if peur == 22:
        peurs = [False,False,False,False]
        peur = 0
        killstreak = 0
    if peur > 0 :
        peur +=1
        
    if vg.compte_gomme(Gomme) == 40:
        Gomme[(11,9)]=3
        surface.blit(cerise,(11,9))
    if vg.compte_gomme(Gomme) == 100:
        Gomme[(11,9)]=4
        surface.blit(fraise,(11,9))
        
    if Gomme[Coord[0][0]] == 1:
        points += 10
        Gomme[Coord[0][0]]=0
    if Gomme[Coord[0][0]] == 3:
        points += 100
        print("cerise")
        Gomme[Coord[0][0]]=0
    if Gomme[Coord[0][0]] == 4:
        points += 200
        print("fraise")
        Gomme[Coord[0][0]]=0
        
    if Gomme[Coord[0][0]] == 2:
        peur = 1
        peurs = [True,True,True,True]
        for k in range (1,4):
            Coord[k][1] = opposite(Coord[k][1])
        Gomme[Coord[0][0]]=0
        
    
    if (state(tour)==0 and peurs[0] == False and (1 not in catch[1])) or (peurs[0]==False and Coord[1][0] in spawn) :        
        chemin_frouge=chemin_fantome_rouge_scatter(map1,Coord)
        drg= Direc[Dico[Coord[1][0]]][Dico[chemin_frouge[1]]]
        irg,jrg = bouger_fantome_rouge(Coord[1][0][0], Coord[1][0][1], drg)
        Coord[1][0]=chemin_frouge[1]
        if Coord[1][0] == (8,9):
            Coord[1][1]=1
        else :
            Coord[1][1]=drg
    
    if state(tour)==0 and peurs[1] == False and (2 not in catch[1]) or (peurs[1]==False and Coord[2][0] in spawn):
        
        chemin_frose=chemin_fantome_rose_scatter(map1,Coord)
        drs= Direc[Dico[Coord[2][0]]][Dico[chemin_frose[1]]]
        irs,jrs = bouger_fantome_rose(Coord[2][0][0], Coord[2][0][1], drs)
        Coord[2][0]=chemin_frose[1]
        if Coord[2][0] == (8,9):
            Coord[2][1]=1
        else :
            Coord[2][1]=drs
    
    if state(tour)==0 and peurs[2] == False and (3 not in catch[1]) or (peurs[2]==False and Coord[3][0] in spawn):
        chemin_fbleu=chemin_fantome_bleu_scatter(map1,Coord)
        db= Direc[Dico[Coord[3][0]]][Dico[chemin_fbleu[1]]]
        ib,jb = bouger_fantome_bleu(Coord[3][0][0], Coord[3][0][1], db)
        Coord[3][0]=chemin_fbleu[1]
        if Coord[3][0] == (8,9):
            Coord[3][1]=1
        else :
            Coord[3][1]=db
    
    if state(tour)==0 and peurs[3] == False and (4 not in catch[1]) or (peurs[3]==False and Coord[4][0] in spawn):
        chemin_fjaune=chemin_fantome_jaune_scatter(map1,Coord)
        dj= Direc[Dico[Coord[4][0]]][Dico[chemin_fjaune[1]]]
        ij,jj = bouger_fantome_jaune(Coord[4][0][0], Coord[4][0][1], dj)
        Coord[4][0]=chemin_fjaune[1]
        if Coord[4][0] == (8,9):
            Coord[4][1]=1
        else :
            Coord[4][1]=dj
    
    if state(tour) == 1 and peurs[0] == False and (1 not in catch[1]) and not (Coord[1][0] in spawn):
        
        chemin_frouge=chemin_fantome_rouge_chase(map1,Coord)
        drg= Direc[Dico[Coord[1][0]]][Dico[chemin_frouge[1]]]
        irg, jrg = bouger_fantome_rouge(Coord[1][0][0], Coord[1][0][1], drg)
        Coord[1][0]=chemin_frouge[1]
        if Coord[1][0] == (8,9):
            Coord[1][1]=1
        else :
            Coord[1][1]=drg
        
    if state(tour) == 1 and peurs[1] == False and (2 not in catch[1]) and not (Coord[2][0] in spawn):
        chemin_frose=chemin_fantome_rose_chase(map1,Coord)
        drs= Direc[Dico[Coord[2][0]]][Dico[chemin_frose[1]]]
        irs,jrs = bouger_fantome_rose(Coord[2][0][0], Coord[2][0][1], drs)
        Coord[2][0]=chemin_frose[1]
        if Coord[2][0] == (8,9):
            Coord[2][1]=1
        else :
            Coord[2][1]=drs
            
    if state(tour) == 1 and peurs[2] == False and (3 not in catch[1]) and not (Coord[3][0] in spawn):

        chemin_fbleu=chemin_fantome_bleu_chase(map1,Coord)
        db= Direc[Dico[Coord[3][0]]][Dico[chemin_fbleu[1]]]
        ib,jb = bouger_fantome_bleu(Coord[3][0][0], Coord[3][0][1], db)
        Coord[3][0]=chemin_fbleu[1]
        if Coord[3][0] == (8,9):
            Coord[3][1]=1
        else :
            Coord[3][1]=db
    
    if state(tour) == 1 and peurs[3] == False and (4 not in catch[1]) and not (Coord[4][0] in spawn):
        
        chemin_fjaune=chemin_fantome_jaune_chase(map1,Coord)
        dj= Direc[Dico[Coord[4][0]]][Dico[chemin_fjaune[1]]]
        ij,jj = bouger_fantome_jaune(Coord[4][0][0], Coord[4][0][1], dj)
        Coord[4][0]=chemin_fjaune[1]
        if Coord[4][0] == (8,9):
            Coord[4][1]=1
        else :
            Coord[4][1]=dj
    
    if peurs[0]:
        ((i,j),d)=Coord[1]
        drg = chemin_fantome_frigthtened(i,j,d)
        drg= redirection(i,j,drg)
        (irg,jrg)=bouger_fantome_peur(i, j, drg)
        (inrg,jnrg)=next_coord_indice(irg,jrg,drg)
        Coord[1][0]=(int(inrg),int(jnrg))
        Coord[1][1]=drg
    
    if peurs[1]:
        ((i,j),d)=Coord[2]
        drs = chemin_fantome_frigthtened(i,j,d)
        drs= redirection(i,j,drs)
        (irs,jrs)=bouger_fantome_peur(i, j, drs)
        (inrs,jnrs)=next_coord_indice(irs,jrs,drs)
        Coord[2][0]=(int(inrs),int(jnrs))
        Coord[2][1]=drs
    
    if peurs[2]:                
        ((i,j),d)=Coord[3]
        db = chemin_fantome_frigthtened(i,j,d)
        db= redirection(i,j,db)
        (ib,jb)=bouger_fantome_peur(i, j, db)
        (inb,jnb)=next_coord_indice(ib,jb,db)
        Coord[3][0]=(int(inb),int(jnb))
        Coord[3][1]=db
         
    if peurs[3]:
        ((i,j),d)=Coord[4]
        dj = chemin_fantome_frigthtened(i,j,d)
        dj= redirection(i,j,dj)
        (ij,jj)=bouger_fantome_peur(i, j, dj)
        (inj,jnj)=next_coord_indice(ij,jj,dj)
        Coord[4][0]=(int(inj),int(jnj))
        Coord[4][1]=dj
    
    replace_global(peurs,Coord,Gomme)
                            
    catch=pac_man_catch(Coord)
    
    if (catch[0] and peur==0) :
        replace_global(peurs,Coord,Gomme)
        return respawn(Gomme,tour,peur,peurs, vie)
        
    
        
    if (catch[0] and peur > 0):
        if catch[1]!=[]:
            for k in catch[1]:
                k-=1
                if peurs[k]:
                    catch[0]=False
                    peurs[k]=False
                    killstreak +=1
                    if killstreak == 1:
                        points += 200
                    elif killstreak == 2:
                        points += 400
                    elif killstreak == 3:
                        points += 800
                    elif killstreak == 4:
                        points += 1600
                    
                    replace_global(peurs,Coord,Gomme)
                                                
                    if k == 0:
                        Coord[1]=[(7,9),1]
                    if k == 1:
                        Coord[2]=[(9,9),1]
                    if k == 2:
                        Coord[3]=[(9,8),2]
                    if k == 3:
                        Coord[4]=[(9,10),4]
                else :
                    return respawn(Gomme,tour,peur,peurs, vie)
        
    pygame.display.flip()
    
    
    ip,jp=bouger_pac_man(ip,jp,dp1)
    Coord[0][0]=(int(ip),int(jp))
    if peurs[0]==0 and (1 not in catch[1]):
        irg,jrg=bouger_fantome_rouge(irg,jrg,drg)
    elif (1 not in catch[1]) :
        irg,jrg=bouger_fantome_peur(irg,jrg,drg)
    if peurs[1]==0 and (2 not in catch[1]):
        irs,jrs=bouger_fantome_rose(irs,jrs,drs)
    elif (2 not in catch[1]) :
        irs,jrs=bouger_fantome_peur(irs,jrs,drs)
    if peurs[2]==0 and (3 not in catch[1]):
        ib,jb=bouger_fantome_bleu(ib,jb,db)
    elif (3 not in catch[1]) :
        ib,jb=bouger_fantome_peur(ib,jb,db)
    if peurs[3]==0 and (4 not in catch[1]):
        ij,jj=bouger_fantome_jaune(ij,jj,dj)
    elif (4 not in catch[1]) :
        ij,jj=bouger_fantome_peur(ij,jj,dj)
    
    replace_global(peurs,Coord,Gomme)
                            
    pygame.display.flip()
    
    clock.tick()
    
    
    va_jeu = Coord, Gomme, tour, points, peur, peurs, killstreak, catch, vie
    return va_jeu



Coord={0:[(15,9),1], 1:[(7,9),1], 2:[(9,9),1], 3:[(9,8),1],4:[(9,10),1]}



