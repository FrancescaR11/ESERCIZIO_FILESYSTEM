#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:23:23 2021

@author: francescaronci
"""


import os 
import argparse 
import json  
from imageai.Detection import ObjectDetection
from Condition_Class import PathChecker
from Condition_Class import SizeChecker,OccurrenceChecker,ImageChecker,TimeChecker
from Reader_Class import FormatReader 

'''

Uso argparse per la lettura dei file di input e la scrittura del file di output.
Il programma riceve in ingresso:
    
- 'input.json' --> il file json contentente la porzione del filesystem su cui effettuare la ricerca e
  una lista delle condizioni che devono essere verificate.
  
- 'objects.txt' --> una file di testo contenente la lista degli oggetti individuabili dall'algoritmo

Il programma restituisce in output un file txt contenente la lista di file che soddisfano le condizioni richieste.

'''

parser=argparse.ArgumentParser()

parser.add_argument("-i", "--input_data", help="Complete path to the file containing input data",
                    type=str, default='./dati/input.json')

parser.add_argument("-o", "--out_data", help="Complete path to the file containing output data", 
                    type=str, default='./results/output.txt')

parser.add_argument("-i_2", "--input_data_2", help="Complete path to the file containing output data", 
                    type=str, default='./dati/objects.txt')


args=parser.parse_args()



'''
Creo la classe 'InputInterpreter' che restituisce, partendo dal file di input,
'lista_classi', ovvero la lista contenente tutte le condizioni da verificare. 
In particolare tale lista contiene la chiamata alle classi che verificano le singole condizioni.
Per ogni specifica condizione viene quindi creato un oggetto diverso.

'''


class InputInterpreter():
    
    def __init__(self,condition_list):
        
        self.condition_list=condition_list
       # self.image_objects=image_objects
        
    def extractor(self,image_objects):
        
        #inizializzo la lista delle classi da chiamare per verificare le condizioni
        lista_classi=[] 
        #Estraggo la lista delle differenti tipologie di condizione
        lista_condizioni= list(self.condition_list.keys())

        if 'size'  in lista_condizioni:
            
            '''
            Appendo a 'lista_classi' le diverse chiamate alla classe
            che gestisce la condizione sulla 'size' (dimensione del file). 
            Creo in questo modo due oggetti diversi, uno per soddisfare la
            dimensione minima e uno per la dimensione massima.
            '''
            min_value=self.condition_list['size']['min']
            max_value=self.condition_list['size']['max']
            lista_classi.append(SizeChecker(self.condition_list,min_value,max_value))
        
        if 'time'  in lista_condizioni:
            
            #Appendo a 'lista_classi' le diverse chiamate alla classe
            #che gestisce la condizione sul 'time' (data di creazione del file).
            
            min_value=self.condition_list['time']['min']
            max_value=self.condition_list['time']['max']
            lista_classi.append(TimeChecker(self.condition_list,min_value,max_value))  
        
        if 'wordlist' in lista_condizioni:
            
            '''
            Appendo a 'lista_classi' le diverse chiamate alla classe
            che gestisce la condizione sulla 'wordlist' (lista delle parole cercate).
            Creo tanti oggetti della classe 'OccurrenceChecker' quante sono le coppie parola-occorrenza cercate.
            '''
            for parola in self.condition_list['wordlist'].keys():
               lista_classi.append(OccurrenceChecker(parola,self.condition_list['wordlist'][parola]))
        
        if 'objectlist' in lista_condizioni:
            
            detector = ObjectDetection()
            
            model_path = "./models/yolo-tiny.h5"
            detector.setModelTypeAsTinyYOLOv3()
            detector.setModelPath(model_path)
            detector.loadModel()
            #Appendo a 'lista_classi' le diverse chiamate alla classe
            #che gestisce la condizione sulla 'objectlist' (lista degli oggetti cercati). 
            
            for obj in self.condition_list['objectlist'].keys():
                
                #controllo se l'oggetto è tra quelli riconoscibili dall'algoritmo
                    
                if obj in image_objects:
            
                    lista_classi.append(ImageChecker(self.condition_list,obj,self.condition_list['objectlist'][obj],detector))
                    
                 
        return lista_classi  #Restituisco la lista contenente la chiamata alle classi per ogni specifica condizione



################################ MAIN ########################################

# Apertura file input

            
with open(args.input_data) as json_file:
   
    condition_list=json.load(json_file)

image_objects = open(args.input_data_2, "r").read()    
    


lista_path=[] # Inizializzo lista che conterrà i path dei file trovati

for path in condition_list['dirlist']: # Scandisco tutti i path contenuti nel file input
 
  for root,dirs, files in os.walk(path, topdown=False): #Scandisco sottocartelle (dirs) e files
   
    for name in files: # Scandisco i file presenti nelle sottocartelle
       
       if name!= ".DS_Store":
        
             lista_path.append(os.path.join(root, name)) # Aggiungo il path del file 'name' alla lista dei path dei file trovati    
    

#Chiamando la classe 'InputInterpreter' estraggo la lista
#contenente le chiamate alle classi per ogni specifica condizione.  
    
lista_classi=InputInterpreter(condition_list).extractor(image_objects)   

# Inizializzo la lista che conterrà i file che soddisfano tutte le condizioni

searched_file=[]

# Scandisco i path dei file relativi alla porzione di filesystem su cui verificare le condizioni
for file in lista_path:     
    
    '''
    Il metodo 'create_instance' della classe 'Condition' rimanda, indistintamente 
    dal formato del file, alla classe 'PathChecker' che verifica che il formato sia 
    tra quelli cercati. In tal caso restituisce 'True', altrimenti 'failure'.
    Se il valore restituito è 'failure' passa direttamente ad analizzare il file successivo.
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

with open(args.out_data, "w") as output:
    
    output.write(str(searched_file))  