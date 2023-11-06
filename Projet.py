


#
#
#IMPORT
#
#

import csv #pour gerer les transfert entre python et csv
import os   #pour verifier la taille d'un fichier(verifier s'il est vide)
import time #pour les sleep, temps d'attentes

#
#
#Variables
#Dictionnaires
#
#

#Fichiers et delimiteur par defaut
FichierEntree="data.csv"
FichierSortie="data2.csv"
DELIMITER=";"

ARRET=0 #0 si on veut continuer, 1 sinon

DEBUGG=1 #1 si onveut debugger, 0 sinon --> different de ARRET

Dictionnaire={}

#Type d'état:
#   0-> quelconque
#   1-> initial
#   2-> final
#   3->initial ET final
TYPE=[0,1,2,3]

#Caractères interdit dans les differentes saisies
RESTRICTION_CHOIX_ETAT=[";"," "]

RESTRICTION_CHOIX_EVENEMENT=[";"," "]

RESTRICTION_CHOIX_NOUVEL_ETAT=[";"," "]

#STR contenant les messages de conditions des differentes saisies
CONDITIONS_ETAT="Un Etat ne peut pas contenir "+str(RESTRICTION_CHOIX_ETAT)+" ni être vide"

CONDITIONS_EVENEMENT="Un Evènement ne peut pas contenir "+str(RESTRICTION_CHOIX_EVENEMENT)+" ni être vide"

CONDITIONS_NOUVEL_ETAT="Un Etat ne peut pas contenir "+str(RESTRICTION_CHOIX_ETAT)+" ni être vide.De plus un Etat de destination doit être un état existant"


#Message des choix de mode
TEXTE_DEMANDE_USER="\n-----------------------------\nChoisissez une action parmis:\n-----------------------------\n(1)Charger un automate depuis un fichier .csv\n(2)Afficher un Automate depuis un fichier .csv\n(3)Afficher l'Automate en mémoire\n(4)Enregistrer l'Automate  en mémoire dans un fichier .csv\n(5)Effacer l'Automate en mémoire\n(6)Créer un Automate\n(7)Modifier un Automate en mémoire\n(8)Verifier si un Automate est un Automate d'état fini\n(0)Arrêter le programme"






#
#
#------------------------------------------------------------------------------------------------------------------------------------
#Fonctions
#------------------------------------------------------------------------------------------------------------------------------------
#
#


def AffichageDico(MonDico):

    print("Dictionnaire:")

    for i in range(len(Dictionnaire)):
        print(Dictionnaire[i],"\n")
    return 0
#
#status
#ok
#

def AffichageAutomateFromDico(MonDico):

    if DicoVide(MonDico)== True:
        print("Erreur: le dictionnaire a afficher est vide")     
        return -1

    else:

        print("Affichage sous la forme:\nETAT:évènement-->NouvelEtat\n")
        field=list(FIELDNAMES(MonDico))
        for i in (range(len(Dictionnaire))):

            for j in range(1,len(field)):
                print(Dictionnaire[i][field[0]],":",field[j],"-->",Dictionnaire[i][list(FIELDNAMES(MonDico))[j]])
            print("\n")#pour séparer les affichage de chaque état
        return 0
#
#status
#ok
#

def AffichageAutomateFromCSV(CSVFILES):
    

    #On verifie que le fichier existe bien et qu'il est non-vide
    if FichierExiste(CSVFILES)==True:
        if FichierVide(CSVFILES)==True:

            # On convertit le fichier dans notre dictionnaire puis on affiche le dictionnaire
            Dico=CSVToDico(CSVFILES)
            AffichageAutomateFromDico(Dico)
            return 0
        
        else:
            print("Erreur: le fichier ",CSVFILES," est vide")    
            return -2
            #le fichier est vide

    else:
        print("Erreur: le fichier n'existe pas\n")
        return -1
        #le fichier n'existe pas 
#
#status
#ok
#


def CSVToDico(CSVFILES):

    if FichierExiste(CSVFILES)==False:
        print("Erreur: le fichier n'existe pas\n")
        return -1
        #fichier n'exise pas


    else:

        if FichierVide(CSVFILES)==False:

            with open(CSVFILES) as csvfile:

                reader = csv.DictReader(csvfile,delimiter=DELIMITER)    #On ouvre le fichier en prenant comme delimiteur DELIMITER
                count=0

                for row in reader:                  #La i_ème ligne de notre fichier est placée dans le dictionnaire à l'indice i   //#d'office convertit en dictionnaire
                    Dictionnaire[count]=row
                    count += 1           

            return (Dictionnaire)


        else:
            print("Erreur: le fichier est vide")
            return -2
            #fichier Vide
#
#status
#ok
#

def DicoToCSV(MonDico,CSVFILES):


    #pas besoin de verifier si le fichier existe deja ou s'il est vide: 
    #           -s'il existe deja il sera "remplacé",ie ancien contenu écraser par nouveau
    #           -s'il n'existe pas il sera créé

    if DicoVide(MonDico)==True:
        print("Erreur: le dictionnaire est vide")
        return -1
        #le dictionnaire est vide
    
    
    else:

        with open (CSVFILES,'w',newline="") as csvfiles:
            #on déclare nos varaiables

            fieldnames=FIELDNAMES(MonDico)  #Les champs de notre dictionnaire(ici il s'agit de la premiere ligne de notre fichier:['colonne', 'type', 'A', 'B', 'C', 'D'])
            writer =  csv.DictWriter(csvfiles,fieldnames,delimiter=DELIMITER)

            #ECRITURE
            writer.writeheader()
            for i in range(len(MonDico)):
                writer.writerow(MonDico[i])
        return 0
#
#status
#ok
#

def CreationDico():

    #INITIALISATION VARIABLES ET OBJETS:

    MonDico={}
    
    #Liste des Etats
    Etat=[]
    #Liste des Types associées a ces etat
    Type=[]
    #Liste des Evenements
    Evenement=[]
    
    #Variables permettant de savoir quand on doit arreter de demander une saisie de l'utilisateur
    a=1

    #insertion des états
    while a != 0:

        # On interroge l'utilisateur
        Rep=input("Saisissez un état (0 pour arrêter):")

        if VerifEntier(Rep)==True : #La reponse de l'utilisateur peut etre converti en entier
            if int(Rep)==0:         #L'utilisateur veut arreter la saisie des états
                a=0


            else:

                while VerifSaisieNewEtat(Rep,Etat)==False:  #On verifie que l'etat saisie est conforme aux exigence données

                    print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_ETAT)
                    Rep=input("Nouveau choix:")

                #on initialise Rep2 en dehors de la liste des types imposées pour entré dans le while    
                Rep2=-1
                
                while VerifType(Rep2)==False :  # On boucle tant que la reponse utilisateur n'est pas dans la liste des type fournie

                    Rep2=input("Saisissez le type de l'état "+Rep+" parmis: quelconque(0), initial(1), final(2) ou initial et final(3):")
                    if VerifType(Rep2)==False:
                        print("Le type n'est pas valide")

                #A partir d'ici l'etat et le type saisies sont valides donc on peut les ajouter a leur liste respectives
                Type.append(Rep2)
                Etat.append(Rep)


        else:                       #La reponse ne peut pas etre converti en entier->l'utilisateur veut continuer

            while VerifSaisieNewEtat(Rep,Etat)==False:  #On verifie que l'etat saisie est conforme aux exigence données

                print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_ETAT)
                Rep=input("Nouveau choix:")

            #on initialise Rep2 en dehors de la liste des types imposées pour entré dans le while    
            Rep2=-1
            
            while VerifType(Rep2)==False :  # On boucle tant que la reponse utilisateur n'est pas dans la liste des type fournie

                Rep2=input("Saisissez le type de l'état "+Rep+" parmis: quelconque(0), initial(1), final(2) ou initial et final(3):")
                if VerifType(Rep2)==False:
                    print("Le type n'est pas valide")

            #A partir d'ici l'etat et le type saisies sont valides donc on peut les ajouter a leur liste respectives
            Type.append(Rep2)
            Etat.append(Rep)

    #Affichages pour controler
    print("La liste des états saisies:",Etat)
    print("La liste des type:",Type,"\n")



    # On recommence la saisie de la meme maniere mais pour les évènement cette fois
    a=1

    #insertion des évènement
    while a != 0:

        # On interroge l'utilisateur
        Rep=input("Saisissez un évènement (0 pour arrêter):")

        if VerifEntier(Rep)==True : #La reponse de l'utilisateur peut etre converti en entier
            if int(Rep)==0:         #L'utilisateur veut arreter la saisie des evenements
                a=0

            else:

                while VerifSaisieNewEvenement(Rep,Evenement)==False: #On verifie que l'evenement saisie est conforme aux exigence données

                    print("Le nom de l'évènement ne respecte pas les conditions.\n"+CONDITIONS_EVENEMENT)
                    Rep=input("Nouveau choix:")

                #A partir d'ici l'évenement saisie est conforme donc on peut l'ajouter a sa liste    
                Evenement.append(Rep)


        else:                       #La reponse ne peut pas etre converti en entier->l'utilisateur veut continuer
            
            while VerifSaisieNewEvenement(Rep,Evenement)==False:    #On verifie que l'evenement saisie est conforme aux exigence données

                print("Le nom de l'évènement ne respecte pas les conditions.\n"+CONDITIONS_EVENEMENT)
                Rep=input("Nouveau choix:")

            #A partir d'ici l'évenement saisie est conforme donc on peut l'ajouter a sa liste
            Evenement.append(Rep)


    # Affichage pour controler        
    print("La liste des évènements saisies:",Evenement,"\n")


    #insertion de "l'interieur"
    print("Insertion des états de destination:\nSynthaxe: Etat de Départ:Evenement-->Etat d'arrivée")

    for i in range(len(Etat)):  #   =Pour chaque Etat

        MonDico[i]={}     #générer un indice pour notre dictionnaire pour pouvoir y acceder ensuite (INDISPENSABLE)
        MonDico[i]["colonne"]=Etat[i]
        MonDico[i]["Type"]=Type[i]

        for j in range(len(Evenement)):     #  =Pour chaque evenement

            # Interroge l'utilisateur
            Rep3=input(Etat[i]+":"+Evenement[j]+"-->")

            while VerifSaisieNouvelEtat(Rep3,Etat)==False:  # On verifie que la saisie est conforme
                print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                Rep3=input(Etat[i]+":"+Evenement[j]+"-->")

            # A partir d'ici la saisie est conforme donc on peut l'ecrire dans notre dictionnaire
            MonDico[i][Evenement[j]]=Rep3
            

    return MonDico

#
#status
#OK
#




def FIELDNAMES(MonDico):# on renvoi les clés pour les champs du csv

    if DicoVide(MonDico)==True:
        return -1

    else:
        return(MonDico[0].keys())
        #on supposera que le premier élément de notre dictionnaire possède le maximum de clés 
        #(ie, aucun autre élément n'a de clé que cet élément n'as pas)
#
#status
#ok
#
    
def ModifDico(MonDico):

    DicoFinal={}
    if DicoVide(MonDico)==True:
        print("Erreur: l'automate est vide/inexistant")
        return -1
    else:

        # On recupere la liste des etat et des evenements
        ListeEtat=EtatDico(MonDico)
        ListeEvenement=EvenementDico(MonDico)
        
        #initialisation de nos listes pour archiver 
        AncienneListeEtat=[]
        AncienneListeEvenement=[]

        # On copie le contenue des listes dans des listes d'archives pour comparer
        for i in range(len(ListeEtat)):
            AncienneListeEtat.append(ListeEtat[i])
        
        for i in range(len(ListeEvenement)):
            AncienneListeEvenement.append(ListeEvenement[i])
        
        # On modifie les liste d'etat et d'evenement en fonction des demandes utilisateurs
        modifListeEtat(ListeEtat)
        modifListeEvenement(ListeEvenement)


        #seul les listes des etats/evenment ont été modifiés, pas le dictionnaire

        # Trop compliqué de supprimer les elements de l'ancien dictionnaire car risque d'il y avoir des sauts d'indices ?
        #   ->(Ou alors créer une fonction pour rééquilibrer le dictionnaire(si un indice n'est plus present on le remplace par le suivant)) //recursif
        #       -> FAIT


        # Retirons les etats qui ont été supprimés et reorganisons le dicionnaire

        for i in range(len(AncienneListeEtat)):
            if AncienneListeEtat[i] not in ListeEtat:
                #l'etat etait là avant mais il n'est plus là
                
                # Donc on supprime
                a=MonDico.pop(i)
                print("valeur suppr:",a)



        # Ajoutons les etats qui ont été ajoutés
        print(ListeEtat)
        for i in range (len(ListeEtat)):
            Taille=len(MonDico)
            if ListeEtat[i] not in AncienneListeEtat:
                #l'etat n'etait pas là avant 
                print("Nouvel Etat:",ListeEtat[i],"taille:",Taille)

                # Ajoutons le dans le dictionnaire
                MonDico.setdefault(Taille+1,{'colonne':ListeEtat[i]})


            else:
                #l'etat etait deja là
                print("Ancien Etat:",ListeEtat[i])

        # On verifie que le dictionnaire est trié, si besoin on le trie pour pouvoir l'equilibrer ensuite
        if VerifTrieDico(MonDico)==False:
            MonDico=TrieDicoCle(MonDico)
        
        print("test1:",MonDico)
        MonDico=EquilibrageDico(MonDico)
        print("test2:",MonDico)
        


        return MonDico

#
#Status   
#En cours
#


def EquilibrageDico(MonDico):
    # Retourne -1 si le dictionnaire est vide
    # Retourne le dictionnaire avec les indices réarangés
    
    # On doit s'assurer avant que les clé du dictionnaire sont triées(fonction VerifTrieDico() et TriDicoCle() )

    # Suppr est une liste contenant les indices devant etre supprimés dans notre dictionnaire
    Suppr=[]

    
    if DicoVide(MonDico)==True:
        return -1

    else:
        
        for i in range(len(list(MonDico.keys()))):   # On parcours les etats
            if list(MonDico.keys())[i]!=i:   #verifions si chaque indice de noter dictionnaire est bien nommé correctement sinon le renommé 
                #print("C'est pas OK pour ",i,"car on a ",list(MonDico.keys())[i])

                # On identifie quel indice on devra retirer 
                AncienneValeur=list(MonDico.values())[i]

                # On rajoute une nouvelle clé et on lui assigne la valeur correspondanteattention elle est rajoutée a la fin du diictionnaire
                MonDico.setdefault(i,AncienneValeur)

                #on ajoute l'indice dans la liste des indice a supprimer

                # On ajoute l'indice dans la liste a supprimer seulement si cet indice n'est pas deja attribué
                if i not in Suppr:
                    Suppr.append(list(MonDico.keys())[i])
                


            #else:
                #rien a faire car l'indice est deja correct


        #on supprime les indices superflus:
        for i in range(len(Suppr)):
            #print("On supprime la clé ",Suppr[i])
            a=MonDico.pop(Suppr[i])

    return MonDico
#
#Status
#OK
#


def TrieDicoCle(MonDico):
    # Retourne -1 si le dictionnaire est vide
    # Retourne le dictionnaire trié sinon

    if DicoVide(MonDico):
        return -1
    
    else:
        DicoFinal=sorted(MonDico.items(),key=lambda t:t[0])
        return DicoFinal
#
#Status
#Pas OK
#

def modifListeEtat(ListeEtat):
    
    # Prend en parametre la liste des etat de notre Automate 
    # Retourne la liste modifiée par l'utilisateur

    if len(ListeEtat) == 0:#la liste est de taille 0 --> vide
        print("La liste est vide")
        return -1

    else:
        #print("Liste OK")
        
        #Variable permettant de savoir quand s'arreter
        stop = 0

        while stop == 0:

            # On interroge l'utilisateur
            reponse =input(str(ListeEtat)+"\nVoulez vous modifier la liste des états ci dessus (oui ou non):")

            #On Convertit la chaine en minuscule
            reponse=reponse.lower()

            #On distingue les cas selon la reponse
            match reponse:

                #on veut modifier
                case "oui":

                    print("Modification")
                    Reponse2=input("Taper le nom de l'etat pour le modifier ou le supprimer et taper le nouveau nom pour le rajouter:")

                    #Verification que la reponse est correcte:
                    while VerifSaisieEtat(Reponse2)==False:
                        print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_ETAT)
                        Reponse2=input("Nouveau choix:")

                    #notre champs est désormais conforme 

                    if Reponse2 in ListeEtat:   #l'état choisi est dans la liste

                        Choix=input("Etat sélectionné: "+Reponse2+" Voulez vous le supprimer(0) ou le modifier(1):")

                        #Verification du champ 'Choix'
                        while VerifEntier(Choix)==False or int(Choix) not in [0,1]:
                            print("La réponse attendue est 0 ou 1")
                            Choix=input("Etat sélectionné: "+Reponse2+" Voulez vous le supprimer(0) ou le modifier(1):")

                        if int(Choix)==0:
                            #Suppression
                            ListeEtat.remove(Reponse2)
                        
                        else:
                            #Modification
                            new=input("Saisissez le nouvel Etat:")

                            #verification de la saisie
                            while VerifSaisieNewEtat(new,ListeEtat)==False:
                                print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_ETAT)
                                new=input("Nouveau choix:")


                            ListeEtat=ModifListe(Reponse2,ListeEtat,new)


                    else:
                        #Ajout
                        ListeEtat.append(Reponse2)



                #On ne veut pas/plus modifier
                case "non":

                    print("Fin de modification")
                    #changement de la valeur de la variable stop pour s'arreter
                    stop=1
                

                #Autre reponse
                case _:
                    print("La réponse attendue est oui ou non")

        return ListeEtat
#
#Status
#OK
#


def modifListeEvenement(ListeEvenement):

    # Prend en parametre la liste des evenement de notre Automate
    # Retourne la liste modifiée par l'utilisateur

    if len(ListeEvenement) == 0:#la liste est de taille 0 --> vide
        print("La liste est vide")
        return -1

    else:
        #print("Liste OK")
        
        #Varaiable permettant de savoir quand s'arreter
        stop = 0

        while stop == 0:

            # On interroge l'utilisateur
            reponse =input(str(ListeEvenement)+"\nVoulez vous modifier la liste des évènements ci dessus (oui ou non):")
            
            # On convertit la chaine en minuscule
            reponse=reponse.lower()

            # On distingue les cas selon la reponse 
            match reponse:

                #on veut modifier
                case "oui":

                    print("Modification")
                    Reponse2=input("Taper le nom de l'évènement pour le modifier ou le supprimer et taper le nouveau nom pour le rajouter:")

                    #Verification que la reponse est correcte:
                    while VerifSaisieEvenement(Reponse2)==False:
                        print("Le nom de l'évènement ne respecte pas les conditions.\n"+CONDITIONS_EVENEMENT)
                        Reponse2=input("Nouveau choix:")

                    #notre champs est désormais conforme 

                    if Reponse2 in ListeEvenement:   #l'évènement choisi est dans la liste

                        Choix=input("Evènement sélectionné: "+Reponse2+" Voulez vous le supprimer(0) ou le modifier(1):")

                        #Verification du champ 'Choix'
                        while VerifEntier(Choix)==False or int(Choix) not in [0,1]:
                            print("La réponse attendue est 0 ou 1")
                            Choix=input("Evènement sélectionné: "+Reponse2+" Voulez vous le supprimer(0) ou le modifier(1):")

                        if int(Choix)==0:
                            #Suppression
                            ListeEvenement.remove(Reponse2)
                        
                        else:
                            #Modification
                            new=input("Saisissez le nouvel Evènement:")

                            #verification de la saisie
                            while VerifSaisieNewEvenement(new,ListeEvenement)==False:
                                print("Le nom de l'évènement ne respecte pas les conditions.\n"+CONDITIONS_EVENEMENT)
                                new=input("Nouveau choix:")


                            ListeEvenement=ModifListe(Reponse2,ListeEvenement,new)


                    else:
                        #Ajout
                        ListeEvenement.append(Reponse2)



                #On ne veut pas/plus modifier
                case "non":

                    print("Fin de modification")
                    #changement de la valeur de la variable stop pour s'arreter
                    stop=1
                

                #Autre reponse
                case _:
                    print("La réponse attendue est oui ou non")

        return ListeEvenement
#
#Status
#OK
# 




def ModifListe(ancien,Liste,nouveau):

    # Prend en parametre un liste et deux variable, une deja presente que l'on va remplacer et la nouvelle valeur
    # Retourne la liste modifiée

    if len(Liste)!= 0:      # On verifie que la liste est non vide

        for i in range(len(Liste)): 
            if Liste[i]==ancien:    # On parcours la liste jusqu'à trouver l'indice de la valeur a remplacer
                Liste[i]=nouveau    # On remplace par la nouvelle valeur
                return  Liste 

    else:

        print("Erreur: la liste est vide")
        return -1     
#
#status
#OK
#


def DicoVide(MonDico):
    # Retourne True si le Dictionnaire est vide
    # Retourne False si le Dictionnaire n'est pas vide

    if not MonDico:
        
        return True     #Dictionnaire vide

    else:
        return False    #Dictionnaire non-vide
#
#status
#ok
#


def FichierVide(CSVFILES):
    # Retourne true si le fichier est vide
    # Retourne False si le fichier n'est pas vide
    # Retourne -1 si le fichier n'existe pas

    # On verifie que le fichier existe
    if FichierExiste(CSVFILES)==False:

        print("Erreur: le ficher n'existe pas ")
        return -1
    
    else:
            
        # On s'interesse à la taille de notre fichier
        size=os.stat(CSVFILES).st_size
        if size == 0:
            
            return True     #Fichier Vide

        else:
            return False    #Fichier non-Vide
#
#status
#ok
#


def FichierExiste(CSVFILES):
    # Retourne True si le fichier existe
    # Retourne False si le fichier n'existe pas

    if os.path.exists(CSVFILES):    #on cherche si le chemin du fichier est valide
        return True     #Fichier existe

    else:
        
        return False    #Fichier n'existe pas
#
#status
#ok
#

def VerifType(a):
    # Retourne True si le Type est incorrect
    # Retourne False si le Type est incorrect

    if VerifEntier(a)==True:    #Le type est bien un entier

        if int(a) in TYPE:      #le type est correct         #TYPE est déclarée au debut du fichier

            return True

    return False     #le type est incorrect
#
#status
#ok
#

def VerifEntier(a):
    # Retourne True si le parametre peut etre convertit en entier
    # Retourne False si le parametre ne peut pas etre convertit en entier

    try:    #Essaie de convertir a en entier
        int(a)

    except ValueError:  # Si Erreur lors de la conversion -> a ne peut pas etre convertit en entier
        return False
        #pas un entier

    else:               # Si pas d'erreur --> a peut etre converti en entier
        return True
        #entier
#
#status
#ok
#

def VerifAEF(MonDico):
    # Retourne True si le dictionnaire decrit un AEF
    # Retourne False si le dictionnaire ne decrit pas un AEF

    if DicoVide(MonDico)==True:
        print("L'automate est vide")
        return False

    else:

        #Definition des liste des etats et evenement de notre Automate
        Etat=EtatDico(MonDico)
        Evenement=EvenementDico(MonDico) 
           
        for i in range(len(MonDico)):   # On parcours les etats   
            for j in range(len(Evenement)): #on parcours les evenements 

                if MonDico[i][Evenement[j]] not in Etat and MonDico[i][Evenement[j]]!="":   #on test si une 'case' est deja un etat ou si elle est vide
                    return False                    

        # si on arrive ici --> tous les element sont dans des etats ou alors ils sont vide --> AEF
        return True          
#
#status
#OK
#

def VerifSaisieNewEtat(choix,ListeEtat):#en attente de savoir quels caractères sont interdits
    # Verifie qu'un etat saisie lors du choix de la creation est correct

    # Retourne False si la saisie n'est pas valide
    # Retourne True si la saisie est valide

    if choix == "":    #chaine vide 
        return False

    else:
        if choix in ListeEtat:                                      #on verifie que l'etat n'existe pas déjà   
            print("Cet Etat existe déjà")
            return False

        for i in range(len(RESTRICTION_CHOIX_ETAT)):
            if RESTRICTION_CHOIX_ETAT[i] in choix:                  # on verifie qu'aucun caractère interdit n'est utilisé
                return False

        return True
#
#status
#OK
#


def VerifSaisieEtat(choix):#en attente de savoir quels caractères sont interdits
    # Verifie qu'un etat saisie lors du choix de la modification est correct
    #-> difference avec VerifSaisieNewEtat: on peut choisir un champ qui n'existe pas encore

    # Retourne False si la saisie n'est pas valide
    # Retourne True si la saisie est valide

    if choix == "":    #chaine vide 
        return False

    else:

        for i in range(len(RESTRICTION_CHOIX_ETAT)):
            if RESTRICTION_CHOIX_ETAT[i] in choix:                  # on verifie qu'aucun caractère interdit n'est utilisé
                return False

        return True
#
#status
#OK
#



def VerifSaisieNewEvenement(choix,ListeEvenement):#en attente de savoir quels caractères sont interdits
    # Verifie qu'un évenement saisie lors du choix de la creation est correct

    # Retourne False si la saisie n'est pas valide
    # Retourne True si la saisie est valide

    if choix == "":    #chaine vide 
        return False

    else:
        if choix in ListeEvenement:                                 #on verifie que l'evenement n'existe pas deja  
            print("Cet Evenement existe déjà")                      
            return False

        for i in range(len(RESTRICTION_CHOIX_EVENEMENT)):       
            if RESTRICTION_CHOIX_EVENEMENT[i] in choix:             # on verifie qu'aucun caractère interdit n'est utilisé
                return False

        return True
#
#status
#OK
#


def VerifSaisieEvenement(choix):#en attente de savoir quels caractères sont interdits
    # Verifie qu'un évenement saisie lors du choix de la modification est correct
    #-> difference avec VerifSaisieNewEvenement: on peut choisir un champ qui n'existe pas encore

    # Retourne False si la saisie n'est pas valide
    # Retourne True si la saisie est valide

    if choix == "":    #chaine vide 
        return False

    else:

        for i in range(len(RESTRICTION_CHOIX_EVENEMENT)):       
            if RESTRICTION_CHOIX_EVENEMENT[i] in choix:             # on verifie qu'aucun caractère interdit n'est utilisé
                return False

        return True
#
#status
#OK
#


def VerifSaisieNouvelEtat(choix,ListeEtat):#en attente de savoir quels caractères sont interdits
    #Verifie qu'un etat de "destination" saisie lors de la creation est correct

    # Retourne False si la saisie n'est pas valide
    # Retourne True si la saisie est valide

    if choix == "":    #chaine vide 
        return True

    else:

        for i in range(len(RESTRICTION_CHOIX_NOUVEL_ETAT)):       
            if RESTRICTION_CHOIX_NOUVEL_ETAT[i] in choix:             # on verifie qu'aucun caractère interdit n'est utilisé
                return False

        if choix in ListeEtat:                           # le nouvel etat existe bien deja 
            return True

        else:                                               #le nouvel etat n'existe pas deja
            return False
    
    return False

#
#status
#OK
#

def VerifTrieDico(MonDico):
    # Retourne True si les clées sont triées
    # Retourne False si les clées ne sont pas triées
    # Retourne -1 si les clées du dictionnaire sont triées

    if DicoVide(MonDico):
        return -1

    else:

        # On manipule la liste des clés de notre dictionnaire
        maListe=list(MonDico.keys())

        # On Definit la version triée de cette liste
        ListeTriee=sorted(maListe)
        
        
        #print("New:",ListeTriee)
        #print("Old:",maListe)
        
        # On compare les deuxpour savoir si la liste initiale bien triée
        if maListe==ListeTriee: 
            return True

        else:
            return False
#
#Status
#OK
#


def EtatDico(MonDico):
    # Retourne une liste contenant l'ensemble des etat de l'AEF -> colonne de gauche(sauf premiere ligne)

    if DicoVide(MonDico)==True:
        print("l'automate est vide")
        return -1


    else:
        etat=[]
        for i in range(len(MonDico)):
            etat.append(MonDico[i][list(FIELDNAMES(MonDico))[0]])
        return(etat)
#
#status
#ok
#     

def EvenementDico(MonDico):
    # Retourne la liste contenant l'ensemble des evenement de l'AEF -> premiere ligne(sauf premiere colonne)

    if DicoVide(MonDico)==True:
        print("l'automate est vide")
        return -1


    else:
        evenement=list(MonDico[0].keys()) # la premiere ligne, il faut retirer la premiere valeur de la liste
        Evenement=[]
        for i in range(2,len(evenement)):   #on commence à deux pour ne pas ajouter  "colonne" ni "type"
            Evenement.append(evenement[i])
        return Evenement
#
#status
#ok
#  



def DemandeUser():
    # Retourne le choix de l'utilisateur qui doit impérativement etre un entier

    # On inerroge l'utilisateur
    print(TEXTE_DEMANDE_USER)
    A=input("Votre Choix:")

    while VerifEntier(A)==False:    # Tant que l réponse n'est pas un entier on boucle sur la question
        print("La réponse attendu doit être un entier")
        print(TEXTE_DEMANDE_USER)
        A=input("Votre Choix:")
    return int(A)

#
#status
#ok
#

def choixFichier(mode,NomFichier): 
    # verif fichier entrée : mode=1
    # verif fichier sortie : mode=2

    # Retourne le nom du fichier saisie
    # Retourne -1 si la fonction est mal appelée(valeur de a anormale)

    #pas besoin de verifier si on 'peut' convertir mode en entier car il n'est pas saisie par l'utilisateur
    match int(mode):
        
        #Mode Choix fichier d'entrée
        case 1:
            
            #on verifie que le fichier existe est qu'il n'est pas vide
            while FichierExiste(NomFichier)==False or FichierVide(NomFichier)==True:        
                NomFichier=input("Fichier vide ou introuvable, réessayer:")
            print("Fichier OK")
            return NomFichier


        #Mode Choix fichier de sortie
        case 2:

            if FichierExiste(NomFichier)==False:#Le fichier n'existe pas 
                print("Aucun fichier correspondant, création d'un nouveau fichier")
                    #Pour Créer un fichier en python, on l'ouvre en mode ecriture(et cela sera fait lors de l'ecriture)

            else:   #Le fichier existe déjà
                print("Fichier OK")
            return NomFichier

        case _:
            print("Erreur dans l'appel de choixFichier()")
            return -1
            #erreur appel de choixFichier()
#
#status
#ok
#

#COCOZONE


def VerifComplet(Dico):#return TRUE if the automate if complete, FALSE else
    for i in range(len(Dico)):
        b=0

#END OF COCOZONE


#
#
#---------------------------------------------------------------------------------------------------------------------------------------------
#PROGRAMME
#---------------------------------------------------------------------------------------------------------------------------------------------
#
#
if DEBUGG != 1:

    print("\n-------------------------\nGestionnaire D'Automate\n-------------------------")

#
#------------------------------------
#---------------DEBUGG---------------
#------------------------------------
#

if DEBUGG == 1:
    print("------------------------------------")
    print("---------------DEBUGG---------------")
    print("------------------------------------")

#-------------------------------


    Dictionnaire=CSVToDico(FichierEntree)
    #Dictionnaire={
     #   0:{"colonne":"q0",'type'},
      #  1:{'colonne':'q1'},
       # 2:{'colonne':'q2'},
        #3:{'colonne':'q3'},
        #4:{'colonne':'q4'}
    #}
    Dictionnaire={
        0: {'colonne': 'q1', 'type': '0', 'A': 'q3', 'B': 'q0', 'C': 'q1', 'D': 'q2'}, 
        3: {'colonne': 'q2', 'type': '0', 'A': 'q2', 'B': 'q3', 'C': 'q0', 'D': 'q1'}, 
        2: {'colonne': 'q3', 'type': '0', 'A': 'q1', 'B': 'q2', 'C': 'q3', 'D': 'q0'}
        }
    #print(VerifTrieDico(Dictionnaire))
    #Dictionnaire=TrieDicoCle(Dictionnaire)
    #print(Dictionnaire)
    #print(VerifTrieDico(Dictionnaire))
    
    
    
    
    #ModifDico(Dictionnaire)
    #print(Dictionnaire)

    ARRET = 1

#
#------------------------------------
#------------------------------------
#------------------------------------
#

while ARRET == 0 :
    
    ChoixUser=DemandeUser()

    match ChoixUser:
        
        #Arret
        case 0:

            print("Fin du programme\n")
            ARRET=1

        #chargement automate depuis .csv
        case 1:

            print("\nChargement d'un Automate depuis un Fichier\n")

            #choix du fichier 
            Fichier=input("Saisissez le nom du fichier:")

            #verif fichier existe
            FichierEntree=choixFichier(1,Fichier)

            Dictionnaire=CSVToDico(FichierEntree)
            if DicoVide(Dictionnaire)==False:
                print("Automate chargé avec succès")
    
            else:
                print("Automate vide à l'arrivée, un probleme est apparu")
            

        #Affichage Automate depuis .csv    
        case 2:

            print("\nAffichage d'un Automate depuis un Fichier\n")

            #choix du fichier 
            Fichier=input("Saisissez le nom du fichier:")

            #verif fichier existe
            FichierEntree=choixFichier(1,Fichier)

            AffichageAutomateFromCSV(FichierEntree)
            


        #Affichage de l'Automate en mémoire
        case 3:

            print("\nAffichage de l'Automate en mémoire\n")
            if DicoVide(Dictionnaire)==True:
                print("Erreur: Aucun Automate n'est chargé en mémoire")
            else:
                AffichageAutomateFromDico(Dictionnaire)



        #Enregistrer l'automate dans un fichier
        case 4:

            print("\nSauvegarde de l'Automate en mémoire vers un fichier\n")

            if DicoVide(Dictionnaire)==True:
                print("Erreur: Aucun Dictionnaire n'est chargé en mémoire")

            else:
                #choix du fichier de destination
                Fichier=input("Saisissez le nom du fichier:")

                #verif fichier existe
                FichierSortie=choixFichier(2,Fichier)
            
            #confirmation si non vide ?
                if DicoToCSV(Dictionnaire,FichierSortie) == 0:
                    print("Sauvegarde réussie")
                else:
                    print("Erreur lors de la sauvegarde")

        #Effacer Automate en memoire
        case 5:

            print("\nEffacement de l'Automate en mémoire\n")
            Dictionnaire={}#remplacement par dictionnaire vide
            print("Automate effacé")


        #Créer un nouvel automate
        case 6:
            print("\nCréation d'un nouvel Automate\n")
            Dictionnaire=CreationDico()
            if VerifAEF(Dictionnaire)==False:
                print("Erreur lors de la création")
            else:
                print("Création de l'automate avec succès")
                AffichageAutomateFromDico(Dictionnaire)


        #Modifier un Automate
        case 7:

            print("\nModification d'un Automate\n")

            if DicoVide(Dictionnaire)==True:
                print("Aucun Automate en mémoire")
            else:
                ModifDico(Dictionnaire)


        #verifier si un Automate est un AEF en mémoire uniquement (l'ordre peut changer)
        case 8:

            print("\nVerification AEF\n")

            if DicoVide(Dictionnaire)==True:    #il n'y a pas d'Automate en memoire
                print("Aucun Automate n'est enregisé en mémoire")
            else:       #un automate a bien été trouvé
                match VerifAEF(Dictionnaire):
            
                    #L'automate est un AEF
                    case True:
                        print("L'automate est un Automate d'état fini")
                    
                    #L'automate n'est pas un AEF
                    case False:
                        print("L'automate n'est pas un Automate d'état fini")

                    #Cas défaut
                    case _: 
                        print("Erreur: probleme lors de la verification de l'automate")
                    
                    


        #cas default
        case _:
            print("Choix non valide\n")








#Dictionnaire de la forme :
#
#
#
#
#{
#0: {'colonne': 'a', 'A': 'a,b', 'B': 'c', 'C': 'd'},
#1: {'colonne': 'b', 'A': 'a', 'B': 'c', 'C': 'c'},
#2: {'colonne': 'c', 'A': 'a', 'B': 'c', 'C': 'c'},
#3: {'colonne': 'd', 'A': 'a', 'B': 'b', 'C': 'd'}
#}
#
#
#
#

#Fichier CSV de la forme:
#
#
#
#
#colonne;type;A;B;C;D
#a;0;a;a;a;a
#b;0;a;a;b;a
#c;0;a;a;b;d
#d;0;a;a;d;c
#
#
#
#



#afficher automate(depuis fichier ou mémoire)
#->OK

#Récupération de l'Automate depuis un fichier
#->OK

#Sauvegarde de l'Automate vers un fichier
#->OK

#etablir automate de la bonne forme(ajout colonne pour nom et pour type(initial,final))
#   |-> pas besoin de faire une colonne pour le nom
#   |-> Si on veut modifier les colonnes a prendre en compte, voir la fonction EvenementDico()
#->OK
                #   Proposition de format pour le type:
                #   0-> quelconque
                #   1-> initial
                #   2-> final
                #   3->initial ET final



#verif AEF(chaque "case" est un évènement présent sur la colonne de gauche--> tout nouvel etat est un etat existant)
        #test pour etre sur qu'on a pas de problème
#->OK


#Verif le contenu du fichier est correct
#->nom des deux premieres case(colonne et type)
#->La premmiere ligne doit avoir tout les champs possible(ie aucune valeur dans la 6e colonne et + si la premiere ligne s'arrete a la 5e )
#->??
#pas OK


#saisir un automate à la main
#On demande les etats puis les evenements et enfin les nouveaux etats
#->OK


#Modif d'un Automate a la main
#affichage des etats, modifié cette liste-->ok
#affichage des evenements-->ok
#-->comment modifier le dictionnaire après?
#pour chaque etat de destination: proposer un changement(si pas de changement on garde l'ancien)--> on affichera bien sur la valeur actuelle




#Fonctions pour verifier qu'une saisie est correcte(Etat/Evenement/NouvelEtat)

#Etat:
#   pas vide
#   n'existe pas déjà
#   carac interdit " ", ";"
#   ???

#Evenement:
#   pas vide
#   n'existe pas déjà
#   carac interdit " ", ";"
#   ???

#Nouvel Etat:
#   pas vide
#   carac interdit " ", ";"
#   Existe dans les etats
#   cas où plusieurs etats d'arrivée???
#   ???





#REFLEXION:

#CAS d'un AEF non-deterministe:(deux etat possible avec le meme évènement/transition)
# Comment on l'ecrit dans le fichier?
#   -> ";" va poser des probleme pour lire le fichier