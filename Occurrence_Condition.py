# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 19:26:18 2021

@author: gaiad,francescaronci
"""
'''
Creo la funzione Occurrence_Condition, che prende come parametri di ingresso i seguenti parametri:
    
    -"dati": file di input ( dict);
   
    -"lista_stringhe": lista delle stringhe contenute nel file che sto analizzando;
   
    -"lista_output": lista inizializzata nel main, che conterrà i file che soddisfano 
    
    sia la condizione sul formato che quella sulle occorrenze delle parole.

Questa funzione aggiunge a "lista_output"  il path del file che sto analizzando se la condizione

sulle occorrenze delle parole è soddisfatta.
    
'''

def Occurrence_Condition(dati,lista_stringhe,file,lista_output):
    
    # Inizializzo la lista che conterrà il numero di volte che si ripetono le parole presenti 
    #sia nel file di input che nel file analizzato
   
    rip=[]  
    
    #Scandisco le parole del file di input 
   
    for occorrenza in dati['wordlist'].keys(): 
         
         ripetizioni=0 # Inizializzo con il valore zero il numero di volte che è presente "parola"
      
         for parola in lista_stringhe: # Scandisco le parole presenti nella lista delle stringhe contenute nel file che sto analizzando
       
             if parola==occorrenza: # Se la parola del file analizzato è uguale alla parola del file di input...
                
              ripetizioni+=1 # ...incremento il contatore "ripetizioni"
         
         rip.append(ripetizioni) # Aggiungo il numero di volte che è presente "parola" alla lista "rip"
    
    # Se la lista "rip" è uguale alla lista dei valori che corrispondono alle occorrenze desiderate...  
    
    if rip==list(dati['wordlist'].values()): 
           
     lista_output.append(file)# ...aggiungo il path del file a "lista_output"
           
    return lista_output # Restituisco lista_output 
