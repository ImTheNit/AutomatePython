

#
#
#IMPORT
#
#

import csv #To manage transfert between python script and csv file
import os   #To verify if the size of a file(test if it is emmpty)
import time #To use sleep() function, to make the programm having short waiting time

#needed to resolve linear system(For regular expression)
#import numpy as np
#import matplotlib.pyplot as plt
#from scipy import linalg
#
#
#Variables
#Dictionnary
#
#

#Files and separator
FichierEntree="data.csv"
FichierSortie="data3.csv"
FileChoice="ChoiceFile.txt" # File containing choices
DELIMITER=";"

ARRET=0 #0 if we want to continue, 1 else
DEBUGG=1 #1 if we want to debugg, 0 else
Dictionnaire={}
automaton={}
#Type of state
#   0-> any
#   1-> initial
#   2-> final
#   3->initial and final
TYPE=[0,1,2,3]

#Forbiden characters in differents input
RESTRICTION_CHOIX_ETAT=[";"," "]

RESTRICTION_CHOIX_EVENEMENT=[";"," "]

RESTRICTION_CHOIX_NOUVEL_ETAT=[";"," "]

#STR including conditions messages of different inputs

CONDITIONS_ETAT="A state can't contain "+str(RESTRICTION_CHOIX_ETAT)+"and be empty"

CONDITIONS_EVENEMENT="An event can't contain "+str(RESTRICTION_CHOIX_EVENEMENT)+"and be empty"

CONDITIONS_NOUVEL_ETAT="A state can't contain "+str(RESTRICTION_CHOIX_ETAT)+",be empty and the destination state must exist"

Done_State=[]

State_CoAccess=[]


#
#
#------------------------------------------------------------------------------------------------------------------------------------
#Functions
#------------------------------------------------------------------------------------------------------------------------------------
#
#

def DisplayChoices():

    if os.path.exists(FileChoice):
        File=open(FileChoice,"r")
        print(File.read())
        File.close()
        return True
    else:
        print("Missing File:",FileChoice)
        return False

def wait(a=0.8):
    # take in parameter a time to wait, default time:0.8s
    # make a break and then exit
    time.sleep(a)
    return 0
#
#Status
#OK
#


def AffichageDico(MonDico):
    #take as parameter a dictionnary
    #print the dictionnary, index by index

    print("Dictionnary:")

    for i in range(len(MonDico)):
        print(MonDico[i],"\n")
    return 0
#
#status
#ok
#

def AffichageAutomateFromDico(MonDico):
    # Take as parameter a dictionnary
    # Return False if it is empty
    # Return 0 and display the dictionnary like:
    # State:Event --> destination State

    if DicoVide(MonDico)== True:
        print("Error: the dictionnary to print is empty")     
        return False

    else:

        print("Affichage sous la forme:\nETAT:évènement-->NouvelEtat\n")
        field=list(FIELDNAMES(MonDico))
        for i in (range(len(MonDico))):

            for j in range(1,len(field)):
                print(MonDico[i][field[0]],":",field[j],"-->",MonDico[i][list(FIELDNAMES(MonDico))[j]])
            print("\n")#to separate the display for each state
            wait()
        return 0
#
#status
#ok
#

def AffichageAutomateFromCSV(CSVFILES):
    # Take as parameter a file name
    # Return False if not existed, empty, NEED ADD VERIFICATION OF THE EXTENSION(.csv)
    # Return 0 and display automate from the file

    #We verify the file exist and not empty
    if FichierExiste(CSVFILES)==True:
        if FichierVide(CSVFILES)==False:

            # We convert file into dictionnary and then display it
            Dico=CSVToDico(CSVFILES)
            AffichageAutomateFromDico(Dico)
            return 0
        
        else:   #empty file
            print("Error: the file ",CSVFILES," is empty")    
            return False
            

    else:       #unexistant file
        print("Error: the file do not exist\n")
        return False 
#
#status
#ok
#


def CSVToDico(CSVFILES):
    # Take as parameter a file name
    # Return False if not existed, empty, NEED ADD VERIFICATION OF THE EXTENSION(.csv)
    # Return the dictionnary corresponding to the file.
     
    Dictionnaire={}
    if FichierExiste(CSVFILES)==False:  # unexistant file
        print("Error: the file do not exist\n")
        return False
        
    else:
        if FichierVide(CSVFILES)==False:

            with open(CSVFILES) as csvfile:

                reader = csv.DictReader(csvfile,delimiter=DELIMITER)    #We open the file, take as delimitor, the global var previously defined
                count=0

                for row in reader:                  #The i-th line of our file is place in our dictionnary at the index i, le line is converted as a dictionnary
                    
                    Dictionnaire[count]=row
                    # We want the programm to convert a multiple choice of state in the csv file into a list of state (separator of state in the file: ",")
                    
                    for i in range(len(EvenementDico(Dictionnaire))):
                        Value=ListState(row[list(EvenementDico(Dictionnaire))[i]])
                        row[list(EvenementDico(Dictionnaire))[i]]=ClearState(Value)
                    count += 1           
            return (Dictionnaire)

        else:   # empty Dictionnary
            print("Error: the file is empty")
            return False
            
#
#status
#ok
#

def DicoToCSV(MonDico,CSVFILES):
    # Take as parameters a dictionnary and a file name NEED ADD VERIFICATION OF THE EXTENSION(.csv)
    # Create the file if not already exist, delete the old file already exist
    # Return False if empty dictionnary 
    # Return 0 and write the dictionnary in the file

    if DicoVide(MonDico)==True: # empty dictionnary
        print("Error: the dictionnary is empty")
        return False
        
    else:
        with open (CSVFILES,'w',newline="") as csvfiles:
            #Variables

            fieldnames=FIELDNAMES(MonDico)  #keys of dictionnary (here:it is the first line of the csv file['colonne', 'type', 'A', 'B', 'C', 'D'])
            writer =  csv.DictWriter(csvfiles,fieldnames,delimiter=DELIMITER)

            #Writing
            writer.writeheader()
            for i in range(len(MonDico)):
                writer.writerow(MonDico[i])
        return 0
#
#status
#ok
#

def CreationDico():
    #Function that create our dictionnary and return it
    #input are integreate inside
    #No parameters

    #Initializing variables and objects:
    MonDico={}
    Etat=[]    #List of states
    Type=[]    # List of Type associate to each State
    Evenement=[]    #List of Event
    
    #Variables that show if we have to stop user input
    a=1

    #Input States
    while a != 0:

        # Ask user
        Rep=input("Input a state (0 to stop):")

        if VerifEntier(Rep)==True : # The input can be convert as integer
            if int(Rep)==0:         # User want to stop input state
                a=0


            else:   #integer but not 0 so the state name is an integer(accepted)

                while VerifSaisieNewEtat(Rep,Etat)==False:  # Verify the input is correct

                    print("The name of the new state do not respect the conditions.\n"+CONDITIONS_ETAT)
                    Rep=input("New choice:")

                # We initialize Rep2 outside the list of accepted Type to access the while  
                Rep2=-1
                
                while VerifType(Rep2)==False :  # Verify the input Type is correct

                    Rep2=input("Input the type of the state"+Rep+" among: ordinary(0), initial(1), final(2) or   initial and final(3):")
                    if VerifType(Rep2)==False:
                        print("The type is not correct")

                # Now state and type are coorect, we can add them to lists
                Type.append(Rep2)
                Etat.append(Rep)


        else:                       #The input can't be converted to integer, the user want to continue input

            while VerifSaisieNewEtat(Rep,Etat)==False:  # Verify the input is correct

                print("The name of the new state do not respect the conditions.\n"+CONDITIONS_ETAT)
                Rep=input("New choice:")

            # We initialize Rep2 outside the list of accepted Type to access the while    
            Rep2=-1
            
            while VerifType(Rep2)==False : # Verify the input Type is correct

                Rep2=input("Input the type of the state "+Rep+" among: ordinary(0), initial(1), final(2) or   initial and final(3):")
                if VerifType(Rep2)==False:
                    print("The type is not correct")

            # Now state and type are coorect, we can add them to lists
            Type.append(Rep2)
            Etat.append(Rep)

    #Control Display
    print("The list of input's states:",Etat)
    print("The list of input's state's type:",Type,"\n")
    wait(0.4)


    # Input again, but for events, same variable a
    a=1

    # Input Event
    while a != 0:

        # Ask user
        Rep=input("Input an event (0 to stop):")

        if VerifEntier(Rep)==True : # The input can be convert as integer
            if int(Rep)==0:         # User want to stop input event
                a=0

            else:

                while VerifSaisieNewEvenement(Rep,Evenement)==False: # Verify the input is correct

                    print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                    Rep=input("New choice:")

                # Now the Eevnt is correct we can add it to his list    
                Evenement.append(Rep)


        else:                       #The input can't be converted to integer, the user want to continue input
            
            while VerifSaisieNewEvenement(Rep,Evenement)==False:    # Verify the input is correct

                print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                Rep=input("New choice:")

            # Now the Event is correct we can add it to his list
            Evenement.append(Rep)


    # Control Display      
    print("The list of input's events:",Evenement,"\n")
    wait(0.4)


    # Input Destination states
    print("Inserting destination's states:\nSynthax: State:Event-->destination's state")

    for i in range(len(Etat)):  # For each State

        MonDico[i]={}     #Create the index in the dictionnary to access later VITAL
        MonDico[i]["colonne"]=Etat[i]
        MonDico[i]["Type"]=Type[i]

        for j in range(len(Evenement)):     #  For each Event
            check=0
            while check == 0:

                # Ask user
                Rep3=input(Etat[i]+":"+Evenement[j]+"-->")

                # Convert the answer into a list if two or more states
                Rep3=ListState(Rep3)
                Rep3=ClearState(Rep3)
                if type(Rep3)==str:
                    if VerifSaisieNouvelEtat(Rep3,Etat)==False:  # Verify the input is correct
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

            # Now input is ok, add to the dictionnary
            MonDico[i][Evenement[j]]=Rep3
            

    return MonDico

#
#status
#OK
#


def FIELDNAMES(MonDico):
    # Take as paramter a dictionnary
    # Return False if empty dictionnary
    # return the list of the field (Ex:['colonne','Type','Event1','Event2'])

    if DicoVide(MonDico)==True:
        return False

    else:
        return(MonDico[0].keys())
        # We suppose the first state of our dictionnary have the maximum of possible keys
        #(ie, No other state have a keys, that the first state do not
#
#status
#ok
#
    
def ModifDico(MonDico):
    # Take as parameter a dicitonnary
    # return False if the dictionnary is empty
    # return the new dictionnary

    if DicoVide(MonDico)==True:
        print("Error: the dictionnary is empty")
        return False
    else:
        #Variables
        ListeEtat=EtatDico(MonDico)
        ListeEvenement=EvenementDico(MonDico)

        AncienneListeEtat=[]
        AncienneListeEvenement=[]

        # Copy content in backup list to compare 
        for i in range(len(ListeEtat)):
            AncienneListeEtat.append(ListeEtat[i])
        
        for i in range(len(ListeEvenement)):
            AncienneListeEvenement.append(ListeEvenement[i])
        
        # Modify lists by asking user
        modifListeEtat(ListeEtat)
        modifListeEvenement(ListeEvenement)

        # Delete unwanted states
        
        print("Removing unwanted states")
        wait()
        for i in range(len(AncienneListeEtat)):
            if AncienneListeEtat[i] not in ListeEtat:      # state was here before, but not anymore          
                a=MonDico.pop(i)


        # Add wanted states

        print("Adding new states")
        wait()


        for i in range (len(ListeEtat)):
            Taille=len(MonDico)
            if ListeEtat[i] not in AncienneListeEtat:   # state was not here before 
                MonDico.setdefault(Taille+1,{'colonne':ListeEtat[i]}) # add it to the dictionnary
        
        # Check if the dictionnary is sorted, if not sort it, in order to balance it 
        if VerifTrieDico(MonDico)==False:
            MonDico=TrieDicoCle(MonDico)
    
        MonDico=ConvertIndiceDico(MonDico)  # Edit dictionnary to make index been succesives integers


        #Delete unwanted events

        print("Removing unwanted events")
        wait()

        for i in range(len(AncienneListeEvenement)):
            if AncienneListeEvenement[i] not in ListeEvenement: # event was here before, but not anymore
                for j in range(len(MonDico)):
                        a=MonDico[j].pop(AncienneListeEvenement[i]) # delete it   

        # Add wanted events

        print("Adding new events")
        wait()

        for i in range(len(ListeEvenement)):
            if ListeEvenement[i] not in AncienneListeEvenement: # event was not here before
                for j in range(len(MonDico)): # add the event in each state of the dictionnary
                    MonDico[j][ListeEvenement[i]]=""

        # Display the automaton and ask input for each destination state

        print("New fields in the automaton")
        print("State:Event-> destination's state")

        for i in range(len(MonDico)):
            field=list(FIELDNAMES(MonDico))
            
            
            # Edit type 
            print(MonDico[i][field[0]],":",field[1],"-->",MonDico[i][list(FIELDNAMES(MonDico))[1]])
            rep=input("Input the type of the state "+MonDico[i][field[0]]+" among: ordinary(0), initial(1), final(2) or    initial and final(3) (Enter to skip):")

            while VerifType(rep)==False and rep!="": # We check if the type respect conditions, if empty keep the old value
                    print("The type is not correct")
                    rep=input("Input the type of the state "+MonDico[i][field[0]]+" among: ordinary(0), initial(1), final(2) or   initial and final(3) (Enter to skip):")
            if rep != "":
                MonDico[i][list(FIELDNAMES(MonDico))[1]]=rep

            # Edit destination state
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
    # take as parameter a dictionnary
    # return - if the dictionnary is empty
    # return the dictionarry with reorganized index 
    #
    #Need to check if the keys of the dictionnary are sorted (function VeriTrieDico() and TriDicoCle())

    # Suppr is a list containing index that must be delete from our dictionnary
    Suppr=[]

    
    if DicoVide(MonDico)==True:
        return -1

    else:
        if VerifTrieDico(MonDico)==False:
            MonDico=TrieDicoCle(MonDico)
        
        for i in range(len(list(MonDico.keys()))):   
            if list(MonDico.keys())[i]!=i:   # Check if each index is correctly named, else named it correctly 
 
                AncienneValeur=list(MonDico.values())[i] # identify which index we have to remove

                MonDico.setdefault(i,AncienneValeur) # add new key et attribute the corresponding value, careful: index added at the end

                if i not in Suppr: # we add the index only if this index is not attributed
                    Suppr.append(list(MonDico.keys())[i])

        for i in range(len(Suppr)): # delete unwanted index
            a=MonDico.pop(Suppr[i])

    return MonDico
#
#Status
#OK
#

def ConvertIndiceDico(MonDico):
    # Take as parameter a dictionnarie
    # return False if the dictionnary is empty
    # return the dictionnary with index converted successively

    if DicoVide(MonDico)==True:
        print("Error: the dictionnary is empty")
        return False
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
        Info=0
        
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
                        Info=1
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
            if Next[0] in ETAT:     # if already process, go to the next one

                i=i+1

                
            else:

                if i+1 not in Transition:     #initializing if new index

                    Transition[i+1]={"colonne":"","type":""}


                for I in range(len(Next[0])):
                    if type(Next[0])==list:
                        type1.append(TypeOfState(MonDico,Next[0][I]))   #add type of each sub-state too the list
                        INFO=0

                    else :
                        type1.append(TypeOfState(MonDico,Next[0]))
                        INFO=1
                    for j in range(len(Event)):

                        if Event[j]  not in Transition[i+1]:     #Event don't exist
                            Transition[i+1][Event[j]]=[]

                        if type(Transition[i+1][Event[j]])!=list:   # actual value not a list

                            Transition[i+1][Event[j]]=[Transition[i+1][Event[j]]]   #Convert into list

                        if INFO==0:
                            Transition[i+1][Event[j]].append(destination(MonDico,Next[0][I],Event[j]))#add new state to list
                        if INFO==1:
                            Transition[i+1][Event[j]].append(destination(MonDico,Next[0],Event[j]))#add new state to list
                        SortList(Transition[i+1][Event[j]])    

                        Transition[i+1][Event[j]]=ClearState(Transition[i+1][Event[j]])


                        if I == len(Next[0])-1: # last sub state of the state

                            if (Transition[i+1][Event[j]] not in Done) and (Transition[i+1][Event[j]] not in Next):     # New State, add to Next
                                if Transition[i+1][Event[j]] != "":
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
        Etat=EtatDico(Dictionnary)
        for i in range(len(Etat)):
            

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
        if len(List)==0:    # list empty -> no destination : ""
            #print("Error: the list is empty")
            return ""
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
            print("test",Etat,ETAT)
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

def ProductAutomatons(Dico1,Dico2):
    # Take as parameter two ditionnary
    # return False if at least one of them is empty
    # return False if they haven't the same aplhabet(list of event)
    # return the product of them if no error

    if DicoVide(Dico1)== True or DicoVide(Dico2)==True: # empty
        print("Error: at least one of the dictionnary is empty")
        return False
    
    EventDico1=EvenementDico(Dico1)
    EventDico2=EvenementDico(Dico2)
    EtatDico1=EtatDico(Dico1)
    EtatDico2=EtatDico(Dico2)
    Product={}

    if EventDico1 != EventDico2:    # Alphabet
        print("Error: automatons do not have the same alphabet")
        return False
    
    Event=EventDico1
    I=0

    # Create States
    for i in range(len(EtatDico1)): # Create States
        for j in range(len(EtatDico2)):
            Product[I]={}
            Product[I]["colonne"]=[]
            Product[I]["colonne"].append(EtatDico1[i])
            Product[I]["colonne"].append(EtatDico2[j])
            


            # Attribute type

            listEtatInitial1=listEtatInitial(Dico1)
            listEtatInitial2=listEtatInitial(Dico2)
            listEtatFinal1=listEtatFinal(Dico1)
            listEtatFinal2=listEtatFinal(Dico2)

            var=0
            State1=Product[I]["colonne"][0]
            State2=Product[I]["colonne"][1]

            if State1 in listEtatInitial1 and State2 in listEtatInitial2 and State1 in listEtatFinal1 and State2 in listEtatFinal2:
                Product[I]["type"]=3
            else:

                if State1 in listEtatInitial1 and State2 in listEtatInitial2:
                    Product[I]["type"]=1
                    var=1
                if State1 in listEtatFinal1 and State2 in listEtatFinal2:
                    Product[I]["type"]=2
                    var=1
                if var==0:
                    Product[I]["type"]=0
    
            # Destination state:
            for k in range(len(Event)):
                destination1=destination(Dico1,State1,Event[k])
                destination2=destination(Dico2,State2,Event[k])
                if destination1=="" or destination2=="":
                    Product[I][Event[k]]=""
                else:
                    Product[I][Event[k]]=[]
                    Product[I][Event[k]].append(destination1)
                    Product[I][Event[k]].append(destination2)



            I=I+1
    Product=ConvertDictionnaryListToStr(Product)
    AffichageAutomateFromDico(Product)
    return Product
#
#Status
# ok
#

def ConcatenationAutomatons(Dico1,Dico2):
    # take as parameters two dictionnary
    # return False if at least one of them is empty
    # return False if automatons have a common state
    # return False if the second automaton is not standard(cf VerifStatndard)
    # ask for confirmation before delete destination of finals states of the first automaton, return False if do not want to delete
    # if a state type is 3, in the first Dictionnary, return False( not sure)
    # return the concatenation of automatons 

    if DicoVide(Dico1)== True or DicoVide(Dico2)==True: # empty
        print("Error: at least one of the dictionnary is empty")
        return False
    
    if VerifAEF(Dico1)==False or VerifAEF(Dico2)==False:
        print("Error: automatons must be final state machine")
        return False


    EventDico1=EvenementDico(Dico1)
    EventDico2=EvenementDico(Dico2)
    EtatDico1=EtatDico(Dico1)
    EtatDico2=EtatDico(Dico2)
    Concatenation={}
    #check if no type 3 state in 1st dictionnary
    for i in range(len(Dico1)):
        if Dico1[i]["type"]==str(3):
            print("Error: invalid type for ",Dico1[i]["colonne"],"(3 not supported)")
            return False

    if VerifNoCommonStates(Dico1,Dico2) == False : # CommonStates
        print("Error: state in both automatons")
        return False
    
    if VerifStandard(Dico2)==False:
        return False
    EtatFinal=listEtatFinal(Dico1)
    EtatInitial=listEtatInitial(Dico2)


    ######################EVENT
    Event=[]
    for i in range(len(EventDico1)):
        Event.append(EventDico1[i])
    
    for i in range(len(EventDico2)):
        if EventDico2[i] not in Event:
            Event.append(EventDico2[i])
    ###################


    for i in range(len(Dico1)):
        if Dico1[i]["colonne"] in EtatFinal:        
            WHILE=0
            while WHILE==0:
                print(Dico1[i]["colonne"]," already has destination state, do you want to delete them?\n Warning, not delete them will stop the concatenation")
                a=input("(Yes/No):")
                match a.lower():
                    
                    #Yes
                    case "yes":
                        print("Deleted")
                        WHILE=1

                    case "no":
                        b=input("Are you sure? ")
                        if b.lower()=="yes":
                            return False
                    case _:
                        print("Expected answer is yes or no")
    
    for i in range(len(Dico1)):

        #initializing values
        Concatenation[i]={}
        Concatenation[i]["colonne"]=""
        Concatenation[i]["type"]=""

        for j in range(len(Event)):
            Concatenation[i][Event[j]]=""


        if Dico1[i]["colonne"] not in EtatFinal:        #not FinalState

            Concatenation[i]=Dico1[i]
            for k in range(len(Event)):

                if Event[k] not in EventDico1:

                    Concatenation[i][Event[k]]=""

        
        else:               #  Final State
            Concatenation[i]["colonne"]=Dico1[i]["colonne"] #state

            if Dico2[indexOfState(Dico2,EtatInitial[0])]['type'] == 3:    #type
                Concatenation[i]["type"]=2
            else:
                Concatenation[i]["type"]=0
            
            for j in range(len(Event)):     #destination
                if Event[j] in EventDico2:
                    Concatenation[i][Event[j]]=destination(Dico2,EtatInitial[0],Event[j])
                else:
                    Concatenation[i][Event[j]]=""
  
    for i in range(len(Dico2)):

        if Dico2[i]["colonne"] not in EtatInitial:
            J=len(Concatenation)
            Concatenation[J]={}
            Concatenation[J]["colonne"]=Dico2[i]["colonne"]
            Concatenation[J]["type"]=Dico2[i]["type"]
            for j in range(len(Event)):
                if Event[j] in EventDico2:
                    Concatenation[J][Event[j]]=Dico2[i][Event[j]]
                else:
                    Concatenation[J][Event[j]]=""

            
    
    return Concatenation
#
#Status
#OK
#
def VerifNoCommonStates(Dico1,Dico2):
    # Take as parameter two dicitonnary
    # return False if at least one is empty
    # return False if at least one states is in both dictionnary
    # return True if none of states of 1st dictionnary is equal to an states of the 2nd dictionnary

    if DicoVide(Dico1)== True or DicoVide(Dico2)==True: # empty
        print("Error: at least one of the dictionnary is empty")
        return False
    
    Etat1=EtatDico(Dico1)
    Etat2=EtatDico(Dico2)
    
    for i in range(len(Etat1)):
        if Etat1[i] in Etat2:
            return False
    
    return True

#
#Status
# OK
#

def VerifStandard(Dico):
    # take as parameter a dicitonnary
    # return False if the dictionnary is empty
    # return False if the Automaton is not standard
    # return True if the Automaton is standard

# a standard automaton is a automaton with only one initial state and where is it impossible to access to this state with a transition

    if DicoVide(Dico) == True:  # empty
        print("Error: empty dictionnary")
        return False
    
    if len(listEtatInitial(Dico)) > 1:  #multiple initial state
        print("Error: multiple initial states")
        return False
    

    for j in range(len(Dico)):
        for i in range(len(EvenementDico(Dico))):
            if Dico[j][EvenementDico(Dico)[i]] == listEtatInitial(Dico)[0] and Dico[j]["colonne"]==listEtatInitial(Dico)[0]:
                print("Error: existing transition to initial state")
                return False

    return True

#
#Status
# OK
#


def RegularExpression(Dico):
    # take as parameter a dctionnary
    # return False if the dictionnary is empty
    # return the regular expression from the automaton

    if DicoVide(Dico)==True:
        print("Error: empty automaton")
    
    # etablished system of equations
    Equation={}
    Final=listEtatFinal(Dico)
    for i in range(len(Dico)):
        Equation[i]=[]
        for j in range(len(EvenementDico(Dico))):
            Equation[i].append(Dico[i][EvenementDico(Dico)[j]])
        if Dico[i]["colonne"] in Final:
            final=1
        else:
            final=0
        Equation[i].append(final)

    print(Equation)
    #resolve system
#
#Status
# In progress
#


def ChangeToExcised(Dico):
    # take as parameter a dictionnary
    # return false if the dictionnary is empty, or not a final state machine
    # return the excised dictionnary

    if DicoVide(Dico)==True:
        print("Error: empty dictionnary")
        return False
    if VerifAEF(Dico)==False:
        print("Error: the automaton is not a final state machine")
        return False
    dictionnary={}
    State_CoAccess=[]
    size=0
    for i in range(len(Dico)):
        Done_State=[]
        if VerifAccess(Dico,Dico[i]["colonne"])==True and VerifCoAccess(Dico,Dico[i]["colonne"])==True:
            #print("State kept: ",Dico[i]["colonne"])
            dictionnary[size]=Dico[i]
            size=size+1

    return dictionnary
#   
#Status
# In progress
#

def VerifAccess(Dico,State):
    # take as parameter a dictionnary and a state
    # return false if empty dictionnary, state not in dictionnary
    # return False if not accessible state
    # return True if accessible state

    #Warning recursivity

    if DicoVide(Dico) == True:      # empty
        print("Error: empty Dictionnary")
        return False
    
    if State not in EtatDico(Dico):     #State in
        print("Error: state",State,"not in the automaton")
        return False

    Initial=listEtatInitial(Dico)
    parents=[]

    if State in Initial:    # initial => Accessible
        #print(State,"Accessible")
        return True

    for i in range(len(Dico)):  #find parents of the state
        for j in range(len(EvenementDico(Dico))):

            if type(Dico[i][EvenementDico(Dico)[j]])==str:          #case str
                if Dico[i][EvenementDico(Dico)[j]]==State and Dico[i]["colonne"]!=State:    # not include state itself as parent
                    parents.append(Dico[i]["colonne"])    


            if type(Dico[i][EvenementDico(Dico)[j]])==list:     # case list
                for k in range(len(Dico[i][EvenementDico(Dico)[j]])):
                    if Dico[i][EvenementDico(Dico)[j]][k]==State and Dico[i]["colonne"]!=State:     # not include state itself as parent
                        parents.append(Dico[i]["colonne"])



    for i in range(len(parents)):   # check if at least one parent is accessible
        if VerifAccess(Dico,parents[i])==True: # one parent is accessible
            #print(State,"Accessible")
            return True

    return False # None parent is Accessible

#    
#Status
# OK
#


def VerifCoAccess(Dico,State):
    # take as parameter a dictionnary and a state
    # return false if empty dictionnary, state not in dictionnary
    # return False if not coaccessible state
    # return True if coaccessible state

    #Warning recursivity

    if DicoVide(Dico) == True:      # empty
        print("Error: empty Dictionnary")
        return False
    
    if State not in EtatDico(Dico):     #State in
        print("Error: state",State,"not in the automaton")
        return False

    Final=listEtatFinal(Dico)
    dest=[]

    if State not in Done_State:
        Done_State.append(State)

    if State in Final:    # final => CoAccessible
        #print(State,"CoAccessible")
        State_CoAccess.append(State)
        return True


    for j in range(len(EvenementDico(Dico))): #find destinations of the state

        if type(Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]])==str:       # case str
            if Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]]!="" and Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]]!=State: # not include state itself as destination
                if Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]] not in Done_State or Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]] in State_CoAccess: # add condition with a global variable that contains list of coAccessible states
                    dest.append(Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]])


        if type(Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]])==list:          # case list
            for k in range(len(Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]])):        
                if Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]][k]!="" and Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]][k]!=State: # not include state itself as destination
                    if Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]][k] not in Done_State or Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]] in State_CoAccess: # add condition with a global variable that contains list of coAccessible states
                        dest.append(Dico[indexOfState(Dico,State)][EvenementDico(Dico)[j]][k])
                    

    for i in range(len(dest)):   # check if at least one destination is CoAccessible

        if VerifCoAccess(Dico,dest[i])==True:   # one destination is CoAccessible
            #print(State,"CoAccessible")
            State_CoAccess.append(State)
            return True
    #print(State,"not coaccessible",len(dest))
    return False    # none destination is CoAccessible

#    
#Status
# OK
#


def DemandeUser():
    # Retourne le choix de l'utilisateur qui doit impérativement etre un entier

    # On inerroge l'utilisateur
    DisplayChoices()
    A=input("\nYour choice:")

    while VerifEntier(A)==False:    # Tant que l réponse n'est pas un entier on boucle sur la question
        print("The expected answer is an integer")
        DisplayChoices()
        A=input("Your choice:")
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


def VerifMotAEF(Mot,MonDico):
    #Don't accept events with more than one character
    #
    #
    #



    if DicoVide(MonDico)==True:
        return False

    if VerifAEF(MonDico)==False:
        return False


    EtatI=listEtatInitial(MonDico)
    EtatF=listEtatFinal(MonDico)


    Mot=str(Mot)

        # se placer sur un etat initial
    for L in range(len(EtatI)): # pour chaque etat on verifie
            # si mot reconnu pour un des etat, le mot est reconnu donc on peut return True
        
        MonEtat=EtatI[L]
        if (Mot=='' and MonEtat in EtatF):
            return True
        for i in range(len(Mot)):
            print("test:",Mot[i])
            #verifier que le caractère i du mot est accepté pour faire une transition
            
            if type(destination(MonDico,MonEtat,Mot[i]))==str:      #case str
                if destination(MonDico,MonEtat,Mot[i])!="":
                    MonEtat=destination(MonDico,MonEtat,Mot[i])
                    b=0
                else:   #pas de destination
                    b=1
                    break
                print("test")
            if type(destination(MonDico,MonEtat,Mot[i]))==list:     #case list
                
                for k in range(len(destination(MonDico,MonEtat,Mot[i]))):
                    print(MonDico)
                    if destination(MonDico,MonEtat,Mot[i])[k]!="":
                        print("esai:",destination(MonDico,MonEtat,Mot[i]))
                        MonEtat=destination(MonDico,MonEtat,Mot[i])[k]
                        b=0
                        print("Mon état :",MonEtat)
                    else:   #pas de destination
                        b=1
                        
                        break
                    print("test2")
            
        if (MonEtat in EtatF and b==0): #bien un etat final 
            print("Youpi")
            return True 

    return False #invalide pour tous les etats initiaux


def ChoixAutomate(Dico1,Dico2):
    print("Two automatons are stored in the program.\nHere is the first automaton :")
    if DicoVide(Dico1)==True:
        print("The automaton is empty.")
    else:
        AffichageAutomateFromDico(Dico1)
    print("\nHere is the second automaton :")
    if DicoVide(Dico2)==True:
        print("THe automaton is empty.")
    else:
        AffichageAutomateFromDico(Dico2)
    a=input("What automaton would you like to choose ? (automaton1 or automaton2)\n")
    p=0
    while p==0:
        match a:

            case 'automaton1':
                print("You choose the first automaton")
                return Dico1
            case 'automaton2':
                print("You choose the second automaton")
                return Dico2
            case _:
                print("The automaton don't exist")
                a=input("Could you choose automaton1 or automaton2 ?\n")


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

def ComplementDico(Dico,mod=0): 
    if DicoVide(Dico)==True:
        print("Dictionnaire vide")
        return False
    if mod ==0:#return the dico with all types changed from final to non-final and vice-versa
        #type 0->2, type 1->3 type 2->0 type 3->1
        for i in range(len(Dico)):
            Type = int(Dico[i]["type"])
            if Type >=2:
                ReplaceType(Dico,i,(Type-2))
            else:
                ReplaceType(Dico,i,(Type+2))
    if mod ==1:#change final to initial and initial to final
        #type 1->2 and type 2->1
        for i in range(len(Dico)):
            Type = int(Dico[i]["type"])
            if Type ==1:
                ReplaceType(Dico,i,2)
            else:
                if Type == 2:
                    ReplaceType(Dico,i,1)
    return -1


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
    DicoFinal ={}
    for i in range(len(Dico)): #creating as many states as the original Automaton
        DicoFinal.setdefault(i,i) #create the element i in the dico
        DicoFinal[i]={} #i become a Dico
        DicoFinal[i]["colonne"]=Dico[i]["colonne"]  
        DicoFinal[i]["type"]=Dico[i]["type"]
    DicoFinal = ComplementDico(DicoFinal,1) #change all the types, only transitions to go 
    States = EtatDico(DicoFinal)
    for i in range(len(Dico)):
        for n in EvenementDico(Dico):
            if Dico[i][n]!="":
                DicoFinal[States.index(Dico[i][n])][n]=Dico[i]["colonne"]
    #.index give the position of the state we are going to in the list of possible states
    
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


    #Dictionnaire1=CSVToDico(FichierEntree)
    #Dictionnaire2=CSVToDico(FichierSortie)

    #print(VerifAccess(Dictionnaire1,"q0"))
    #print(VerifAccess(Dictionnaire1,"q1"))
    #print(VerifAccess(Dictionnaire1,"q2"))
    #print(VerifAccess(Dictionnaire1,"q3"))

    #Dictionnaire=ChangeToExcised(Dictionnaire1)
    #AffichageDico(Dictionnaire)
    #Dictionnaire = MiroirDico(Dictionnaire)
    #AffichageAutomateFromDico(Dictionnaire)
    Dictionnaire=CSVToDico("data4.csv")
    print(VerifMotAEF("ab",Dictionnaire))
    #ChoixAutomate(Dictionnaire,automaton)
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

            Dictionnary=ChoixAutomate(Dictionnaire,automaton)
            if DicoVide(Dictionnary)==True:
                print("Erreur: Aucun Automate n'est chargé en mémoire")
                wait()
            else:
                AffichageAutomateFromDico(Dictionnary)



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


        #Check word is admit
        case 11:
            print("\n-------------")
            print("Checking word")
            print("-------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:
                print("No Automaton in memory")
                wait()
            else:
                word=input("Input a word:")
                if VerifMotAEF(word,Dictionnaire) == False:
                    print("The word",word," is not admitted by the dictionnary")
                else:
                    print("The word",word,"is not admitted by the dictionnary")
                wait()

        #check determinist
        case 12:
            print("\n-----------------")
            print("Check determinist")
            print("-----------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifAEF(Dictionnaire)==True:    
                    if VerifDeterminism(Dictionnaire)==True:
                        print("The automaton is determinist")
                        wait()
                    else:
                        print("The automaton is not determinist")
                        wait()
                else:
                    print("The Automaton is not a final state machine")

        #Make determinist
        case 13:
            print("\n---------------")
            print("Determinisation")
            print("---------------\n")
            wait()

            if DicoVide(Dictionnaire)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifAEF(Dictionnaire)==True:
                    if VerifDeterminism(Dictionnaire)==True:
                        print("The automaton is already determinist")
                        wait()
                    else:
                        Dictionnaire=ChangeToDeterminist(Dictionnaire)
                        if Dictionnaire!= False:
                            print("Automaton succesfully determinised")
                            AffichageAutomateFromDico(Dictionnaire)
                        wait()
                else:
                    print("The Automaton is not a final state machine")
        
        #Find Complement
        case 14:
            print("\n----------")
            print("Complement")
            print("----------\n")  
            wait()

            if DicoVide(Dictionnaire)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifDeterminism(Dictionnaire)==True:
                    Dictionnaire=ComplementDico(Dictionnaire)
                    AffichageAutomateFromDico(Dictionnaire)
                    wait()
                else:
                    print("Error: non determinist automaton are not allowed")
        # Find Mirror
        case 15:
            print("\n------")
            print("Mirror")
            print("------\n")  
            wait()

            if DicoVide(Dictionnaire)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifDeterminism(Dictionnaire)==True:
                    Dictionnaire=MiroirDico(Dictionnaire)
                    AffichageAutomateFromDico(Dictionnaire)
                    wait()     
                else:
                    print("Error: non determinist automaton are not allowed")                      

        # product
        case 16:
            print("\n-------")
            print("Product")
            print("-------\n")
            wait()

        #######################ENVIRONNEMENT DEUX AUTOMATES +verif##############
            Dictionnaire1={}
            Dictionnaire2={}

            Dictionnaire=ProductAutomatons(Dictionnaire1,Dictionnaire2)
            AffichageAutomateFromDico(Dictionnaire)
            wait()
        

        # concatenation
        case 17:
            print("\n-------------")
            print("Concatenation")
            print("-------------\n")
            wait()

        #######################ENVIRONNEMENT DEUX AUTOMATES +verif##############
            Dictionnaire1={}
            Dictionnaire2={}

            Dictionnaire=ConcatenationAutomatons(Dictionnaire1,Dictionnaire2)
            AffichageAutomateFromDico(Dictionnaire)
            wait()
        
        #############################(18)-(19)-(20)


        # Excising
        case 17:
            print("\n-------------")
            print("Excising mode")
            print("-------------\n")
            wait()

            Dictionnaire=ChangeToExcised(Dictionnaire)
            AffichageAutomateFromDico(Dictionnaire)
            wait()



        #cas default
        case _:
            print("Invalid choice\n")
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




