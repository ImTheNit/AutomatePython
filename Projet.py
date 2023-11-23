


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
CONDITIONS_ETAT="A state can't contain "+str(RESTRICTION_CHOIX_ETAT)+"and be empty"

CONDITIONS_EVENEMENT="An event can't contain "+str(RESTRICTION_CHOIX_EVENEMENT)+"and be empty"

CONDITIONS_NOUVEL_ETAT="A state can't contain "+str(RESTRICTION_CHOIX_ETAT)+",be empty and the destination state must exist"


#Message des choix de mode
TEXTE_DEMANDE_USER="\n-----------------------------\nChoose an action:\n-----------------------------\n(1)Load an automaton from a .csv file\n(2)Display the automaton from a .csv file\n(3)Display the automaton in memory\n(4)Register the automaton in memory in a .csv file\n(5)Erase the automaton in memory\n(6)Create an automaton\n(7)Modify the automaton in memory\n(8)Verify if the automaton is a final state machine\n(9)Verify that the automaton is complete\n(10)Complete the automaton\n(0)Arrêter le programme"



#
#
#------------------------------------------------------------------------------------------------------------------------------------
#Fonctions
#------------------------------------------------------------------------------------------------------------------------------------
#
#

def wait(a=0.8):
    time.sleep(a)
    return 0
#
#Status
#OK
#


def AffichageDico(MonDico):

    print("Dictionnary:")

    for i in range(len(MonDico)):
        print(MonDico[i],"\n")
    return 0
#
#status
#ok
#

def AffichageAutomateFromDico(MonDico):

    if DicoVide(MonDico)== True:
        print("Error: the dictionnary to print is empty")     
        return -1

    else:

        print("Affichage sous la forme:\nETAT:évènement-->NouvelEtat\n")
        field=list(FIELDNAMES(MonDico))
        for i in (range(len(MonDico))):

            for j in range(1,len(field)):
                print(MonDico[i][field[0]],":",field[j],"-->",MonDico[i][list(FIELDNAMES(MonDico))[j]])
            print("\n")#pour séparer les affichage de chaque état
            wait()
        return 0
#
#status
#ok
#

def AffichageAutomateFromCSV(CSVFILES):
    

    #On verifie que le fichier existe bien et qu'il est non-vide
    if FichierExiste(CSVFILES)==True:
        if FichierVide(CSVFILES)==False:

            # On convertit le fichier dans notre dictionnaire puis on affiche le dictionnaire
            Dico=CSVToDico(CSVFILES)
            AffichageAutomateFromDico(Dico)
            return 0
        
        else:
            print("Error: the file ",CSVFILES," is empty")    
            return -2
            #le fichier est vide

    else:
        print("Error: the file do not exist\n")
        return -1
        #le fichier n'existe pas 
#
#status
#ok
#


def CSVToDico(CSVFILES):
    Dictionnaire={}
    if FichierExiste(CSVFILES)==False:
        print("Error: the file do not exist\n")
        return -1
        #fichier n'exise pas


    else:

        if FichierVide(CSVFILES)==False:

            with open(CSVFILES) as csvfile:

                reader = csv.DictReader(csvfile,delimiter=DELIMITER)    #On ouvre le fichier en prenant comme delimiteur DELIMITER
                count=0

                for row in reader:                  #La i_ème ligne de notre fichier est placée dans le dictionnaire à l'indice i   //#d'office convertit en dictionnaire
                    Dictionnaire[count]=row
                    


                    # We want the programm to convert a multiple choice of state in the csv file into a list of state (separator of state in the file: ",")
                    
                    for i in range(len(EvenementDico(Dictionnaire))):
                        Value=ListState(row[list(EvenementDico(Dictionnaire))[i]])
                        row[list(EvenementDico(Dictionnaire))[i]]=ClearState(Value)
   
                    count += 1           

            return (Dictionnaire)


        else:
            print("Error: the file is empty")
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
        print("Error: the dictionnary is empty")
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

    #insertion des étatse
    while a != 0:

        # On interroge l'utilisateur
        Rep=input("Input a state (0 to stop):")

        if VerifEntier(Rep)==True : #La reponse de l'utilisateur peut etre converti en entier
            if int(Rep)==0:         #L'utilisateur veut arreter la saisie des états
                a=0


            else:

                while VerifSaisieNewEtat(Rep,Etat)==False:  #On verifie que l'etat saisie est conforme aux exigence données

                    print("The name of the new state do not respect the conditions.\n"+CONDITIONS_ETAT)
                    Rep=input("New choice:")

                #on initialise Rep2 en dehors de la liste des types imposées pour entré dans le while    
                Rep2=-1
                
                while VerifType(Rep2)==False :  # On boucle tant que la reponse utilisateur n'est pas dans la liste des type fournie

                    Rep2=input("Input the type of the state"+Rep+" among: ordinary(0), initial(1), final(2) or   initial and final(3):")
                    if VerifType(Rep2)==False:
                        print("The type is not correct")

                #A partir d'ici l'etat et le type saisies sont valides donc on peut les ajouter a leur liste respectives
                Type.append(Rep2)
                Etat.append(Rep)


        else:                       #La reponse ne peut pas etre converti en entier->l'utilisateur veut continuer

            while VerifSaisieNewEtat(Rep,Etat)==False:  #On verifie que l'etat saisie est conforme aux exigence données

                print("The name of the new state do not respect the conditions.\n"+CONDITIONS_ETAT)
                Rep=input("New choice:")

            #on initialise Rep2 en dehors de la liste des types imposées pour entré dans le while    
            Rep2=-1
            
            while VerifType(Rep2)==False :  # On boucle tant que la reponse utilisateur n'est pas dans la liste des type fournie

                Rep2=input("Input the type of the state "+Rep+" among: ordinary(0), initial(1), final(2) or   initial and final(3):")
                if VerifType(Rep2)==False:
                    print("The type is not correct")

            #A partir d'ici l'etat et le type saisies sont valides donc on peut les ajouter a leur liste respectives
            Type.append(Rep2)
            Etat.append(Rep)

    #Affichages pour controler
    print("The list of input's states:",Etat)
    print("The list of input's state's type:",Type,"\n")
    wait(0.4)


    # On recommence la saisie de la meme maniere mais pour les évènement cette fois
    a=1

    #insertion des évènement
    while a != 0:

        # On interroge l'utilisateur
        Rep=input("Input an event (0 to stop):")

        if VerifEntier(Rep)==True : #La reponse de l'utilisateur peut etre converti en entier
            if int(Rep)==0:         #L'utilisateur veut arreter la saisie des evenements
                a=0

            else:

                while VerifSaisieNewEvenement(Rep,Evenement)==False: #On verifie que l'evenement saisie est conforme aux exigence données

                    print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                    Rep=input("New choice:")

                #A partir d'ici l'évenement saisie est conforme donc on peut l'ajouter a sa liste    
                Evenement.append(Rep)


        else:                       #La reponse ne peut pas etre converti en entier->l'utilisateur veut continuer
            
            while VerifSaisieNewEvenement(Rep,Evenement)==False:    #On verifie que l'evenement saisie est conforme aux exigence données

                print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                Rep=input("New choice:")

            #A partir d'ici l'évenement saisie est conforme donc on peut l'ajouter a sa liste
            Evenement.append(Rep)


    # Affichage pour controler        
    print("The list of input's events:",Evenement,"\n")
    wait(0.4)


    #insertion de "l'interieur"
    print("Inserting destination's states:\nSynthax: State:Event-->destination's state")

    for i in range(len(Etat)):  #   =Pour chaque Etat

        MonDico[i]={}     #générer un indice pour notre dictionnaire pour pouvoir y acceder ensuite (INDISPENSABLE)
        MonDico[i]["colonne"]=Etat[i]
        MonDico[i]["Type"]=Type[i]

        for j in range(len(Evenement)):     #  =Pour chaque evenement
            check=0
            while check == 0:

                # Interroge l'utilisateur
                Rep3=input(Etat[i]+":"+Evenement[j]+"-->")

                # Convert the answer into a list if two or more states
                Rep3=ListState(Rep3)
                Rep3=ClearState(Rep3)
                if type(Rep3)==str:
                    if VerifSaisieNouvelEtat(Rep3,Etat)==False:  # On verifie que la saisie est conforme
                        print(Rep3,": the name of the state do not respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                    else:
                        check=2


                if type(Rep3)==list:
                    # We have to check if each member of the list is ok
                    check=1
                    print("\n")
                    wait()
                    for k in range(len(Rep3)):

                        if VerifSaisieNouvelEtat(Rep3[k],Etat)==False and check==1:
                            print(Rep3[k],": the name of the state do not respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                            check=0
                            break

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

    if DicoVide(MonDico)==True:
        print("Error: the file do not exist or is empty")
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
        
        print("Removing unwanted files")
        wait()
        for i in range(len(AncienneListeEtat)):
            if AncienneListeEtat[i] not in ListeEtat:
                #l'etat etait là avant mais il n'est plus là
                
                # Donc on supprime
                a=MonDico.pop(i)
                #print("valeur suppr:",a)


        # Ajoutons les etats qui ont été ajoutés

        print("Adding new states")
        wait()


        for i in range (len(ListeEtat)):
            Taille=len(MonDico)
            if ListeEtat[i] not in AncienneListeEtat:
                #l'etat n'etait pas là avant 
                #print("Nouvel Etat:",ListeEtat[i],"taille:",Taille)

                # Ajoutons le dans le dictionnaire
                MonDico.setdefault(Taille+1,{'colonne':ListeEtat[i]})


            else:
                a=1 #bidon
                #l'etat etait deja là
                #print("Ancien Etat:",ListeEtat[i])
        
        # On verifie que le dictionnaire est trié, si besoin on le trie pour pouvoir l'equilibrer ensuite
        if VerifTrieDico(MonDico)==False:
            MonDico=TrieDicoCle(MonDico)
        
        #On reorganise notre Dictionnaire pour que les indices soient successifs
        MonDico=ConvertIndiceDico(MonDico)


        #On retire maintenant les évenement que l'utilisateur ne veut plus garder

        print("Removing unwanted events")
        wait()

        for i in range(len(AncienneListeEvenement)):
            if AncienneListeEvenement[i] not in ListeEvenement:
                #print("Ancienne valeur:",AncienneListeEvenement[i])
                #l'evennement etait là avant mais il n'est plus là
                for j in range(len(MonDico)):
                        a=MonDico[j].pop(AncienneListeEvenement[i])
                        #print("valeur suppr:",a)
                # Donc on supprimme
        #print(MonDico)

        # On rajoute les evennements qui ont été rajoutés

        print("Adding new events")
        wait()

        for i in range(len(ListeEvenement)):
            #Taille=len(ListeEvenement)
            if ListeEvenement[i] not in AncienneListeEvenement:
                #L'evenement n'etait pas là avant
                #print("Nouvel Evenement:",ListeEvenement[i])

                # On ajoute dans le dictionnaire pour chaque etat
                for j in range(len(MonDico)):
                    MonDico[j][ListeEvenement[i]]=""
        #print(MonDico)

        # On Affiche maintenant l'automate pas à pas et demandant les nouvelles valeurs

        print("New fields in the automaton")
        print("State:Event-> destination's state")

        for i in range(len(MonDico)):
            field=list(FIELDNAMES(MonDico))
            
            
            # Modification du Type
            print(MonDico[i][field[0]],":",field[1],"-->",MonDico[i][list(FIELDNAMES(MonDico))[1]])
            rep=input("Input the type of the state "+MonDico[i][field[0]]+" among: ordinary(0), initial(1), final(2) or    initial and final(3) (Enter to skip):")

            while VerifType(rep)==False and rep!="": # On verifie que le type saisie respecte les conditions ou alors qu'il est vide(dans ce cas on garde l'ancienne valeur)
                    print("The type is not correct")
                    rep=input("Input the type of the state "+MonDico[i][field[0]]+" among: ordinary(0), initial(1), final(2) or   initial and final(3) (Enter to skip):")
            if rep != "":
                MonDico[i][list(FIELDNAMES(MonDico))[1]]=rep

            # Modification des etat de destination
            for j in range(2,len(field)):
                check=0
                while check==0:
                    print(MonDico[i][field[0]],":",field[j],"-->",MonDico[i][list(FIELDNAMES(MonDico))[j]])
                    rep=input("Enter a new destination state (Enter to skip):")
                    rep=ListState(rep)
                    rep=ClearState(rep)

                    if type(rep)==str:
                        if VerifSaisieNouvelEtat(rep,EtatDico(MonDico))== False:
                            print("The name of the state do no respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                        else:
                            check=2
                            if rep != "":
                                #print("test")
                                MonDico[i][list(FIELDNAMES(MonDico))[j]]=rep

                    if type(rep)==list:
                        check=1
                        print("\n")
                        wait()
                        for k in range(len(rep)):
                            if VerifSaisieNouvelEtat(rep[k],EtatDico(MonDico))==False and check==1:
                                print(rep[k],": the name of the state do not respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                                check=0
                                break

                            else:
                                print(rep[k],"Correct")
                               
                if type(rep)==list and rep[k]!="":
                    MonDico[i][list(FIELDNAMES(MonDico))[j]]=rep

        return MonDico

#
#Status   
#OK
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

def ConvertIndiceDico(MonDico):
    if DicoVide(MonDico):
        print("Error: the dictionnary is empty")
        return -1
    else:
        DicoFinal={}
        for i in range(len(MonDico.keys())):
            DicoFinal[i]=MonDico[list(MonDico.keys())[i]]
    return DicoFinal
#
#Status
#ok
#




def TrieDicoCle(MonDico):
    # Retourne -1 si le dictionnaire est vide
    # Retourne le dictionnaire trié sinon

    if DicoVide(MonDico):
        return -1
    
    else:
        Dico=sorted(MonDico.items(),key=lambda t:t[0])
        #Here it's a list not a dictionnary, let's convert it

        DicoFinal={}

        for i in range(len(Dico)):
            DicoFinal[Dico[i][0]]=Dico[i][1]
        return DicoFinal
#
#Status
# OK
#

def ListState(string):

    #Take in parameter, a string of state or a state 
    # Return the state if there is only one state
    # Return a list of states if there is more than one 

    if len(string)==0 or "," not in string:
        return string
    else:
        return( string.split(","))
#
#Status
#ok
#


def ClearState(State):
    # Take as parameter a list
    # Return this list without elements that are twice or more in
    # Return the State if there is only one state(no matter how many times) in the list
    # Return the parameter if the parameter is not a list

    if type(State) ==list:

        New=[]

        for i in range(len(State)):
            if State[i] not in New:
                New.append(State[i])
        if len(New)==1:
            return(New[0])
        else:
            return(New)
    else:

        return State


#
#Status
#OK
#


def modifListeEtat(ListeEtat):
    
    # Prend en parametre la liste des etat de notre Automate 
    # Retourne la liste modifiée par l'utilisateur

    if len(ListeEtat) == 0:#la liste est de taille 0 --> vide
        print("The list is empty")
        return -1

    else:
        #print("Liste OK")
        
        #Variable permettant de savoir quand s'arreter
        stop = 0

        while stop == 0:

            # On interroge l'utilisateur
            reponse =input(str(ListeEtat)+"\nDo you want to edit the state's list above (yes or no):")

            #On Convertit la chaine en minuscule
            reponse=reponse.lower()

            #On distingue les cas selon la reponse
            match reponse:

                #on veut modifier
                case "yes":

                    print("Edit")
                    Reponse2=input("Insert the name of the state to edit or remove it and insert the new name to add it:")

                    #Verification que la reponse est correcte:
                    while VerifSaisieEtat(Reponse2)==False:
                        print("The name do not respect conditions.\n"+CONDITIONS_ETAT)
                        Reponse2=input("New choice:")

                    #notre champs est désormais conforme 

                    if Reponse2 in ListeEtat:   #l'état choisi est dans la liste

                        Choix=input("Choosen state: "+Reponse2+" Do you want to remove(0) or edi(1) it:")

                        #Verification du champ 'Choix'
                        while VerifEntier(Choix)==False or int(Choix) not in [0,1]:
                            print("The expected answer is 0 or 1")
                            Choix=input("Choosen state: "+Reponse2+" Do you want to remove(0) or edi(1) it:")

                        if int(Choix)==0:
                            #Suppression
                            ListeEtat.remove(Reponse2)
                        
                        else:
                            #Modification
                            new=input("Insert the new state:")

                            #verification de la saisie
                            while VerifSaisieNewEtat(new,ListeEtat)==False:
                                print("The name do not respect conditions.\n"+CONDITIONS_ETAT)
                                new=input("New choice:")


                            ListeEtat=ModifListe(Reponse2,ListeEtat,new)


                    else:
                        #Ajout
                        ListeEtat.append(Reponse2)



                #On ne veut pas/plus modifier
                case "no":

                    print("End of edit")
                    wait()
                    #changement de la valeur de la variable stop pour s'arreter
                    stop=1
                

                #Autre reponse
                case _:
                    print("The expected answer is yes or no")

        return ListeEtat
#
#Status
#OK
#


def modifListeEvenement(ListeEvenement):

    # Prend en parametre la liste des evenement de notre Automate
    # Retourne la liste modifiée par l'utilisateur

    if len(ListeEvenement) == 0:#la liste est de taille 0 --> vide
        print("The list is empty")
        return -1

    else:
        #print("Liste OK")
        
        #Varaiable permettant de savoir quand s'arreter
        stop = 0

        while stop == 0:

            # On interroge l'utilisateur
            reponse =input(str(ListeEvenement)+"\nDo you want to edit the event list above (yes or no):")
            
            # On convertit la chaine en minuscule
            reponse=reponse.lower()

            # On distingue les cas selon la reponse 
            match reponse:

                #on veut modifier
                case "yes":

                    print("Edit")
                    Reponse2=input("Insert the name of the event to edit or remove it and insert the new name to add it:")

                    #Verification que la reponse est correcte:
                    while VerifSaisieEvenement(Reponse2)==False:
                        print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                        Reponse2=input("New choice:")

                    #notre champs est désormais conforme 

                    if Reponse2 in ListeEvenement:   #l'évènement choisi est dans la liste

                        Choix=input("Choosen event: "+Reponse2+" Do you want to remove(0) or edit(1) it:")

                        #Verification du champ 'Choix'
                        while VerifEntier(Choix)==False or int(Choix) not in [0,1]:
                            print("The expected answer is 0 or 1")
                            Choix=input("Choosen event"+Reponse2+" Do you want to remove(0) or edit(1) it:")

                        if int(Choix)==0:
                            #Suppression
                            ListeEvenement.remove(Reponse2)
                        
                        else:
                            #Modification
                            new=input("Insert the new event:")

                            #verification de la saisie
                            while VerifSaisieNewEvenement(new,ListeEvenement)==False:
                                print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                                new=input("New choice:")


                            ListeEvenement=ModifListe(Reponse2,ListeEvenement,new)


                    else:
                        #Ajout
                        ListeEvenement.append(Reponse2)



                #On ne veut pas/plus modifier
                case "no":

                    print("End of edit")
                    wait()
                    #changement de la valeur de la variable stop pour s'arreter
                    stop=1
                

                #Autre reponse
                case _:
                    print("The expected answer is yes or no")

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

        print("Error: the list is empty")
        return -1     
#
#status
#OK
#


def DicoVide(MonDico):
    # Retourne True si le Dictionnaire est vide
    # Retourne False si le Dictionnaire n'est pas vide
    # Return False if type of parameter is incorrect

    if type(MonDico)!=dict: #type
        print("Error: the type expected is dictionnary")
        return False    

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

        print("Error: the file do not exist")
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
        print("Automaton is empty")
        return False

    else:

        #Definition des liste des etats et evenement de notre Automate
        Etat=EtatDico(MonDico)
        Evenement=EvenementDico(MonDico) 
           
        for i in range(len(MonDico)):   # On parcours les etats   
            for j in range(len(Evenement)): #on parcours les evenements 
                
                # case of a list of states
                if type(MonDico[i][Evenement[j]])==list:
                    for k in range(len(MonDico[i][Evenement[j]])):
                        if MonDico[i][Evenement[j]][k] not in Etat and MonDico[i][Evenement[j]][k]!="":
                            return False

                # case of a single state
                if type(MonDico[i][Evenement[j]])==str:
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
            print("This state already exist")
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
            print("This event already exist")                      
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

def VerifDeterminism(Dico):


    if DicoVide(Dico):
        return -1
    else:
        #Testing the startingState's list's lenght is 1 ###utiliser la fonction de guillaume
        if len(listEtatInitial(Dico))!=1:
            return False
        
        #Testing there is no list of state 
        Evenement=EvenementDico(Dico)
        for i in range(len(Dico)):
            for j in range(len(Evenement)):
                Value=Dico[i][Evenement[j]]
                if type(Value) == list:
                    return False

        return True
    
#
#Status
# OK
#   



def ChangeToDeterminist(MonDico):

   

    # Function that take in parameters a dictionnary

    # Return an equivalent of the automaton but determinist

    # Return False if the dictionnary in parameter is empty

    # Return False if there is no initial state

    # Return the automaton if the automaton is already determinist

    if DicoVide(MonDico)==True:

        return False

    else:
        
        if VerifDeterminism(MonDico)==True:     #already determinist

            print("Already determinist")
            return MonDico

        Transition= {}

        Transition[0]={}

        match len(listEtatInitial(MonDico)):

 

            case 0:     #no initial state

                return False

 

            case 1:     #only one initial state
 

                for i in range(len(MonDico)):

                    if MonDico[i]["colonne"]==listEtatInitial(MonDico)[0]:  #putting initial state in new dictionnary

                        Transition[0]=MonDico[i]

                if len(Transition[0])==0:   #empty dictionnary created
                    return False

               

            case _:     #more than one

                #initializing new initial state as list:

                New_State=[]

                Type=[]

                for i in range(len(listEtatInitial(MonDico))): #adding this state(and type) to the list

                    New_State.append(listEtatInitial(MonDico)[i])

                    Type.append(TypeOfState(MonDico,listEtatInitial(MonDico)[i]))


                
            


                #Initializing variables 
                Initial=listEtatInitial(MonDico)

                Event=EvenementDico(MonDico)

                AddState(MonDico,New_State,1,"")    #adding the new initial state to the old dictionnary
                
                
                #-----------creating a tmp dictionnary of state--------



                Transition[0]["colonne"]=New_State

                Transition[0]["type"]=UpdateTypeL(Type,0)

                for i in range(len(Initial)):  

                    Type.append(TypeOfState(MonDico,Initial[i]))    #adding type to the list
                    
                    for j in range(len(Event)):

                        if Event[j] in Transition[0]:       # Event already exist in dictionnary

                            Transition[0][Event[j]].append(destination(MonDico,Initial[i],Event[j]))    #add new state

                            SortList(Transition[0][Event[j]])

                        else:           # new event, create it and add value

                            Transition[0][Event[j]]=[]

                            Transition[0][Event[j]].append(destination(MonDico,Initial[i],Event[j]))





        #------------------ordinary states---------------------

        #initializing variables

        Next=[] # State to process

        Done=[Transition[0]["colonne"]] # States already processed

        Etat=EtatDico(MonDico)

        Event=EvenementDico(MonDico)


        for j in range(len(Event)):  

            if Transition[0][Event[j]] not in Done:     # adding states to process

                Next.append(Transition[0][Event[j]])


        #each state was correctly added

 

        #process next states

        i=0

        while len(Next) != 0 :      #while a state to process

            #initializing variables

            type1=[]

            ETAT=EtatDico(Transition)

            EVENT=EvenementDico(Transition)

           

            if i+1 not in Transition:     #initializing if new index

                Transition[i+1]={"colonne":"","type":""}




            if Next[0] in ETAT:     # if already process, go to the next one


                i=i+1

                break


 

            for I in range(len(Next[0])):

                type1.append(TypeOfState(MonDico,Next[0][I]))   #add type of each sub-state too the list

                for j in range(len(Event)):

                    if Event[j]  not in Transition[i+1]:     #Event don't exist
                        Transition[i+1][Event[j]]=[]

                    if type(Transition[i+1][Event[j]])!=list:   # actual value not a list

                        Transition[i+1][Event[j]]=[Transition[i+1][Event[j]]]   #Convert into list


                    Transition[i+1][Event[j]].append(destination(MonDico,Next[0][I],Event[j]))#add new state to list

                    SortList(Transition[i+1][Event[j]])    

                    Transition[i+1][Event[j]]=ClearState(Transition[i+1][Event[j]])


                    if I == len(Next[0])-1: # last sub state of the state

                        if (Transition[i+1][Event[j]] not in Done) and (Transition[i+1][Event[j]] not in Next):     # New State, add to Next

                            Next.append(Transition[i+1][Event[j]])                       

            New_Type=UpdateTypeL(type1,1)

            Transition[i+1]["colonne"]=Next[0]

            Transition[i+1]["type"]=New_Type

            Done.append(Next[0])   

            del(Next[0])

            i=i+1

        

    #here we have our new dictionnary but all states are registred as list, 
    #let's convert this with a new function ConvertDictionnaryListToStr() and ConvertListToStr()

    Transition=ConvertDictionnaryListToStr(Transition)

    return Transition
#
#Status
# OK
#

def ConvertDictionnaryListToStr(Dictionnary):
    # take in parameter a dictionnary
    # return False if the dictionnary is empty
    # return the dictionnary with each state converted as string(Ex:["q0","q1"]->"q0,q1")
    # use the function ConvertListToStr()
    
    if DicoVide(Dictionnary)== True:        #empty
        print("Error: the dictionnary is empty")
        return False
    else:
        Event=EvenementDico(Dictionnary)
        for i in range(len(Dictionnary)):
            for j in range(len(Event)):
                if type(Dictionnary[i][Event[j]])==list:
                    Dictionnary[i][Event[j]]=ConvertListToStr(Dictionnary[i][Event[j]])
            if type(Dictionnary[i]["colonne"])==list:
                Dictionnary[i]["colonne"]=ConvertListToStr(Dictionnary[i]["colonne"])
    return Dictionnary
#
#Status
# Ok
#

def ConvertListToStr(List):
    #take in parameter a list
    # Return False if the list is empty
    # Return False if the parameter is not list
    # Return the list converted as a string

    if type(List)!=list:
        print("Error: type not respected")
        return False
    else:
        if len(List)==0:
            print("Error: the list is empty")
            return False
        else:
            string=""
            for i in range(len(List)):
                if string!="":
                    string=string+"."
                string=string+List[i]
            return string
#
#Status
# Ok
#

def indexOfState(MonDico,State):

    # Take in parameter a dictionnary and a state

    # Return Flase if the dictionnary is empty or if the state is not in the dictionnary

    # Return the index of the State if the state is in the dictionnary

    ETAT=EtatDico(MonDico)

 

    if DicoVide(MonDico)==True:

        print("Error: the dictionnary is empty")

        return False

    else:

        if State not in ETAT:

            print("Error: the state is not in this dictionnary")

            return False

        else:

            for i in range(len(MonDico)):

                if MonDico[i]["colonne"]==State:

                    return i

            print("Error: the state is not in this dictionnary")

            return False

#
#Status
# OK
#

def TypeOfState(MonDico,Etat):

    # Take in parameter a Dictionnary and a state

    # Return False if the dictionnary is empty or the state is not in the dictionnary

    # Return the type of the state if it is in the dictionnary

    ETAT=EtatDico(MonDico)

 

    if DicoVide(MonDico)==True:

        print("Error: Empty dictionnary")

        return False

    else:

        if Etat not in ETAT:

            print("Error: the state is not in this dictionnary")

            return False

        else:

            for i in range(len(MonDico)):

                if MonDico[i]["colonne"]==Etat:

                    return MonDico[i]["type"]

            print("Error: the state is not in this dictionnary")

            return False

#
#Status
#
#

def UpdateType(type1,type2):

    # take in parameter two type

    # Return False if at least one is incorrect(not in TYPE)

    # Return the new type

    type1=int(type1)

    type2=int(type2)

    if VerifType(type1)==False or VerifType(type2)==False:

        print("Error: At least one type is incorrect")

        return False

    else:

        if type1==type2:

            return type1

 

        if type1==0:    #type2 give more informations

            return type2

 

        if type2==0:    #type1 give more informations

            return type1

 

        if type1==3 or type2==3:    #at least one is inital and final

            return 3

       

        if (type1==1 and type2==2)  or (type1==2 and type2==1):   # one final and one initial

            return 3

#
#Status
# OK
#

def UpdateTypeL(Type,mode=-1):
    # Take in parameter a list of type and an integer (that determine mode)
    # Return false if one of them is incorrect
    # Return False if the list is empty
    # Return False if the parameter is not a list
    # Return the equivalent type
    # Return False if mode is not an integer or not a known mode

    #
    if type(mode)!= int:
        if VerifEntier(mode)==True: # we can convert mode into integer
            mode=int(mode)
        else:
            print("Error: invalid mode")
            return False


    match mode:
        #mode : 0(initial) or 1(ordinary)


        case 0: #initial using
            if type(Type)!=list:        #type
                print("Error: the parameter must be a list")
                return False
            
            if len(Type)==0:            #empty
                print("Error: the list is empty")
                return False
            
            for i in range(len(Type)):      #correct
                if VerifType(Type[i])==False:
                    print("The type ",Type[i]," is incorrect")
                    return False
            
            
            j=0
            while "0" in Type:
                if int(Type[j])==0: # 0 are useless to determine the type
                    del(Type[j])    # remove 0's
                    break
                else:
                    j=j+1
            #Verify there is something else than 0
            if len(Type)==0:
                return "0"

            if "3" in Type:     # 3 is the more dominant
                return "3"
            
            if "1"  in Type:
                if "2"  in Type:  # Both type 1 and 2 -> final+initial ==>3
                    return "3"
                else:
                    return "1"      # type 1 but not 2
            else:
                if "2"  in Type:  # Type 2 but not 1
                    return "2"
                else:
                    return "0"      # neither 1  and 2 ==> 0 (impossible to access)


        case 1: #ordinary case (can't be initial like in determinist automaton building)
            
            
            if type(Type)!=list:    #type
                print("Error: the parameter must be a list")
                return False
            
            if len(Type)==0:        #empty
                print("Error: the list is empty")
                return False

            for i in range(len(Type)):      #correct
                if VerifType(Type[i])==False:
                    print("The type ",Type[i]," is incorrect")
                    return False            
            
            if "2" in Type or "3" in Type: #final

                return "2"
            else:
                return "0"   #any

        case _:
            print("Error: invalid mode")
            return False




#
#Status
#Ok
#
def SortList(Mylist):

    # take in parameter a list

    # return False if the list is empty

 

    if len(Mylist)==0:

        print("Error: empty list")

        return False

    else:

        for i in range(len(Mylist)):

 

            if type(Mylist[i])==list:   # if list inside list, split it

                for j in range(len(Mylist[i])):

                    Mylist.append(Mylist[i][j])

                del(Mylist[i])    

 
        Mylist.sort()
        return(Mylist)
#
#Status
# OK
#

def destination(MonDico,state,Event):

 

    if DicoVide(MonDico):

        print("Error: empty Dictionnary")

        return False

 

    Return=[]

    for i in range(len(EtatDico(MonDico))):

        if state == EtatDico(MonDico)[i] and Event in EvenementDico(MonDico):

            Return=MonDico[i][Event]

            return Return

 

    # unkonwn event or state:

    print("unknonw event or state")

    return False

 

#
#Status
# Ok
#
def EtatDico(MonDico):
    # Retourne une liste contenant l'ensemble des etat de l'AEF -> colonne de gauche(sauf premiere ligne)

    if DicoVide(MonDico)==True:
        print("Error: the automaton is empty")
        return -1


    else:
        etat=[]

        for i in range(len(MonDico.keys())):

            etat.append(MonDico[list(MonDico.keys())[i]]['colonne'])
        return(etat)
#
#status
#ok
#     

def EvenementDico(MonDico):
    # Retourne la liste contenant l'ensemble des evenement de l'AEF -> premiere ligne(sauf premiere colonne)

    if DicoVide(MonDico)==True:
        print("Error: the automaton is empty")
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
    A=input("\nYour choice:")

    while VerifEntier(A)==False:    # Tant que l réponse n'est pas un entier on boucle sur la question
        print("The expected answer is an integer")
        print(TEXTE_DEMANDE_USER)
        A=input("\Your choice:")
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
            print("File OK")
            return NomFichier


        #Mode Choix fichier de sortie
        case 2:

            if FichierExiste(NomFichier)==False:#Le fichier n'existe pas 
                print("No corresponding file, creating new file")
                    #Pour Créer un fichier en python, on l'ouvre en mode ecriture(et cela sera fait lors de l'ecriture)

            else:   #Le fichier existe déjà
                print("File OK")
                wait()
            return NomFichier

        case _:
            print("Error when calling choixFichier()")
            return -1
            #erreur appel de choixFichier()
#
#status
#ok
#

def listEtatInitial(MonDico):
    l=[]
    for i in range (len(MonDico)):
        if ((int(list(MonDico[i].values())[1])==1) or (int(list(MonDico[i].values())[1])==3)):
            l.append(list(MonDico[i].values())[0])
    return l
#
#status
#ok
#

def listEtatFinal(MonDico):
    liste=[]
    for i in range (len(MonDico)):
        if ((int(list(MonDico[i].values())[1])==2) or (int(list(MonDico[i].values())[1])==3)):
            liste.append(list(MonDico[i].values())[0])
    return liste
#
#status
#ok
#

def ExisteTransition(Evenement,Etat1,Etat2):
    print("test")
    #A faire
#
#status
#En cours
#

def VerifMotAEF(MonDico):

    EtatI=listEtatInitial(MonDico)
    EtatF=listEtatFinal(MonDico)
    Evenement=EvenementDico(MonDico)
    Etat=EtatDico(MonDico)
    Fin=[]


    mot=input("Entrez un mot \n")
    if DicoVide(MonDico)==True:
        print("l'automate est vide")
        return False

    for i in range (len(mot)):#parcours du mot 
        for j in range (len(Evenement)):
            if(mot[i]==Evenement[j]):#on verifie que chaque caractère est un evenement existant
            
                for k in range (len(Etat)):
                    for l in range (len(Etat)):
                        if (ExisteTransition(Evenement[j],Etat[k],Etat[l])==True):
                            Fin.append(Etat[k])
                            newEtat=Etat[l]
                    if (ExisteTransition(Evenement[j],newEtat,Etat[k])==True):
                        Fin.append(newEtat)
                        newEtat=Etat[k]
            #print("else")                       
    nbEtat=len(Fin)
    for m in range (len(EtatI)):
        if (Fin[0]==EtatI[m]):
            for n in range (len(EtatF)):
                if(Fin[nbEtat]==EtatF[n]):
                    return True
    return False
    
#
#status
#En cours
#

#COCOZONE




def VerifComplet(Dico):#return TRUE if the automate if complete, FALSE else
    Events = EvenementDico(Dico)
    Keys = EtatDico(Dico)
    end = True
    for i in range(len(Dico)): #test every elmt
        for j in range(len(Events)): #test every possible transition
            if Dico[i][Events[j]]=="": #if a transition don't have an output, the automate isn't complete
                end = False
                return end
    return end

#
#status
#ok
#
              
def ChangeToComplet(Dico): #to do, utiliser la fct pour ajouter un evenement poubelle et rajouter lorsqu'on trouve un lien manquant un lien vers poubelle pour chaque événement
    if not VerifComplet(Dico):#the automate isn't complete
        Events = EvenementDico(Dico)
        bin = "bin"
        Keys = EtatDico(Dico)
        if bin in Keys: #if bin is already the name of a state
            n=0
            bin=bin.str(n)
        
        while bin in Keys:
            n+=1
            bin = "bin".str(n)
        
        for i in range(len(Dico)): #test every elmt
            for j in range(len(Events)): #test every possible transition
                if Dico[i][Events[j]]=="": #if a transition don't have an output, the automate isn't complete
                    Dico[i][Events[j]]=bin #replace the free transition to a transition to the bin
        print(Dico)
        Dico = AddState(Dico,bin,0,bin)
    return Dico
#
#status
#ok
#

def AddState(Dico,name,type=0,event=""): #add the state to the list with default "" destination to all events
    States = EtatDico(Dico)
    if name in States:  #the state already exist -> nothing to do
        return Dico
    else:
        Events = EvenementDico(Dico)
        print (event)
        if event not in States and event != name :                #case of an invalid event (invalid for "" -> we change "" to "")
            event =""
        i=len(Dico)                                 #event go back to the default case
        Dico.setdefault(i,i)              #add the row len(Dico) to the dico
        Dico[i]={}     #generate the Dico we are going to fill
        Dico[i]["colonne"]=name #giving a colonne key with the name attribute
        Dico[i]["type"]=type #same with the type
        for j in EvenementDico(Dico): #going throught all existing Event
            Dico[i][j]=event #giving the event the desired destination
        

    return Dico
#
#status
#ok
#

def ComplementDico(Dico): #return the dico with all types changed from final to non-final and vice-versa
    #type 0->2, type 1->3 type 2->0 type 3->1
    for i in range(len(Dico)):
        type = Dico[i]["type"]
        if type >=2:
            ReplaceType(Dico,i,(type-2))
        else:
            ReplaceType(Dico,i,(type+2))
    return Dico

def ReplaceType(Dico,num:int,type:int): #replace the type of the event coresponding to the number num in the dico to the type type
    Dico[num]["type"]=type
    return Dico

def ReplaceEvent(Dico,name,elmt1="",elmt2=""): #replace the events elmt2 of the state name to elmt1
    return Dico
def ReplaceDestination(Dico,num,event,destination=""): #replace the destination of state number num event event to the destination destination
    if num < len(Dico):
        if event in EvenementDico(Dico):
            Dico[num][event]=destination
    return Dico

def MiroirDico(Dico): #return the mirror Automaton (correspond to a complement with all transition reversed (destination become origin and vice-versa))
    DicoFinal = Dico #create the dico we are going to fill (with default values all the existing ones)
    DicoFinal = ComplementDico(DicoFinal) #change all the types, only transitions to go
#to do, utiliser .index
    return DicoFinal
#
#status
#ok
#


#END OF COCOZONE


#
#
#---------------------------------------------------------------------------------------------------------------------------------------------
#PROGRAMME
#---------------------------------------------------------------------------------------------------------------------------------------------
#
#
if DEBUGG != 1:

    print("\n--------------------\nAutomaton's manager\n--------------------")
    wait()
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
    #Dictionnaire=CreationDico()
    #print(Dictionnaire)
    #print(listEtatInitial(Dictionnaire))
    #print(listEtatFinal(Dictionnaire))
    #print(VerifMotAEF(Dictionnaire)) 
    #print(EtatDico(Dictionnaire))
    
    
    print(Dictionnaire)
    print(VerifDeterminism(Dictionnaire))
    #Dictionnaire={
    #    0: {'colonne': 'q1', 'type': '0', 'A': 'q3', 'B': 'q0', 'C': 'q1', 'D': 'q2'}, 
    #    3: {'colonne': 'q2', 'type': '0', 'A': 'q2', 'B': 'q3', 'C': 'q0', 'D': 'q1'}, 
    #    2: {'colonne': 'q3', 'type': '0', 'A': 'q1', 'B': 'q2', 'C': 'q3', 'D': 'q0'}
    #    }

    ARRET = 1

#
#------------------------------------
#------------------------------------
#------------------------------------
#

while ARRET == 0 :
    
    ChoixUser=DemandeUser()
    time.sleep(0.8)
    match ChoixUser:
        
        #Arret
        case 0:
            print("-----------------")
            print("Fin du programme")
            print("-----------------")
            ARRET=1

        #chargement automate depuis .csv
        case 1:
            print("\n------------------------------------------")
            print("Chargement d'un Automate depuis un Fichier")
            print("------------------------------------------\n")
            wait()

            #choix du fichier 
            Fichier=input("Saisissez le nom du fichier:")

            #verif fichier existe
            FichierEntree=choixFichier(1,Fichier)

            Dictionnaire=CSVToDico(FichierEntree)
            if DicoVide(Dictionnaire)==False:
                print("Automate chargé avec succès")
                wait()
    
            else:
                print("Automate vide à l'arrivée, un probleme est apparu")
                wait()
            

        #Affichage Automate depuis .csv    
        case 2:
            print("\n-----------------------------------------")
            print("Affichage d'un Automate depuis un Fichier")
            print("-----------------------------------------\n")
            wait()

            #choix du fichier 
            Fichier=input("Saisissez le nom du fichier:")

            #verif fichier existe
            FichierEntree=choixFichier(1,Fichier)

            AffichageAutomateFromCSV(FichierEntree)
            


        #Affichage de l'Automate en mémoire
        case 3:
            print("\n----------------------------------")
            print("Affichage de l'Automate en mémoire")
            print("----------------------------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:
                print("Erreur: Aucun Automate n'est chargé en mémoire")
                wait()
            else:
                AffichageAutomateFromDico(Dictionnaire)



        #Enregistrer l'automate dans un fichier
        case 4:
            print("\n---------------------------------------------------")
            print("Sauvegarde de l'Automate en mémoire vers un fichier")
            print("---------------------------------------------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:
                print("Erreur: Aucun Dictionnaire n'est chargé en mémoire")
                wait()

            else:
                #choix du fichier de destination
                Fichier=input("Saisissez le nom du fichier:")

                #verif fichier existe
                FichierSortie=choixFichier(2,Fichier)
            
            #confirmation si non vide ?
                if DicoToCSV(Dictionnaire,FichierSortie) == 0:
                    print("Sauvegarde réussie")
                    wait()
                else:
                    print("Erreur lors de la sauvegarde")
                    wait()

        #Effacer Automate en memoire
        case 5:
            print("\n-----------------------------------")
            print("Effacement de l'Automate en mémoire")
            print("-----------------------------------\n")
            wait()
            Dictionnaire={}#remplacement par dictionnaire vide
            print("Automate effacé")
            wait()


        #Créer un nouvel automate
        case 6:
            print("\n-----------------------------")
            print("Création d'un nouvel Automate")
            print("-----------------------------\n")
            wait()

            Dictionnaire=CreationDico()
            if VerifAEF(Dictionnaire)==False:
                print("Erreur lors de la création")
                wait()
            else:
                print("Création de l'automate avec succès")
                wait()
                AffichageAutomateFromDico(Dictionnaire)


        #Modifier un Automate
        case 7:
            print("\n--------------------------")
            print("Modification d'un Automate")
            print("--------------------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:
                print("Aucun Automate en mémoire")
                wait()
            else:
                ModifDico(Dictionnaire)


        #verifier si un Automate est un AEF en mémoire uniquement (l'ordre peut changer)
        case 8:
            print("\n----------------")
            print("Verification AEF")
            print("----------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:    #il n'y a pas d'Automate en memoire
                print("Aucun Automate n'est enregisé en mémoire")
                wait()
            else:       #un automate a bien été trouvé
                match VerifAEF(Dictionnaire):
            
                    #L'automate est un AEF
                    case True:
                        print("L'automate est un Automate d'état fini")
                        wait()
                    
                    #L'automate n'est pas un AEF
                    case False:
                        print("L'automate n'est pas un Automate d'état fini")
                        wait()

                    #Cas défaut
                    case _: 
                        print("Erreur: probleme lors de la verification de l'automate")
                        wait()
                    
                    

        #verify if an automaton is complete
        case 9:
            print("\n---------------------")
            print("Complete Verification")
            print("---------------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:    #No automaton in memory
                print("No Automaton in memory")
                wait()
            else:
                match VerifComplet(Dictionnaire):
                    case True : #automaton is complete
                        print("The automaton is complete")
                        wait()

                    case False :#automaton is not complete
                        print("The automaton is not complete")
                        wait()

                    case _: #default case
                        print("Error: problem with the verification")
                        wait()

        #to complete an automaton
        case 10:
            print("\n--------------------")
            print("Automaton completion")
            print("--------------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:    #No automaton in memory
                print("No Automaton in memory")
                wait()

            else:
                Dictionnaire = ChangeToComplet(Dictionnaire)
                print("done \n")
                wait()

        #cas default
        case _:
            print("Choix non valide\n")
            wait()








#Dictionnaire de la forme :
#
#
#
#
#{
#0: {'colonne': 'a','Type':0,'A': 'var1', 'B': 'var2', 'C': 'var3'},
#1: {'colonne': 'b', 'A': 'var4', 'B': 'var5', 'C': 'var6'},
#2: {'colonne': 'c', 'A': 'var7', 'B': 'var8', 'C': 'var9'},
#3: {'colonne': 'd', 'A': '1', 'B': '2', 'C': '3'}
#}
#
#
#Dictionnaire[i].values().values('Type')
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