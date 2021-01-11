# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 19:26:18 2021

@author: gaiad,francescaronci
"""
'''
Creo la funzione Occurrence_Condition, che prende come parametri di ingresso i seguenti parametri:
    
    -"dati": file di input ( dict);
   
    -"lista": lista delle stringhe contenute nel file che sto analizzando;
   

Questa funzione restituisce True se il file che sto analizzando verifica la condizione

sulle occorrenze delle parole e False altrimenti.
    
'''

def Occurrence_Condition(dati,lista):
    
    # Inizializzo la lista che conterrà il numero di volte che si ripetono le parole presenti 
    #sia nel file di input che nel file analizzato
   
    rip=[]  
    
    #Scandisco le parole del file di input 
   
    for occorrenza in dati['wordlist'].keys(): 
         
         ripetizioni=0 # Inizializzo con il valore zero il numero di volte che è presente "parola"
      
         for parola in lista: # Scandisco le parole presenti nella lista delle stringhe contenute nel file che sto analizzando
       
             if parola==occorrenza: # Se la parola del file analizzato è uguale alla parola del file di input...
                
              ripetizioni+=1 # ...incremento il contatore "ripetizioni"
         
         rip.append(ripetizioni) # Aggiungo il numero di volte che è presente "parola" alla lista "rip"
    
    # Se la lista "rip" è uguale alla lista dei valori che corrispondono alle occorrenze desiderate...  
    
    if rip==list(dati['wordlist'].values()): 
           
     
           
     return True
   
    else:
       
       return False 
