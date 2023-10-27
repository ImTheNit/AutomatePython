


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

DEBUGG=1 #1 si on veut debugger, 0 sinon --> different de ARRET

DELIMITER=";"

Dictionnaire={}

TEXTE_DEMANDE_USER="\n-----------------------------\nChoisissez une action parmis:\n-----------------------------\nCharger un automate depuis un fichier .csv(1)\nAfficher un Automate depuis un fichier .csv(2)\nAfficher l'Automate en mémoire(3)\nEnregistrer l'Automate  en mémoire dans un fichier .csv(4)\nEffacer l'Automate en mémoire(5)\nArrêter le programme(0)"
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
    
            
def ModifNomColonne(MonDico):

    for i in range(len(Dictionnaire)):
        MonDico[i]["colonne"]=i
        
    return MonDico
#
#status
#ok
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
        return -1
    else:

        Etat=EtatDico(MonDico)
        Evenement=EvenementDico(MonDico)

        for i in range(len(MonDico)):   #les print aident a comprendre 
            #print("\n")
            for j in range(len(Evenement)):
                #print(Evenement[j])
                if MonDico[i][Evenement[j]] not in Etat :
                    return False                    

        # si on arrive ici --> tous les element sont dans Etat -> AEF
        return True

            
#
#status
#ko
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
        for i in range(1,len(evenement)):
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
            while FichierExiste(NomFichier)==False:
                NomFichier=input("Fichier introuvable, réessayer:")
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
    print(VerifAEF(Dictionnaire))
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

            print("Chargement d'un Automate depuis un Fichier")

            #choix du fichier 
            Fichier=input("Saisissez le nom du fichier:")

            #verif fichier existe
            FichierEntree=choixFichier(1,Fichier)

            Dictionnaire=CSVToDico(FichierEntree)
            if DicoVide(Dictionnaire)==False:
                print("Automate chargé avec succès")
    
            else:
                print("Dictionnaire vide à l'arrivée, un probleme est apparu")
            

        #Affichage Automate depuis .csv    
        case 2:

            print("Affichage d'un Automate depuis un Fichier\n")

            #choix du fichier 
            Fichier=input("Saisissez le nom du fichier:")

            #verif fichier existe
            FichierEntree=choixFichier(1,Fichier)

            AffichageAutomateFromCSV(FichierEntree)
            


        #Affichage de l'Automate en mémoire
        case 3:

            print("Affichage de l'Automate en mémoire\n")
            if DicoVide(Dictionnaire)==True:
                print("Erreur: Aucun Dictionnaire n'est chargé en mémoire")
            else:
                AffichageAutomateFromDico(Dictionnaire)



        #Enregistrer l'automate dans un fichier
        case 4:

            print("Sauvegarde de l'Automate en mémoire vers un fichier")

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
            print("Effacement de l'Automate en mémoire")
            Dictionnaire={}#remplacement par dictionnaire vide
            print("Automate effacé")


        #cas default
        case _:
            print("Choix non valide\n")





#REFLEXION


#saisi d'un automate au terminal
#
#Demander le nombre d'etat
#Demander le nombre d'évènement
#
#pour chaque "case", offrir la possibilité de changer la valeur
#
#


#modif d'un automate
#nouveau MENU
#ajouter element(1),suppr elements(2), modif element(3)

#   OU BIEN

#
#



#De la forme :
#
#
#
#
#
#
#{0: {'colonne': 'a', 'A': 'var1', 'B': 'var2', 'C': 'var3'},
#1: {'colonne': 'b', 'A': 'var4', 'B': 'var5', 'C': 'var6'},
#2: {'colonne': 'c', 'A': 'var7', 'B': 'var8', 'C': 'var9'},
#3: {'colonne': 'd', 'A': '1', 'B': '2', 'C': '3'}}
#
#
#
#
#

#afficher automate ok
#saisir un automate à la main(succesions de input?)ko
#verif AEF(chaque "case est un évènement présent sur la colonne de gauche")


