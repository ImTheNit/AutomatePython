


#
#
#IMPORT
#
#

import csv #pour gerer les ransfert entre python et csv
import os   #pour verifier la taille d'un fichier(verifier s'il est vide)
import time #pour les sleep, temps d'attentes

#
#
#Variables
#Dictionnaires
#
#

FichierEntree="data.csv"
FichierSortie="data2.csv"

ARRET=0 #0 si on veut continuer, 1 sinon

DEBUGG=0 #1 si onveut debugger, 0 sinon --> different de ARRET

DELIMITER=";"

Dictionnaire={}

TYPE=[0,1,2,3]

RESTRICTION_CHOIX_ETAT=[";"," "]

RESTRICTION_CHOIX_EVENEMENT=[";"," "]

RESTRICTION_CHOIX_NOUVEL_ETAT=[";"," "]

CONDITIONS_ETAT="Un Etat ne peut pas contenir "+str(RESTRICTION_CHOIX_ETAT)+" ni être vide"

CONDITIONS_EVENEMENT="Un Evènement ne peut pas contenir "+str(RESTRICTION_CHOIX_EVENEMENT)+" ni être vide"

CONDITIONS_NOUVEL_ETAT="Un Etat ne peut pas contenir "+str(RESTRICTION_CHOIX_ETAT)+" ni être vide.De plus un Etat de destination doit être un état existant"


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

    if FichierExiste(CSVFILES)==True:
        Dico=CSVToDico(CSVFILES)
        AffichageAutomateFromDico(Dico)
        return 0

    else:
        print("Erreur: le fichier n'existe pas\n")
        return -1
        #le fichier est vide
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
                reader = csv.DictReader(csvfile,delimiter=DELIMITER)
                count=0
                for row in reader:
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
    #           -s'il existe deja il sera "remplacer",ie ancien contenu écraser par nouveau
    #           -s'il n'existe pas il sera créé

    if DicoVide(MonDico)==True:
        print("Erreur: le dictionnaire est vide")
        return -1
        #le dictionnaire est vide
    
    
    else:

        with open (CSVFILES,'w',newline="") as csvfiles:
            #on déclare nos varaiables
            fieldnames=FIELDNAMES(MonDico)
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
    MonDico={}
    Etat=[]
    Type=[]
    Evenement=[]
    a=1

    #insertion des états
    while a != 0:
        Rep=input("Saisissez un état (0 pour arrêter):")
        if VerifEntier(Rep)==True : #La reponse de l'utilisateur peut etre converti en entier
            if int(Rep)==0:         #L'utilisateur veut arreter la saisie des états
                a=0
            else:
                while VerifSaisieNewEtat(Rep,Etat)==False:
                    print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_ETAT)
                    Rep=input("Nouveau choix:")
                Rep2=-1
                while VerifType(Rep2)==False :
                    Rep2=input("Saisissez le type de l'état "+Rep+" parmis: quelconque(0), initial(1), final(2) ou initial et final(3):")
                    if VerifType(Rep2)==False:
                        print("Le type n'est pas valide")
                Type.append(Rep2)
                Etat.append(Rep)
        else:                       #La reponse ne peut pas etre converti en entier->l'utilisateur veut continuer
            while VerifSaisieNewEtat(Rep,Etat)==False:
                print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_ETAT)
                Rep=input("Nouveau choix:")
            Rep2=-1
            while VerifType(Rep2)==False :
                Rep2=input("Saisissez le type de l'état "+Rep+" parmis: quelconque(0), initial(1), final(2) ou initial et final(3):")
                if VerifType(Rep2)==False:
                    print("Le type n'est pas valide")
            Type.append(Rep2)
            Etat.append(Rep)

    print("La liste des états saisies:",Etat)
    print("La liste des type:",Type,"\n")

    a=1

    #insertion des évènement
    while a != 0:
        Rep=input("Saisissez un évènement (0 pour arrêter):")
        if VerifEntier(Rep)==True : #La reponse de l'utilisateur peut etre converti en entier
            if int(Rep)==0:         #L'utilisateur veut arreter la saisie des evenements
                a=0
        else:                       #La reponse ne peut pas etre converti en entier->l'utilisateur veut continuer
            while VerifSaisieNewEvenement(Rep,Evenement)==False:
                print("Le nom de l'évènement ne respecte pas les conditions.\n"+CONDITIONS_EVENEMENT)
                Rep=input("Nouveau choix:")
            Evenement.append(Rep)
    print("La liste des évènements saisies:",Evenement,"\n")


    #insertion de "l'interieur"
    print("Insertion des états de destination:\nSynthaxe: Etat de Départ:Evenement-->Etat d'arrivée")

    for i in range(len(Etat)):
        MonDico[i]={}     #générer un indice pour notre dictionnaire pour pouvoir y acceder ensuite (INDISPENSABLE)
        MonDico[i]["colonne"]=Etat[i]
        MonDico[i]["Type"]=Type[i]

        for j in range(len(Evenement)):
            Rep3=input(Etat[i]+":"+Evenement[j]+"-->")
            while VerifSaisieNouvelEtat(Rep3,Etat)==False:
                print("Le nom de l'état ne respecte pas les conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                Rep3=input(Etat[i]+":"+Evenement[j]+"-->")

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
    if DicoVide(MonDico)==True:
        print("Erreur: l'automate est vide/inexistant")
        return -1
    else:
        ListeEtat=EtatDico(MonDico)
        ListeEvenement=EvenementDico(MonDico)

        NewListeEtat=modifListeEtat(ListeEtat)
        NewListeEvenement=modifListeEvenement(ListeEvenement)

        #seul les listes des etats/evenment ont été modifiés, pas le dictionnaire
        #AffichageAutomateFromDico(MonDico)
        return MonDico

#
#Status   
#En cours
#




def modifListeEtat(ListeEtat):

    if len(ListeEtat) == 0:#la liste est de taille 0 --> vide
        print("La liste est vide")
        return -1
    else:
        #print("Liste OK")
        
        stop = 0
        while stop == 0:
            reponse =input(str(ListeEtat)+"\nVoulez vous modifier la liste des états ci dessus (oui ou non):")
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

    if len(ListeEvenement) == 0:#la liste est de taille 0 --> vide
        print("La liste est vide")
        return -1
    else:
        #print("Liste OK")
        
        stop = 0
        while stop == 0:
            reponse =input(str(ListeEvenement)+"\nVoulez vous modifier la liste des évènements ci dessus (oui ou non):")
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
    if len(Liste)!= 0:
        for i in range(len(Liste)):
            if Liste[i]==ancien:
                Liste[i]=nouveau
                return  Liste      
#
#status
#OK
#


def DicoVide(MonDico):

    if not MonDico:
        
        return True     #Dictionnaire vide

    else:
        return False    #Dictionnaire non-vide
#
#status
#ok
#


def FichierVide(CSVFILES):

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

    if os.path.exists(CSVFILES):
        return True     #Fichier existe

    else:
        
        return False    #Fichier n'existe pas
#
#status
#ok
#

def VerifType(a):


    #TYPE est un variable global déclarée plus haut

    if VerifEntier(a)==True:    #Le type est bien un entier

        if int(a) in TYPE:      #le type est correct         #TYPE est déclarer au debut du fichier

            return True

    return False     #le type est incorrect
#
#status
#ok
#

def VerifEntier(a):

    try:
        int(a)
    except ValueError:
        return False
        #pas un entier
    else:
        return True
        #entier
#
#status
#ok
#

def VerifAEF(MonDico):
    if DicoVide(MonDico)==True:
        print("L'automate est vide")
        return False
    else:

        Etat=EtatDico(MonDico)
        Evenement=EvenementDico(MonDico)    
        #les print aident a comprendre 
        for i in range(len(MonDico)):   
            #print("\n")
            for j in range(len(Evenement)): #on parcours le dictionnaire 
                #print(Evenement[j])
                if MonDico[i][Evenement[j]] not in Etat and MonDico[i][Evenement[j]]!="":   #on test si une 'case' est deja un etat ou si elle est vide
                    return False                    

        # si on arrive ici --> tous les element sont dans des etats ou alors ils sont vide --> AEF
        return True

            
#
#status
#OK
#

def VerifSaisieNewEtat(choix,ListeEtat):#en attente de savoir quels caractères sont interdits
    
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
    #pour les états de "destination"
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


def EtatDico(MonDico):

    #Retourne une liste contenant l'ensemble des etat de l'AEF -> colonne de gauche(sauf premiere ligne)
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

    #retourne la liste contenant l'ensemble des evenement de l'AEF -> premiere ligne(sauf premiere colonne)
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


    print(TEXTE_DEMANDE_USER)
    A=input("Votre Choix:")
    while VerifEntier(A)==False:
        print("La réponse attendu doit être un entier")
        print(TEXTE_DEMANDE_USER)
        A=input("Votre Choix:")
    return int(A)

#
#status
#ok
#

def choixFichier(a,NomFichier): 
    # verif fichier entrée : a=1
    # verif fichier sortie : a=2

    match int(a):
        
        #Mode Choix fichier d'entrée
        case 1:
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
            print("appel de choixFichier()")
            return -1
            #erreur appel de choixFichier()
#
#status
#ok
#


#
#
#---------------------------------------------------------------------------------------------------------------------------------------------
#PROGRAMME
#---------------------------------------------------------------------------------------------------------------------------------------------
#
#



if DEBUGG == 1:
    Dictionnaire=CSVToDico(FichierEntree)

    ModifDico(Dictionnaire)
    ARRET = 1


print("\n-------------------------\nGestionnaire D'Automate\n-------------------------")
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
#0: {'colonne': 'a', 'A': 'var1', 'B': 'var2', 'C': 'var3'},
#1: {'colonne': 'b', 'A': 'var4', 'B': 'var5', 'C': 'var6'},
#2: {'colonne': 'c', 'A': 'var7', 'B': 'var8', 'C': 'var9'},
#3: {'colonne': 'd', 'A': '1', 'B': '2', 'C': '3'}
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
