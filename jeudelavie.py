import tkinter
from random import randint
import time

class Case:
    def __init__(self, val=0) :
        '''Case -> None
        Constructeur des cases.
        '''
        self.val = val

    def str(self) :
        '''Case -> str
        Retourne une représentation sous forme textuelle d'une case.
        '''
        if self.est_morte() :
            return ' - '
        return ' * '

    def est_morte(self) :
        '''Case -> boolean
        Retourne vrai si la case est morte.
        ''' 
        return self.val == 0

    def est_vivante(self) :
        '''Case -> boolean
        Retourne vrai si la case est vivante.
        ''' 
        return self.val == 1

    def valeur(self) :
        '''Case -> int
        Retourne la valeur de la case (0 : morte, 1 : vivante).
        ''' 
        return self.val

class Jeu:
    def __init__(self, nblig=20, nbcol=57):
        '''Jeu -> None
        Constructeur du jeu.
        '''
        self.nblig = nblig
        self.nbcol = nbcol
        self.plateau = []
        for i in range(nblig) :
            lig = []
            for j in range(nbcol) :
                c = Case()
                lig.append(c)
            self.plateau.append(lig)

    def afficheGrille(self) :
        '''Jeu -> None
        Afficher la grille du jeu pour la version en mode texte.
        '''
        res = '\nColonne '
        for i in range(self.nbcol):
            if i <= 10:
                res += ' '
            res += str(i) + ' '
        print(res)
        for j in range(self.nblig):
            self.affiche_ligne(j)

    def affiche_ligne(self,lig) :
        '''Jeu, int -> None
        Afficher une ligne de la grille pour le jeu en mode texte.
        '''
        if lig < 10:
            res = 'Ligne  ' + str(lig)
        else:
            res = 'Ligne ' + str(lig)
        for i in range(self.nbcol) :
            res += self.plateau[lig][i].str()
        print(res)

    def etapeSuivante(self):
        '''Jeu -> None
        Applique les règles du jeu pour obtenir la prochaine génération du modèle.
        '''
        li_mourrante = []
        li_vivante = []
        for lig in range(self.nblig):
            for col in range(self.nbcol):
                nb = self.getAdj(lig,col)
                if self.plateau[lig][col].est_morte() and nb==3:
                    li_vivante.append((lig,col))
                elif self.plateau[lig][col].est_vivante() and (nb==2 or nb==3):
                    li_vivante.append((lig,col))
                else:
                    li_mourrante.append((lig,col))
        for coords in li_mourrante:
            self.plateau[coords[0]][coords[1]].val = 0
        for coords in li_vivante:
            self.plateau[coords[0]][coords[1]].val = 1

    def getAdj(self,l,c):
        '''Jeu, int, int, -> int
        Compte le nombre de cellules vivantes qui sont immédiatement adjacentes
        à la cellule de coordonnées (l,c).
        '''
        cpt = 0
        for lig in range(-1,2):
            for col in range(-1,2):
                if lig != 0 or col != 0:
                    if 0<=l+lig<self.nblig and 0<=c+col<self.nbcol:
                        if self.plateau[l+lig][c+col].est_vivante():
                            cpt += 1
        return cpt

    def demande_nb_vivantes(self):
        '''Jeu -> int
        Dans la version texte, demande à l'utilisateur combien de cellules
        vivantes vont être placées aléatoirement.
        '''
        nb = int(input('Combien voulez-vous de cellules vivantes ? '))
        while not(0 <= nb <= self.nblig * self.nbcol):
            print('Réponse incorrecte.')
            nb = int(input('Combien voulez-vous de cellules vivantes ? '))
        return nb
    
    def demande_aleatoire(self):
        '''Jeu -> int
        Dans la version texte, demande à l'utilisateur s'il veut générer une
        grille aléatoire.
        '''
        aleat = int(input('\nVoulez-vous générer une grille aléatoire (1) ou non (0) ? '))
        while aleat != 1 and aleat !=0:
            print('Réponse incorrecte.')
            aleat = int(input('\nVoulez-vous générer une grille aléatoire (1) ou non (0) ? '))
        return aleat

    def placeVCelsRandom(self,nb):
        '''Jeu, int -> None
        Place nb cellules vivantes aléatoirement dans la grille, après l'avoir
        nettoyé.
        '''
        for i in range(self.nblig):
            for j in range(self.nbcol):
                self.plateau[i][j].val = 0
        for i in range(nb):
            lig = randint(0,self.nblig-1)
            col = randint(0,self.nbcol-1)
            while self.plateau[lig][col].est_vivante():
                lig = randint(0,self.nblig-1)
                col = randint(0,self.nbcol-1)
            self.plateau[lig][col].val = 1
                        
    def estGrilleVide(self):
        '''Jeu -> boolean
        Retourne si la grille est vide, c'est-à-dire si toutes les cellules
        sont mortes.
        '''
        for lig in range(self.nblig):
              for col in range(self.nbcol):
                if self.plateau[lig][col].est_vivante():
                    return False
        return True

    def reinit(self) :
        '''Jeu) -> None
        Réinitialise la grille du jeu
        '''
        self.plateau = []
        for i in range(self.nblig) :
            self.plateau.append([])
            for j in range(self.nbcol) :
                self.plateau[i].append(Case())

    def main(self):
        '''Jeu -> None
        Fonction principale de la classe Jeu.
        '''
        self.afficheGrille()
        aleat = self.demande_aleatoire()
        if aleat == 1:
            nb = self.demande_nb_vivantes()
            self.placeVCelsRandom(nb)
            self.afficheGrille()
        while self.estGrilleVide() == False:
            self.etapeSuivante()
            self.afficheGrille()
        print('Partie terminée !')

class Vue:
    def __init__(self,modele):
        '''Vue, Jeu -> None
        Constructeur de la classe Vue.
        '''
        self.modele = modele
        self.fen1 = tkinter.Tk()
        self.fen1.title("Choix des dimensions")
        self.fen1.configure(bg='white')
        btn_valider = tkinter.Button(self.fen1,text='Valider',fg='white',bg='black',command=lambda:self.validation())
        btn_valider.grid(row=2, column=2)
        tkinter.Label(self.fen1, fg='black',bg='white',text="Nombre de lignes (max : "+str(self.modele.nblig)+")").grid(row=0)
        tkinter.Label(self.fen1, fg='black',bg='white',text="Nombre de colonnes (max : "+str(self.modele.nbcol)+")").grid(row=1)
        self.e3 = tkinter.Entry(self.fen1,fg='white',bg='black',width=6)
        self.e3.insert(0,0)
        tkinter.Label(self.fen1, fg='black',bg='white',text="Nombre de cases aléatoires").grid(row=2)
        self.e1 = tkinter.Entry(self.fen1,fg='white',bg='black',width=3)
        self.e2 = tkinter.Entry(self.fen1,fg='white',bg='black',width=3)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.fen1.lift()
        self.fen1.attributes('-topmost',True)
        self.fen1.after_idle(self.fen1.attributes,'-topmost',False)
        self.fen1.mainloop( )
        self.modele.nblig = self.nblig
        self.modele.nbcol = self.nbcol
        self.fenetre = tkinter.Tk()
        self.fenetre.title("Jeu de la vie")
        self.fenetre.configure(bg='white')
        self.delai = 1500
        frTerrain = tkinter.Frame(self.fenetre)
        accral =  tkinter.Frame(self.fenetre)
        accral.configure(bg='white')
        cleaquit = tkinter.Frame(self.fenetre)
        cleaquit.configure(bg='white')
        self.gene = 0
        self.li = []
        for i in range(self.nblig):
            ligne = []
            for j in range(self.nbcol):
                self.btn_case = tkinter.Button(frTerrain, width=2, height=1)
                self.btn_case.grid(row=i,column=j)
                ligne.append(self.btn_case)
            self.li.append(ligne)                                      
        self.btn_start = tkinter.Button(self.fenetre,text='Start',fg='white',bg='black',command=self.btn_stop)
        self.btn_start.pack(side='top',padx=10,pady=5)
        self.btn_aleat = tkinter.Button(self.fenetre,text='Cases aléatoires',fg='white',bg='black',command=lambda: self.modele.placeVCelsRandom((self.nblig*self.nbcol)//2))
        self.btn_aleat.pack(side='top',padx=10,pady=5)
        btn_clear = tkinter.Button(cleaquit,text='    Clear   ',fg='white',bg='black',command=self.ctrl_reinit)
        btn_clear.pack(side='left',padx=11,pady=5)
        btn_quitter = tkinter.Button(cleaquit,text='Quitter',fg='white',bg='black',command=self.fenetre.destroy)
        btn_quitter.pack(side='right',padx=20,pady=5)
        self.btn_accelerer = tkinter.Button(accral,text='Accélérer',fg='white',bg='black',command=self.accelerer)
        self.btn_accelerer.pack(side='left',padx=10,pady=5)
        self.btn_ralentir = tkinter.Button(accral,text='Ralentir',fg='white',bg='black',command=self.ralentir)
        self.btn_ralentir.pack(side='right',padx=20,pady=5)
        accral.pack()
        cleaquit.pack()
        frTerrain.pack()
        self.lbl_generation = tkinter.Label(self.fenetre,text="Génération n°0")
        self.lbl_generation.pack(side='top')
        self.boucle = tkinter.Label(self.fenetre,text="")
        self.boucle.pack(side='top')
        self.ctrl_reinit()
        self.fenetre.lift()
        self.fenetre.attributes('-topmost',True)
        self.fenetre.after_idle(self.fenetre.attributes,'-topmost',False)
        self.fenetre.geometry("%dx%d+0+0" % (self.fenetre.winfo_screenwidth(),self.fenetre.winfo_screenheight()))

    def btn_stop(self):
        '''Vue -> None
        Gère le bouton "Stop".
        '''
        self.btn_start.config(text='Stop',command=self.btn_commencer)
        self.pause = False

    def btn_commencer(self):
        '''Vue -> None
        Gère le bouton "Commencer".
        '''
        self.btn_start.config(text='Continue',command=self.btn_stop)
        self.pause = True

    def accelerer(self):
        '''Vue -> None
        Accélère la durée entre chaque génération du jeu.
        '''
        self.delai -= (self.delai)/3
        if self.delai < 2:
            self.delai = 2
            self.btn_accelerer.configure(text='MAX',bg='red')
        else:
            self.btn_accelerer.configure(text='Accélérer',bg='black')
            self.btn_ralentir.configure(text='Ralentir',bg='black')

    def validation(self):
        '''Vue -> None
        Gère le bouton "Valider" de la première fenêtre.
        '''
        if (0 < int(self.e1.get()) <= self.modele.nblig) and (0 < int(self.e2.get()) <= self.modele.nbcol) and (len(self.e3.get())<=1 or 0 <= int(self.e3.get()) <= (int(self.e1.get())*int(self.e2.get()))):
            self.nblig = int(self.e1.get())
            self.nbcol = int(self.e2.get())
            if len(self.e3.get()) != 0:
                self.nbaleat = int(self.e3.get())
            else:
                self.nbaleat = 0
            self.fen1.destroy()

    def ralentir(self):
        '''Vue -> None
        Ralentit la durée entre chaque génération du jeu.
        '''
        self.delai += (self.delai)/3
        if self.delai > 5000:
            self.delai = 5000
            self.btn_ralentir.configure(text='MINI',bg='red')
        else:
            self.btn_ralentir.configure(text='Ralentir',bg='black')
            self.btn_accelerer.configure(text='Accélérer',bg='black')

    def change_en_vivant(self,i,j):
        '''Vue, int, int -> None
        Change la valeur de la case de coordonnées (i,j) à 1 (vivante).
        '''
        self.li[i][j].configure(bg = 'white', command=lambda:self.change_en_mort(i,j))
        self.modele.plateau[i][j].val = 1

    def change_en_mort(self,i,j):
        '''Vue, int, int -> None
        Change la valeur de la case de coordonnées (i,j) à 0 (morte).
        '''
        self.li[i][j].configure(bg = 'black', command=lambda:self.change_en_vivant(i,j))
        self.modele.plateau[i][j].val = 0

    def dessine_case(self,lig,col):
        '''Vue, int, int -> None
        Dessine la case de coordonnées (lig,col).
        '''
        if self.modele.plateau[lig][col].est_vivante():
            self.li[lig][col].config(bg='white',command=lambda:self.change_en_mort(lig,col))
        if self.modele.plateau[lig][col].est_morte():
            self.li[lig][col].config(bg='black',command=lambda:self.change_en_vivant(lig,col))

    def dessine_terrain(self):
        '''Vue -> None
        Dessine la grille.
        '''
        for lig in range(self.nblig):
            for col in range(self.nbcol):
                self.dessine_case(lig,col)

    def fin_detect(self):
        '''Vue -> None
        Détecte la fin de la partie et la gère.
        '''
        self.boucle.config(text="Partie terminée ! (cliquer sur \"Clear\" pour recommencer)")
        self.btn_ralentir.configure(text='Ralentir',bg='black')
        self.btn_accelerer.configure(text='Accélérer',bg='black')
        self.btn_stop()

    def generation(self,nb):
        '''Vue, int -> None
        Met à jour le numéro de la génération actuelle.
        '''
        self.lbl_generation.config(text="Génération n°"+str(nb))
    
    def ctrl_reinit(self):
        '''Vue -> None
        Réinitialise le jeu et remet à jour la vue.
        '''
        self.btn_start.config(text='Start',command=self.btn_stop)
        self.pause = True
        self.gene = 0
        self.lbl_generation.configure(text="Génération n°0")
        self.boucle.config(text="")
        self.delai = 1500
        self.modele.reinit()
        self.dessine_terrain()

class Controleur:
    '''Créer le lien, au niveau de l’interface graphique, entre le modèle et
    la classe qui gère les dessins et les animations (Vue).
    '''
    def __init__(self,modele):
        '''Controleur, Jeu -> None
        Constructeur du controleur.
        '''
        self.jeu = modele
        self.vue = Vue(self.jeu)
        self.jeu.placeVCelsRandom(int(self.vue.nbaleat))
        self.vue.dessine_terrain()
        self.fenetre = self.vue.fenetre
        self.delai = self.vue.delai
        self.joue()
        self.fenetre.mainloop()

    def affiche_generations(self):
        '''Controleur -> None
        Affiche le numéro de la génération actuelle.
        '''
        self.vue.generation(self.vue.gene)

    def affichage(self):
        '''Controleur -> None
        Met à jour et affiche les données du jeu.
        '''
        if self.jeu.estGrilleVide(): 
            self.vue.gene += 1
            self.affiche_generations()
        else:
            self.vue.boucle.config(text="")
            self.vue.gene += 1
            self.affiche_generations()
        self.delai = self.vue.delai
        self.jeu.etapeSuivante()
        self.vue.dessine_terrain()
        if self.jeu.estGrilleVide(): 
            self.vue.dessine_terrain()
            self.vue.fin_detect()
            self.vue.gene -= 1

    def joue(self):
        '''Controleur -> None
        Fait tourner le jeu.
        '''
        if self.vue.pause == False:
            self.affichage()
        self.fenetre.after(int(self.delai),self.joue)

if __name__ == '__main__':
    vie = Jeu()
    jeu = Controleur(vie)
