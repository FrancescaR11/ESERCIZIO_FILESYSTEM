#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:23:23 2021

@author: francescaronci
"""


import os 
import argparse 
import json  
from Conditions_Classes import PathChecker
from Reader_Class import FormatReader 
from Conditions_Classes import InputInterpreter
import time

'''

Uso argparse per la lettura dei file di input e la scrittura del file di output.
Il programma riceve in ingresso:
    
- 'input.json' --> il file json contentente la porzione del filesystem su cui effettuare la ricerca e
  una lista delle condizioni che devono essere verificate.
  
- 'objects.txt' --> una file di testo contenente la lista degli oggetti individuabili dall'algoritmo

Il programma restituisce in output un file txt contenente la lista di file che soddisfano le condizioni richieste.

'''

parser=argparse.ArgumentParser()

parser.add_argument("-i", "--condition_list", help="Complete path to the input file containing conditions list",
                    type=str, default='./dati/input.json')

parser.add_argument("-o", "--searched_files", help="Complete path to the output file containing searched files", 
                    type=str, default='./results/output.txt')

parser.add_argument("--recognized_objects", help="Complete path to the input file containing recognized objects", 
                    type=str, default='./dati/objects.txt') 

args=parser.parse_args()



################################ MAIN ########################################

start = time.perf_counter() #  Avvio conteggio del tempo di esecuzione


# Apertura del file json contentente la porzione del filesystem su cui effettuare la ricerca
# e una lista delle condizioni che devono essere verificate.

            
with open(args.condition_list) as json_file:
   
    condition_list=json.load(json_file)

# Apertura del file txt contenente la lista degli oggetti individuabili dall'algoritmo

image_objects = open(args.recognized_objects, "r").read()    
    


lista_path=[] # Inizializzo lista che conterrà i path dei file trovati

for path in condition_list['dirlist']: # Scandisco tutti i path contenuti nel file input
 
  for root,dirs, files in os.walk(path, topdown=False): #Scandisco sottocartelle (dirs) e files
   
    for name in files: # Scandisco i file presenti nelle sottocartelle
       
       if name!= ".DS_Store":
             
             # Aggiungo il path del file 'name' alla lista dei path dei file trovati
             
             lista_path.append(os.path.join(root, name))     
    

#Chiamando la classe 'InputInterpreter' estraggo la lista
#contenente le chiamate alle classi per ogni specifica condizione.  
    
lista_classi=InputInterpreter.extractor(image_objects,condition_list)   

# Inizializzo la lista che conterrà i file che soddisfano tutte le condizioni

searched_file=[]

# Scandisco i path dei file relativi alla porzione di filesystem su cui verificare le condizioni

for file in lista_path:     
    
    '''
    Chiamo la classe 'PathChecker' che verifica che il formato sia 
    tra quelli cercati. In tal caso restituisce 'True', altrimenti 'False'.
    Se il valore restituito è 'False' passa direttamente ad analizzare il file successivo.
   
    '''
    
    condition=PathChecker(file,condition_list).function()  

    if condition !=False:
        
        '''
        Il metodo 'create_instance' della classe 'FormatReader' rimanda, in base all'estensione
        del file, alla classe derivata in grado di estrarne il contenuto, la size e la data di creazione.
        '''
        file_object=FormatReader.create_instance(file)
        
        '''
        Eseguo il ciclo su tutte le condizioni, chiamando il metodo 'checker' della classe
        'Condition', implementato diversamente per ogni tipologia di condizione. Il metodo checker 
        restituisce 'True' se la condizione è verificata e 'False' in caso contrario.
        '''
        
        for condizione in lista_classi:
            
            is_verified_condition= condizione.checker(file_object)
              
            #Se la condizione non è verificata esco dal ciclo passando al file successivo
            if  is_verified_condition== False:  
                 
                break 
            
        #Se verifica tutte le condizioni lo appendo nel file di output 'searched_file'
        if  is_verified_condition== True:       
              
              searched_file.append(file)
              
            
# Salvo su un file in formato txt la lista dei file che rispettano le condizioni

with open(args.searched_files, "w") as output:
    
    output.write(str(searched_file))  
    
elapsed= time.perf_counter() - start # Calcolo il tempo impiegato per l'esecuzione

print ('Il tempo di esecuzione è' + ' ' +str(elapsed)) # Stampo il tempo impiegato per l'esecuzione    
    
    
    