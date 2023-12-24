

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
DEBUGG=0 #1 if we want to debugg, 0 else
Dictionnary={}
Dictionnary1={}
Dictionnary2={}
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


def AffichageDico(Dico):
    #take as parameter a dictionnary
    #print the dictionnary, index by index

    print("Dictionnary:")

    for i in range(len(Dico)):
        print(Dico[i],"\n")
    return 0
#
#status
#ok
#

def AffichageAutomateFromDico(Dico):
    # Take as parameter a dictionnary
    # Return False if it is empty
    # Return 0 and display the dictionnary like:
    # State:Event --> destination State

    if DicoVide(Dico)== True:
        print("Error: the dictionnary to print is empty")     
        return False

    else:

        print("Affichage sous la forme:\nETAT:évènement-->NouvelEtat\n")
        field=list(FIELDNAMES(Dico))
        for i in (range(len(Dico))):

            for j in range(1,len(field)):
                print(Dico[i][field[0]],":",field[j],"-->",Dico[i][list(FIELDNAMES(Dico))[j]])
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

def DicoToCSV(Dico,CSVFILES):
    # Take as parameters a dictionnary and a file name NEED ADD VERIFICATION OF THE EXTENSION(.csv)
    # Create the file if not already exist, delete the old file already exist
    # Return False if empty dictionnary 
    # Return 0 and write the dictionnary in the file

    if DicoVide(Dico)==True: # empty dictionnary
        print("Error: the dictionnary is empty")
        return False
        
    else:
        with open (CSVFILES,'w',newline="") as csvfiles:
            #Variables

            fieldnames=FIELDNAMES(Dico)  #keys of dictionnary (here:it is the first line of the csv file['colonne', 'type', 'A', 'B', 'C', 'D'])
            writer =  csv.DictWriter(csvfiles,fieldnames,delimiter=DELIMITER)

            #Writing
            writer.writeheader()
            for i in range(len(Dico)):
                writer.writerow(Dico[i])
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
    Dico={}
    State=[]    #List of states
    Type=[]    # List of Type associate to each State
    Event=[]    #List of Event
    
    #Variables that show if we have to stop user input
    a=1

    #Input States
    while a != 0:

        # Ask user
        Answer=input("Input a state (0 to stop):")

        if VerifEntier(Answer)==True : # The input can be convert as integer
            if int(Answer)==0:         # User want to stop input state
                a=0


            else:   #integer but not 0 so the state name is an integer(accepted)

                while VerifSaisieNewEtat(Answer,State)==False:  # Verify the input is correct

                    print("The name of the new state do not respect the conditions.\n"+CONDITIONS_ETAT)
                    Answer=input("New choice:")

                # We initialize Answer2 outside the list of accepted Type to access the while  
                Answer2=-1
                
                while VerifType(Answer2)==False :  # Verify the input Type is correct

                    Answer2=input("Input the type of the state"+Answer+" among: ordinary(0), initial(1), final(2) or   initial and final(3):")
                    if VerifType(Answer2)==False:
                        print("The type is not correct")

                # Now state and type are coorect, we can add them to lists
                Type.append(Answer2)
                State.append(Answer)


        else:                       #The input can't be converted to integer, the user want to continue input

            while VerifSaisieNewEtat(Answer,State)==False:  # Verify the input is correct

                print("The name of the new state do not respect the conditions.\n"+CONDITIONS_ETAT)
                Answer=input("New choice:")

            # We initialize Answer2 outside the list of accepted Type to access the while    
            Answer2=-1
            
            while VerifType(Answer2)==False : # Verify the input Type is correct

                Answer2=input("Input the type of the state "+Answer+" among: ordinary(0), initial(1), final(2) or   initial and final(3):")
                if VerifType(Answer2)==False:
                    print("The type is not correct")

            # Now state and type are coorect, we can add them to lists
            Type.append(Answer2)
            State.append(Answer)

    #Control Display
    print("The list of input's states:",State)
    print("The list of input's state's type:",Type,"\n")
    wait(0.4)


    # Input again, but for events, same variable a
    a=1

    # Input Event
    while a != 0:

        # Ask user
        Answer=input("Input an event (0 to stop):")

        if VerifEntier(Answer)==True : # The input can be convert as integer
            if int(Answer)==0:         # User want to stop input event
                a=0

            else:

                while VerifSaisieNewEvenement(Answer,Event)==False: # Verify the input is correct

                    print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                    Answer=input("New choice:")

                # Now the Eevnt is correct we can add it to his list    
                Event.append(Answer)


        else:                       #The input can't be converted to integer, the user want to continue input
            
            while VerifSaisieNewEvenement(Answer,Event)==False:    # Verify the input is correct

                print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                Answer=input("New choice:")

            # Now the Event is correct we can add it to his list
            Event.append(Answer)


    # Control Display      
    print("The list of input's events:",Event,"\n")
    wait(0.4)


    # Input Destination states
    print("Inserting destination's states:\nSynthax: State:Event-->destination's state")

    for i in range(len(State)):  # For each State

        Dico[i]={}     #Create the index in the dictionnary to access later VITAL
        Dico[i]["colonne"]=State[i]
        Dico[i]["Type"]=Type[i]

        for j in range(len(Event)):     #  For each Event
            check=0
            while check == 0:

                # Ask user
                Answer3=input(State[i]+":"+Event[j]+"-->")

                # Convert the answer into a list if two or more states
                Answer3=ListState(Answer3)
                Answer3=ClearState(Answer3)
                if type(Answer3)==str:
                    if VerifSaisieNouvelEtat(Answer3,State)==False:  # Verify the input is correct
                        print(Answer3,": the name of the state do not respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                    else:
                        check=2


                if type(Answer3)==list:
                    # We have to check if each member of the list is ok
                    check=1
                    print("\n")
                    wait()
                    for k in range(len(Answer3)):

                        if VerifSaisieNouvelEtat(Answer3[k],State)==False and check==1:
                            print(Answer3[k],": the name of the state do not respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                            check=0
                            break

            # Now input is ok, add to the dictionnary
            Dico[i][Event[j]]=Answer3
            

    return Dico

#
#status
#OK
#


def FIELDNAMES(Dico):
    # Take as paramter a dictionnary
    # Return False if empty dictionnary
    # return the list of the field (Ex:['colonne','Type','Event1','Event2'])

    if DicoVide(Dico)==True:
        return False

    else:
        return(Dico[0].keys())
        # We suppose the first state of our dictionnary have the maximum of possible keys
        #(ie, No other state have a keys, that the first state do not
#
#status
#ok
#
    
def ModifDico(Dico):
    # Take as parameter a dicitonnary
    # return False if the dictionnary is empty
    # return the new dictionnary

    if DicoVide(Dico)==True:
        print("Error: the dictionnary is empty")
        return False
    else:
        #Variables
        ListState=EtatDico(Dico)
        ListEvent=EvenementDico(Dico)

        OldListState=[]
        OldListEvent=[]

        # Copy content in backup list to compare 
        for i in range(len(ListState)):
            OldListState.append(ListState[i])
        
        for i in range(len(ListEvent)):
            OldListEvent.append(ListEvent[i])
        
        # Modify lists by asking user
        modifListeEtat(ListState)
        modifListeEvenement(ListEvent)

        # Delete unwanted states
        
        print("Removing unwanted states")
        wait()
        for i in range(len(OldListState)):
            if OldListState[i] not in ListState:      # state was here before, but not anymore          
                a=Dico.pop(i)


        # Add wanted states

        print("Adding new states")
        wait()


        for i in range (len(ListState)):
            Size=len(Dico)
            if ListState[i] not in OldListState:   # state was not here before 
                Dico.setdefault(Size+1,{'colonne':ListState[i]}) # add it to the dictionnary
        
        # Check if the dictionnary is sorted, if not sort it, in order to balance it 
        if VerifTrieDico(Dico)==False:
            Dico=TrieDicoCle(Dico)
    
        Dico=ConvertIndiceDico(Dico)  # Edit dictionnary to make index been succesives integers


        #Delete unwanted events

        print("Removing unwanted events")
        wait()

        for i in range(len(OldListEvent)):
            if OldListEvent[i] not in ListEvent: # event was here before, but not anymore
                for j in range(len(Dico)):
                        a=Dico[j].pop(OldListEvent[i]) # delete it   

        # Add wanted events

        print("Adding new events")
        wait()

        for i in range(len(ListEvent)):
            if ListEvent[i] not in OldListEvent: # event was not here before
                for j in range(len(Dico)): # add the event in each state of the dictionnary
                    Dico[j][ListEvent[i]]=""

        # Display the automaton and ask input for each destination state

        print("New fields in the automaton")
        print("State:Event-> destination's state")

        for i in range(len(Dico)):
            field=list(FIELDNAMES(Dico))
            
            
            # Edit type 
            print(Dico[i][field[0]],":",field[1],"-->",Dico[i][list(FIELDNAMES(Dico))[1]])
            Answer=input("Input the type of the state "+Dico[i][field[0]]+" among: ordinary(0), initial(1), final(2) or    initial and final(3) (Enter to skip):")

            while VerifType(Answer)==False and Answer!="": # We check if the type respect conditions, if empty keep the old value
                    print("The type is not correct")
                    Answer=input("Input the type of the state "+Dico[i][field[0]]+" among: ordinary(0), initial(1), final(2) or   initial and final(3) (Enter to skip):")
            if Answer != "":
                Dico[i][list(FIELDNAMES(Dico))[1]]=Answer

            # Edit destination state
            for j in range(2,len(field)):
                check=0
                while check==0:
                    print(Dico[i][field[0]],":",field[j],"-->",Dico[i][list(FIELDNAMES(Dico))[j]])
                    Answer=input("Enter a new destination state (Enter to skip):")
                    Answer=ListState(Answer)
                    Answer=ClearState(Answer)

                    if type(Answer)==str:
                        if VerifSaisieNouvelEtat(Answer,EtatDico(Dico))== False:
                            print("The name of the state do no respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                        else:
                            check=2
                            if Answer != "":
                                #print("test")
                                Dico[i][list(FIELDNAMES(Dico))[j]]=Answer

                    if type(Answer)==list:
                        check=1
                        print("\n")
                        wait()
                        for k in range(len(Answer)):
                            if VerifSaisieNouvelEtat(Answer[k],EtatDico(Dico))==False and check==1:
                                print(Answer[k],": the name of the state do not respect conditions.\n"+CONDITIONS_NOUVEL_ETAT)
                                check=0
                                break

                            else:
                                print(Answer[k],"Correct")
                               
                if type(Answer)==list and Answer[k]!="":
                    Dico[i][list(FIELDNAMES(Dico))[j]]=Answer

        return Dico

#
#Status   
#OK
#


def EquilibrageDico(Dico):
    # take as parameter a dictionnary
    # return - if the dictionnary is empty
    # return the dictionarry with reorganized index 
    #
    #Need to check if the keys of the dictionnary are sorted (function VeriTrieDico() and TriDicoCle())

    # Suppr is a list containing index that must be delete from our dictionnary
    Suppr=[]

    
    if DicoVide(Dico)==True:
        return -1

    else:
        if VerifTrieDico(Dico)==False:
            Dico=TrieDicoCle(Dico)
        
        for i in range(len(list(Dico.keys()))):   
            if list(Dico.keys())[i]!=i:   # Check if each index is correctly named, else named it correctly 
 
                OldValue=list(Dico.values())[i] # identify which index we have to remove

                Dico.setdefault(i,OldValue) # add new key et attribute the corresponding value, careful: index added at the end

                if i not in Suppr: # we add the index only if this index is not attributed
                    Suppr.append(list(Dico.keys())[i])

        for i in range(len(Suppr)): # delete unwanted index
            a=Dico.pop(Suppr[i])

    return Dico
#
#Status
#OK
#

def ConvertIndiceDico(Dico):
    # Take as parameter a dictionnarie
    # return False if the dictionnary is empty
    # return the dictionnary with index converted successively

    if DicoVide(Dico)==True:
        print("Error: the dictionnary is empty")
        return False
    else:
        FinalDico={}
        for i in range(len(Dico.keys())):
            FinalDico[i]=Dico[list(Dico.keys())[i]]
    return FinalDico
#
#Status
#ok
#




def TrieDicoCle(Dico):
    # Retourne -1 si le dictionnaire est vide
    # Retourne le dictionnaire trié sinon

    if DicoVide(Dico):
        return -1
    
    else:
        Dico=sorted(Dico.items(),key=lambda t:t[0])
        #Here it's a list not a dictionnary, let's convert it

        FinalDico={}

        for i in range(len(Dico)):
            FinalDico[Dico[i][0]]=Dico[i][1]
        return FinalDico
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


def modifListeEtat(ListeState):
    # Take as parameter liste of state 
    # Return the new new, edited by user

    if len(ListeState) == 0:    #Empty list
        print("The list is empty")
        return False

    else:        
        #Variables to know when stop
        stop = 0

        while stop == 0:

            # Ask user
            answer =input(str(ListeState)+"\nDo you want to edit the state's list above (yes or no):")
            # Convert to lower
            answer=answer.lower()

            # many case depending of answer
            match answer:

                # User want to edit
                case "yes":

                    print("Edit")
                    answer2=input("Insert the name of the state to edit or remove it and insert the new name to add it:")

                    # Check answer is correct:
                    while VerifSaisieEtat(answer2)==False:
                        print("The name do not respect conditions.\n"+CONDITIONS_ETAT)
                        answer2=input("New choice:")
                    # Answer is now correct 

                    if answer2 in ListeState:   # State already exist
                        Choice=input("Choosen state: "+answer2+" Do you want to remove(0) or edi(1) it:")

                        # Check field 'Choice'
                        while VerifEntier(Choice)==False or int(Choice) not in [0,1]:
                            print("The expected answer is 0 or 1")
                            Choice=input("Choosen state: "+answer2+" Do you want to remove(0) or edit(1) it:")

                        if int(Choice)==0:
                            # Erasing
                            ListeState.remove(answer2)
                        
                        else:
                            # Edit
                            new=input("Insert the new state:")

                            # Check field 'new'
                            while VerifSaisieNewEtat(new,ListeState)==False:
                                print("The name do not respect conditions.\n"+CONDITIONS_ETAT)
                                new=input("New choice:")
    
                            ListeState=ModifListe(answer2,ListeState,new)
                    else:
                        # Adding
                        ListeState.append(answer2)



                # No more changes
                case "no":

                    print("End of edit")
                    wait()
                    # edit value of stop variable to exit
                    stop=1
                
                # other answer
                case _:
                    print("The expected answer is yes or no")

        return ListeState
#
#Status
#OK
#


def modifListeEvenement(ListeEvent):
    # Take as parameter list of event
    # Return the new list, edited by user

    if len(ListeEvent) == 0:    # Empty list
        print("The list is empty")
        return False

    else:        
        # Varaiables to know when stop
        stop = 0

        while stop == 0:
            # Ask user
            answer =input(str(ListeEvent)+"\nDo you want to edit the event list above (yes or no):")
            
            # Convert to lower
            answer=answer.lower()

            # Many case depending on th answer 
            match answer:

                # user want to edit
                case "yes":

                    print("Edit")
                    answer2=input("Insert the name of the event to edit or remove it and insert the new name to add it:")

                    # Check answer is correct:
                    while VerifSaisieEvenement(answer2)==False:
                        print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                        answer2=input("New choice:")
                    # field is now correct 
                    
                    if answer2 in ListeEvent:   # Event already exist
                        Choice=input("Choosen event: "+answer2+" Do you want to remove(0) or edit(1) it:")

                        # Check field 'Choice' is correct
                        while VerifEntier(Choice)==False or int(Choice) not in [0,1]:
                            print("The expected answer is 0 or 1")
                            Choice=input("Choosen event"+answer2+" Do you want to remove(0) or edit(1) it:")

                        if int(Choice)==0:
                            # Erasing
                            ListeEvent.remove(answer2)
                        
                        else:
                            # Edit
                            new=input("Insert the new event:")

                            # Check field 'new' is correct
                            while VerifSaisieNewEvenement(new,ListeEvent)==False:
                                print("The name of the event do not respect conditions.\n"+CONDITIONS_EVENEMENT)
                                new=input("New choice:")


                            ListeEvent=ModifListe(answer2,ListeEvent,new)


                    else:
                        #Ajout
                        ListeEvent.append(answer2)



                # No more edit
                case "no":

                    print("End of edit")
                    wait()
                    # Change value of variable stop to exit
                    stop=1
                

                # Other answer
                case _:
                    print("The expected answer is yes or no")

        return ListeEvent
#
#Status
#OK
# 




def ModifListe(old,List,new):
    # Take as parameter list and two variables, one already in the list and one to replace the old one
    # Return the edited list

    if len(List)!= 0:      # Check empty list

        for i in range(len(List)): 
            if List[i]==old:    # Cross list to find the old value
                List[i]=new    # Replace by new value
                return  List

    else:

        print("Error: the list is empty")
        return False     
#
#status
#OK
#


def DicoVide(Dico):
    # Take as parameter a Dictionnary
    # Return True if the Dictionnary is empty
    # Return False if the Dictionnary is not empty
    # Return -1 if type of parameter is incorrect

    if type(Dico)!=dict: # type
        print("Error: the type expected is dictionnary")
        return -1    

    if not Dico:
        
        return True     # Empty Dictionnary

    else:
        return False    # Not empty Dictionnary
#
#status
#ok
#


def FichierVide(CSVFILES):
    # Take as parameter a file name
    # Return True if the file is empty
    # Return False if the file is not empty
    # Return -1 if the file does not exist

    # Check existing file
    if FichierExiste(CSVFILES)==False:

        print("Error: the file do not exist")
        return -1
    
    else:
            
        # Look at size of the file
        size=os.stat(CSVFILES).st_size
        if size == 0:
            
            return True     # Empty file

        else:
            return False    # File not empty
#
#status
#ok
#


def FichierExiste(CSVFILES):
    # Take as parameter a file name
    # Return True if the file do exist
    # Return False if the file do not exist

    if os.path.exists(CSVFILES):    # look for path where file is valide
        return True     # File exist

    else:
        
        return False    # File not exist
#
#status
#ok
#

def VerifType(Type):
    # Take as parameter a type (0,1,2,3) of state
    # Return True if the Type is correct
    # Return False if the Type is incorrect

    if VerifEntier(Type)==True:    # Type var is an integer

        if int(Type) in TYPE:      # Type is correct         #TYPE is global var defined before

            return True

    return False     # Type incorrect
#
#status
#ok
#

def VerifEntier(var):
    # Take as parameter a variable
    # Return True if parameter can be converted to integer
    # Return False if parameter cannot be converted to integer

    try:    # Try to convert to integer
        int(var)

    except ValueError:  # If error while convertion -> var can't be converted
        return False    # Cannot be converted

    else:               # If no error -> var can be converted safely
        return True # Can be converted
#
#status
#ok
#

def VerifAEF(Dico):
    # Take as parameter a dictionnary
    # Return True if the dictionnary do show a Final State Machine(FSM)
    # Return False if the dictionnary do not show a Final State Machine(FSM)
    # Return -1 if empty of incorrect parameter
    
    if DicoVide(Dico)==True:    #empty
        print("Automaton is empty")
        return -1

    else:
        # Define list of states and events
        State=EtatDico(Dico)
        Event=EvenementDico(Dico) 
           
        for i in range(len(Dico)):   # Cross states   
            for j in range(len(Event)): # Cross events 
                
                # case of a list of states
                if type(Dico[i][Event[j]])==list:
                    for k in range(len(Dico[i][Event[j]])):
                        if Dico[i][Event[j]][k] not in State and Dico[i][Event[j]][k]!="":
                            return False

                # case of a single state
                if type(Dico[i][Event[j]])==str:
                    if Dico[i][Event[j]] not in State and Dico[i][Event[j]]!="":   # Check if a field already has a state or is empty
                        return False                    

        # If arrive here: every fields are state or empty --> FSM
        return True          
#
#status
#OK
#

def VerifSaisieNewEtat(Choice,ListState):
    # Take as parameter a user choice and a list of state
    # return False if input not correct
    # return True if input is correct
    # return -1 if parameters are incorrect

    if Choice == "":    # Empty input 
        return -1
    if len(ListState)==0:   # empty list
        return -1
    else:
        if Choice in ListState:                                      # check state do not already exist   
            print("This state already exist")
            return False

        for i in range(len(RESTRICTION_CHOIX_ETAT)):
            if RESTRICTION_CHOIX_ETAT[i] in Choice:                  # Check no forbidden caracter used
                return False

        return True
#
#status
#OK
#


def VerifSaisieEtat(Choice):
    # Take as parameter a user choice 
    # difference with VerifSaisieNewEtat:  we can choose a field that do not already exist
    # return False if input not correct
    # return True if input is correct
    # return -1 if parameters are incorrect

    if Choice == "":    # empty input 
        return -1

    else:

        for i in range(len(RESTRICTION_CHOIX_ETAT)):
            if RESTRICTION_CHOIX_ETAT[i] in Choice:                  # Check no forbidden caracter used
                return False

        return True
#
#status
#OK
#



def VerifSaisieNewEvenement(Choice,ListEvent):
    # Take as parameter a user choice and a list of event
    # return False if input not correct
    # return True if input is correct
    # return -1 if parameters are incorrect

    if Choice == "":    #empty input 
        return -1
    if len(ListEvent)==0:   # empty list
        return -1

    else:
        if Choice in ListEvent:                                 # Check the event do not already exist  
            print("This event already exist")                      
            return False

        for i in range(len(RESTRICTION_CHOIX_EVENEMENT)):       
            if RESTRICTION_CHOIX_EVENEMENT[i] in Choice:             # Check no forbidden caracter used
                return False

        return True
#
#status
#OK
#


def VerifSaisieEvenement(Choice):
    # Take as parameter a user choice 
    # difference with VerifSaisieNewEvennement:  we can choose a field that do not already exist
    # return False if input not correct
    # return True if input is correct
    # return -1 if parameters are incorrect

    if Choice == "":    #Empty input 
        return -1

    else:

        for i in range(len(RESTRICTION_CHOIX_EVENEMENT)):       
            if RESTRICTION_CHOIX_EVENEMENT[i] in Choice:             # Check no forbidden caracter used
                return False

        return True
#
#status
#OK
#


def VerifSaisieNouvelEtat(Choice,listState):
    # Take as parameter a user choice and a list of state
    # return False if input not correct
    # return True if input is correct as destination state
    # return -1 if parameters are incorrect

    if Choice == "":    # empty input 
        return -1
    if len(listState)==0:   # empty list
        return -1

    else:

        for i in range(len(RESTRICTION_CHOIX_NOUVEL_ETAT)):       
            if RESTRICTION_CHOIX_NOUVEL_ETAT[i] in Choice:             # Check no forbidden caracter used
                return False

        if Choice in listState:                           # the new state already exist 
            return True

        else:                                               # the new state do not already exist
            return False
    
    return False

#
#status
#OK
#

def VerifTrieDico(Dico):
    # Take as parameter a dictionnary
    # Return True if keys are sorted
    # Return False if keys are not sorted
    # Return -1 if error with dictionnary(empty or wrong type)

    if DicoVide(Dico):  
        return -1

    else:

        # use keys of dictionnary
        Mylist=list(Dico.keys())

        # define a sorted list
        SortedList=sorted(Mylist)
        
        # Compare 
        if Mylist==SortedList: 
            return True

        else:
            return False
#
#Status
#OK
#

def VerifDeterminism(Dico):
    # Take as parameter a dictionnary
    # return True if the automaton is determinist
    # return False if the automaton is not determinist
    # Return -1 if error with dictionnary(empty or wrong type) 

    if DicoVide(Dico):
        return -1
    else:
        #Testing the startingState's list's lenght is 1 ###utiliser la fonction de guillaume
        if len(listEtatInitial(Dico))!=1:
            return False
        
        #Testing there is no list of state 
        Event=EvenementDico(Dico)
        for i in range(len(Dico)):
            for j in range(len(Event)):
                Value=Dico[i][Event[j]]
                if type(Value) == list:
                    return False
        return True
    
#
#Status
# OK
#   



def ChangeToDeterminist(Dico):
    # Function that take in parameters a dictionnary
    # Return an equivalent of the automaton but determinist
    # Return False if the dictionnary in parameter is empty
    # Return False if there is no initial state
    # Return the automaton if the automaton is already determinist

    if DicoVide(Dico)==True:

        return False

    else:   
        Info=0
        
        if VerifDeterminism(Dico)==True:     #already determinist

            print("Already determinist")
            return Dico

        Transition= {}

        Transition[0]={}

        match len(listEtatInitial(Dico)):

            case 0:     #no initial state
                return False

 

            case 1:     #only one initial state
                for i in range(len(Dico)):

                    if Dico[i]["colonne"]==listEtatInitial(Dico)[0]:  #putting initial state in new dictionnary

                        Transition[0]=Dico[i]
                        Info=1
                if len(Transition[0])==0:   #empty dictionnary created
                    return False

            case _:     #more than one

                #initializing new initial state as list:
                New_State=[]
                Type=[]

                for i in range(len(listEtatInitial(Dico))): #adding this state(and type) to the list
                    New_State.append(listEtatInitial(Dico)[i])
                    Type.append(TypeOfState(Dico,listEtatInitial(Dico)[i]))

                #Initializing variables 
                Initial=listEtatInitial(Dico)
                Event=EvenementDico(Dico)
                AddState(Dico,New_State,1,"")    #adding the new initial state to the old dictionnary
                
                
                #-----------creating a tmp dictionnary of state--------



                Transition[0]["colonne"]=New_State
                Transition[0]["type"]=UpdateTypeL(Type,0)

                for i in range(len(Initial)):  
                    Type.append(TypeOfState(Dico,Initial[i]))    #adding type to the list
                    
                    for j in range(len(Event)):
                        if Event[j] in Transition[0]:       # Event already exist in dictionnary

                            Transition[0][Event[j]].append(destination(Dico,Initial[i],Event[j]))    #add new state
                            SortList(Transition[0][Event[j]])

                        else:           # new event, create it and add value
                            Transition[0][Event[j]]=[]
                            Transition[0][Event[j]].append(destination(Dico,Initial[i],Event[j]))




        #------------------ordinary states---------------------

        #initializing variables

        Next=[] # State to process
        Done=[Transition[0]["colonne"]] # States already processed
        State=EtatDico(Dico)
        Event=EvenementDico(Dico)
        for j in range(len(Event)):  
            if Transition[0][Event[j]] not in Done:     # adding states to process
                Next.append(Transition[0][Event[j]])

        #each state was correctly added

        #process next states

        i=0
        while len(Next) != 0 :      #while a state to process
            #initializing variables
            type1=[]
            STATE=EtatDico(Transition)
            EVENT=EvenementDico(Transition)

            if Next[0] in STATE:     # if already process, go to the next one
                i=i+1
                
            else:
                if i+1 not in Transition:     #initializing if new index
                    Transition[i+1]={"colonne":"","type":""}

                for I in range(len(Next[0])):
                    if type(Next[0])==list:
                        type1.append(TypeOfState(Dico,Next[0][I]))   #add type of each sub-state too the list
                        INFO=0

                    else :
                        type1.append(TypeOfState(Dico,Next[0]))
                        INFO=1
                    for j in range(len(Event)):

                        if Event[j]  not in Transition[i+1]:     #Event don't exist
                            Transition[i+1][Event[j]]=[]

                        if type(Transition[i+1][Event[j]])!=list:   # actual value not a list
                            Transition[i+1][Event[j]]=[Transition[i+1][Event[j]]]   #Convert into list

                        if INFO==0:
                            Transition[i+1][Event[j]].append(destination(Dico,Next[0][I],Event[j]))#add new state to list
                        if INFO==1:
                            Transition[i+1][Event[j]].append(destination(Dico,Next[0],Event[j]))#add new state to list
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
        State=EtatDico(Dictionnary)
        for i in range(len(State)):
            

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

def indexOfState(Dico,State):
    # Take in parameter a dictionnary and a state
    # Return False if the dictionnary is empty or if the state is not in the dictionnary
    # Return the index of the State if the state is in the dictionnary

    STATE=EtatDico(Dico)

    if DicoVide(Dico)==True:
        print("Error: the dictionnary is empty")
        return False

    else:

        if State not in STATE:
            print("Error: the state is not in this dictionnary")
            return False

        else:
            for i in range(len(Dico)):
                if Dico[i]["colonne"]==State:
                    return i
            
            print("Error: the state is not in this dictionnary")
            return False
#
#Status
# OK
#

def TypeOfState(Dico,State):
    # Take in parameter a Dictionnary and a state
    # Return False if the dictionnary is empty or the state is not in the dictionnary
    # Return the type of the state if it is in the dictionnary

    STATE=EtatDico(Dico)
    if DicoVide(Dico)==True:
        print("Error: Empty dictionnary")
        return False

    else:
        if State not in STATE:
            print("Error: the state is not in this dictionnary")
            return False

        else:
            for i in range(len(Dico)):
                if Dico[i]["colonne"]==State: 
                    return Dico[i]["type"]

            print("Error: the state is not in this dictionnary")
            return False

#
#Status
#ok
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

def destination(Dico,state,Event):
    # Take as parameter a dictionnary, a state and an event
    # Return the destination state of the state with the event in the automaton
    # Return False if empty Dictionnary or unexistant state or event
 

    if DicoVide(Dico):
        print("Error: empty Dictionnary")
        return False
        
    Return=[]
    for i in range(len(EtatDico(Dico))):
        if state == EtatDico(Dico)[i] and Event in EvenementDico(Dico):
            Return=Dico[i][Event]
            
            return Return

    # unkonwn event or state:
    print("unknown event or state",state,"event:",Event)
    return False
#
#Status
# Ok
#

def EtatDico(Dico):
    # Take as parameter a dictionnary
    # Return list of state
    # Return False if empty Dictionnary

    if DicoVide(Dico)==True:
        print("Error: the automaton is empty")
        return False
        
    else:
        state=[]
        for i in range(len(Dico.keys())):
            state.append(Dico[list(Dico.keys())[i]]['colonne'])
        return(state)
#
#status
#ok
#     

def EvenementDico(Dico):
    # Take as parameter a dictionnary
    # Return list of event
    # Return False if empty Dictionnary
    
    if DicoVide(Dico)==True:
        print("Error: the automaton is empty")
        return False
        
    else:
        event=list(Dico[0].keys()) # First ligne, without first value
        Event=[]
        for i in range(2,len(event)):   # Start at 2 to not add 'colonne' and 'type'
            Event.append(event[i])
        return Event
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

        if dest[i] in State_CoAccess or VerifCoAccess(Dico,dest[i])==True:   # one destination is CoAccessible
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
    # Return user choice , as en integer

    # Ask user
    DisplayChoices()
    Choice=input("\nYour choice:")

    while VerifEntier(Choice)==False:    # While answer incorrect, try again
        print("The expected answer is an integer")
        DisplayChoices()
        Choice=input("Your choice:")
    return int(Choice)

#
#status
#ok
#

def choixFichier(mode,FileName): 
    # Check entry file: mode=1
    # Check exit file: mode=2

    # Take as parameter the mode(1 or 2) and the file name
    # Return the file name after checkings
    # Return -1 if parameters are incorrects

    # No need to check if we can convert var 'mode' because not set by user
    match int(mode):
        
        #entry file mode
        case 1:
            
            # Check file exist and not empty
            while FichierExiste(FileName)==False or FichierVide(FileName)==True:        
                FileName=input("Empty file or unexisting file, try another:")
            print("File OK")
            return FileName


        # exit file mode
        case 2:

            if FichierExiste(FileName)==False:    # unexisting file 
                print("No corresponding file, creating new file")
                    # To create a file using python, open it in writing mode

            else:   #File already exist, content will be deleted
                print("File OK")
                wait()
            return FileName

        case _:
            print("Error when calling choixFichier()")
            return -1
            # Error call function
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


    b=0
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
            print("destination",destination(MonDico,MonEtat,Mot[i]))
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
                    #print(MonDico)
                    print("len:",len(destination(MonDico,MonEtat,Mot[i])),(destination(MonDico,MonEtat,Mot[i])))
                    if destination(MonDico,MonEtat,Mot[i])[k]!="":
                        print("essai:",destination(MonDico,MonEtat,Mot[i]))
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
        print("The automaton is empty.")
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


def StockageAutomate(NewDico,Dico1,Dico2):
    #Take as parameter three dictionnary
    #This function serve to save the automaton that the user is using in one of the predefined variables in the program
    #If the automaton that the user choose is already used the program asks him if he is sure that he want to overwrite the automaton
    #Return Dico1 if the user save the his automaton in the variable Dico1
    #Return Dico2 if the user save the his automaton in the variable Dico2

    a=input("In which automaton would you like to stock your automaton ? (automaton1 or automaton2)\n")
    p=0
    while p==0:
        match a:

            case 'automaton1':
                print("You choose the first automaton \n")
                if DicoVide(Dico1)==False:
                    print("This automaton is already used \n")
                    choice=input("Are you sure you want to overwrite this automaton ? (y or n)\n")
                    v=0
                    while v==0:
                        match choice:

                            case 'y':
                                Dico1=NewDico
                                return "Dico1"
                            case 'n':
                                a=input("In which automaton would you like to stock your automaton ? (automaton1 or automaton2)\n")
                                v=1
                            case _:
                                choice=input("Could you choose y or n ?\n")
                else:
                    Dico1=NewDico
                    return "Dico1"

            case 'automaton2':
                print("You choose the second automaton")
                if DicoVide(Dico1)==False:
                    print("This automaton is already used \n")
                    choice=input("Are you sure you want to overwrite this automaton ? (y or n)\n")
                    v=0
                    while v==0:
                        match choice:

                            case 'y':
                                Dico2=NewDico
                                return "Dico2"
                            case 'n':
                                a=input("In which automaton would you like to stock your automaton ? (automaton1 or automaton2)\n")
                                v=1
                            case _:
                                choice=input("Could you choose y or n ? \n")
                else:
                    Dico2=NewDico
                    return "Dico2"

            case _:
                print("The automaton don't exist")
                a=input("Could you choose automaton1 or automaton2 ?\n")


def replaceAutomatonMemory(Dico):
    # take as parameter a Dictionnary
    # replace the dictionnary in the memory in the right variable
    # return False if parameter is empty or wrong
    # return True if everything is okay at the end
    
    global Dictionnary
    global Dictionnary1
    global Dictionnary2

    if DicoVide(Dico):
        print("Error: empty Dictionnary")
        return False
    
    DicoChoose=StockageAutomate(Dico,Dictionnary1,Dictionnary2)
    if DicoChoose=='Dico1':
        Dictionnary1=Dico
        Dictionnary=Dictionnary1
        return True
    else:
        Dictionnary2=Dico
        Dictionnary=Dictionnary2
        return True
    
#
#Status 
#OK
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

def ComplementDico(Dico,mod=0): 
    if DicoVide(Dico)==True:
        print("Error: empty dictionnary")
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


    Dictionnaire1=CSVToDico("data3.csv")
    Dictionnaire2=CSVToDico("data4.csv")
    Dictionnaire=CSVToDico("data.csv")

    
    #print(StockageAutomate(Dictionnaire,Dictionnaire1,Dictionnaire2))
    #Dictionnaire=ConcatenationAutomatons(Dictionnaire1,Dictionnaire2)
    #AffichageAutomateFromDico(Dictionnaire)
    ARRET = 1

#
#------------------------------------
#------------------------------------
#------------------------------------
#

while ARRET == 0:
    
    ChoixUser=DemandeUser()
    time.sleep(0.8)
    match ChoixUser:
        
        #Stop
        case 0:
            print("----------")
            print("Shutdown")
            print("----------")
            ARRET=1

        #Loading automaton from .csv
        case 1:
            print("\n---------------------------")
            print("Loading Automaton from file")
            print("---------------------------\n")
            

            #choose file 
            Fichier=input("Choose a file name:")

            #check existing file
            FichierEntree=choixFichier(1,Fichier)
            Dico=CSVToDico(FichierEntree)

            if replaceAutomatonMemory(Dico)==False:
                break


            if DicoVide(Dictionnary)==False:
                print("Automaton successfully loaded")
                wait()
    
            else:
                print("Empty Automaton, an error occured")
                wait()
            

        #Display automaton from .csv    
        case 2:
            print("\n---------------------------")
            print("Display Automaton from file")
            print("---------------------------\n")
            wait()

            #choose file 
            Fichier=input("Input file name:")

            #check existing file
            FichierEntree=choixFichier(1,Fichier)

            AffichageAutomateFromCSV(FichierEntree)
            


        #Display automaton in memory
        case 3:
            print("\n---------------------------")
            print("Display Automaton in memory")
            print("---------------------------\n")
            wait()

            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("Error: no Automaton in memory")
                wait()
            else:
                AffichageAutomateFromDico(Dictionnary)



        #Register automaton as csv
        case 4:
            print("\n------------------------------------------")
            print("Register Automaton in memory in a csv file")
            print("------------------------------------------\n")
            wait()

            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)

            if DicoVide(Dictionnary)==True:
                print("Error: no Automaton in memory")
                wait()

            else:
                #Choose destination file
                Fichier=input("Input file name:")

                #Check existing file
                FichierSortie=choixFichier(2,Fichier)
            
            #confirmation if not empty ?
                if DicoToCSV(Dictionnary,FichierSortie) == 0:
                    print("Successfully registered")
                    wait()
                else:
                    print("Error while registering")
                    wait()

        #Delete automaton in memory
        case 5:         # a faire
            print("\n---------------------------")
            print("Erasing Automaton in memory")
            print("---------------------------\n")
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            Dictionnary={}#Replace by empty dictionnary
            print("Automaton erase")
            wait()


        #Create a new automaton
        case 6:
            print("\n----------------------")
            print("Create a new Automaton")
            print("----------------------\n")
            wait()

            Dictionnary=CreationDico()
            if VerifAEF(Dictionnary)==False:
                print("Error while creating")
                wait()
            else:
                print("Automaton successfully created")
                wait()

                DicoChoose=StockageAutomate(Dico,Dictionnary1,Dictionnary2)
                if DicoChoose=='Dico1':
                    Dictionnary1=Dico
                    Dictionnary=Dictionnary1
                else:
                    Dictionnary2=Dico
                    Dictionnary=Dictionnary2
         
                AffichageAutomateFromDico(Dictionnary)


        #Edit an automaton
        case 7:
            print("\n--------------------------")
            print("Edit an Automaton")
            print("--------------------------\n")
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                ModifDico(Dictionnary)


        #Check if an Automaton is a FSM(final state machine) 
        case 8:
            print("\n---------")
            print("Check FSM")
            print("---------\n")
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:    #Empty
                print("No Automaton in memory")
                wait()
            else:       #existing Automaton
                match VerifAEF(Dictionnary):
            
                    #Automaton is FSM
                    case True:
                        print("The Automaton is a Final State Machine")
                        wait()
                    
                    #Automaton is not FSM
                    case False:
                        print("The Automaton is not a Final State Machine")
                        wait()

                    #default case
                    case _: 
                        print("Error: probleme occurend while checking")
                        wait()
                    
                    

        #verify if an automaton is complete
        case 9:
            print("\n---------------------")
            print("Complete Verification")
            print("---------------------\n")
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:    #No automaton in memory
                print("No Automaton in memory")
                wait()
            else:
                match VerifComplet(Dictionnary):
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
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:    #No automaton in memory
                print("No Automaton in memory")
                wait()

            else:
                Dictionnary = ChangeToComplet(Dictionnary)
                print("done \n")
                wait()


        #Check word is admit
        case 11:
            print("\n-------------")
            print("Checking word")
            print("-------------\n")
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                word=input("Input a word:")
                if VerifMotAEF(word,Dictionnary) == False:
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
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifAEF(Dictionnary)==True:    
                    if VerifDeterminism(Dictionnary)==True:
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
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifAEF(Dictionnary)==True:
                    if VerifDeterminism(Dictionnary)==True:
                        print("The automaton is already determinist")
                        wait()
                    else:
                        Dictionnary=ChangeToDeterminist(Dictionnary)
                        if Dictionnary!= False:
                            print("Automaton succesfully determinised")
                            AffichageAutomateFromDico(Dictionnary)
                        wait()
                else:
                    print("The Automaton is not a final state machine")
        
        #Find Complement
        case 14:
            print("\n----------")
            print("Complement")
            print("----------\n")  
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifDeterminism(Dictionnary)==True:
                    Dictionnary=ComplementDico(Dictionnary)
                    AffichageAutomateFromDico(Dictionnary)
                    wait()
                else:
                    print("Error: non determinist automaton are not allowed")
        # Find Mirror
        case 15:
            print("\n------")
            print("Mirror")
            print("------\n")  
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                if VerifDeterminism(Dictionnary)==True:
                    Dictionnary=MiroirDico(Dictionnary)
                    AffichageAutomateFromDico(Dictionnary)
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


            Dictionnary=ProductAutomatons(Dictionnaire1,Dictionnaire2)
            AffichageAutomateFromDico(Dictionnary)
            wait()
        

        # concatenation
        case 17:
            print("\n-------------")
            print("Concatenation")
            print("-------------\n")
            wait()

        #######################ENVIRONNEMENT DEUX AUTOMATES +verif##############

            Dictionnary=ConcatenationAutomatons(Dictionnaire1,Dictionnaire2)
            AffichageAutomateFromDico(Dictionnary)
            wait()
        
        #############################(18)-(19)-(20)


        # Excising
        case 18:
            print("\n-------------")
            print("Excising mode")
            print("-------------\n")
            wait()
            Dictionnary=ChoixAutomate(Dictionnary1,Dictionnary2)
            if DicoVide(Dictionnary)==True:
                print("No Automaton in memory")
                wait()
            else:
                Dictionnary=ChangeToExcised(Dictionnary)
                AffichageAutomateFromDico(Dictionnary)
                wait()



        #cas default
        case _:
            print("Invalid choice\n")
            wait()









