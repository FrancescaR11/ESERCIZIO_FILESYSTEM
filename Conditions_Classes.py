#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Thu Jan 14 12:19:09 2021

@author: francescaronci,gaiad
"""


from os.path import splitext 
from abc import ABC, abstractmethod
import datetime,time
from Reader_Class import JPEGReader
from imageai.Detection import ObjectDetection


'''

Creo la classe 'PathChecker' che prende in ingresso il file che stiamo analizzando e il dizionario, 'condition_list'
contenente l'informazione del file json di input. 
Se il formato è presente nel file di input restituisce True altrimenti restituisce False


'''

class PathChecker():
    
    def __init__(self,filename,condition_list):
        
     self.filename=filename
     self.condition_list=condition_list
        
    def function(self) :
       
        suffix = splitext(self.filename)[1][1:].lower()  #Estraggo il formato del file
  
        #Se il formato del file è presente tra i formati del file di input restituisco True
        
        if suffix in self.condition_list['filetypelist']: 
               
               return True
        else:
                
               return False
            
                       
            
'''

Creo classe astratta sulle condizioni. 
Questa classe contiene il metodo astratto checker(), che viene implementato diversamente
in base alla condizione. Tale metodo restituisce sempre 'True' se la condizione è soddisfatta
e 'False' altrimenti.

'''

class Condition(ABC):
    """
    interface
    """
    def __init__(self):
     
     pass
            
    @abstractmethod
  
    def checker(self) :
        
        """
        abstract method
        """
        pass
        
    

'''

Creo la classe derivata 'OccurrenceChecker' che verifica, tramite il metodo 'checker()',
per ogni coppia parola-occorrenza, che la condizione sia verificata.

'''
 
class OccurrenceChecker(Condition):
    
    def __init__(self,parola,occorrenza):
       
     self.parola= parola
     self.occorrenza=occorrenza
    

        
    
    def checker(self,file_object):
     
     #Se il 'file_object' creato fa riferimento ad un formato immagine,
     #restituisce 'True' e salta la condizione relativa al file di testo.
     
     if   type(file_object)== JPEGReader:
         
         return True 
     
     else:
         
         #Il metodo 'get_file_content' restituisce la lista di stringhe presente nel file di testo
     
         lista_parole=file_object.get_file_content()
 
         ripetizioni=0  #Inizializzo il numero di ripetizioni della parola

         for stringa in lista_parole: #Confronto ogni stringa di 'lista_parole' con la parola cercata
             
           if stringa==self.parola: #Se è presente nel file..
                
              ripetizioni+=1 #..incremento
         
         if ripetizioni >= self.occorrenza: #Se la stringa è presente almeno tante volte quanto richiesto dalla condizione..
              
               return True 
         else :
              
               return False

            

'''
Creo la classe derivata 'SizeChecker' che verifica, tramite il metodo 'checker()',
che le condizioni sulla dimensione del file siano verificate.

'''


class SizeChecker(Condition):
    
    
    def __init__(self,condition_list,min_value,max_value):
        
        
        self.condition_list=condition_list
        self.min_value=min_value
        self.max_value=max_value
       
    
    def checker(self,file_object):
          
          # Se il valore minimo non è specificato assegno valore zero
        
          if self.min_value=='': 
              
              self.min_value=0
           
          # Se il valore massimo non è specificato oppure è infinito, assegno inf 
           
          if (self.max_value=='') | (self.max_value=='infinito'):
              
              self.max_value=float('inf')
              
                
          #Verifico la condizione sulla dimensione
          
          if  self.min_value < file_object.size_extractor() < self.max_value :
          
              return True
          
          else:
             
              return False

            
                       
'''
Creo la classe derivata 'TimeChecker' che verifica, tramite il metodo 'checker()',
che le condizioni sulla data di creazione del file siano verificate.

'''

class TimeChecker(Condition):
    
    def __init__(self,condition_list,min_value,max_value):
        
        
        self.condition_list=condition_list
        self.min_value=min_value
        self.max_value=max_value
        
        
    def checker(self,file_object):   
        
            
            #Se il minimo non è specificato lo sostituisco con 0
            
            if self.min_value== '':
                
                time_min=0
                
            #Se invece il minimo è specificato    
            
            else :
                
                #Estraggo la data di creazione del file e la converto il formato timestamp
                
                time_min=time.mktime(datetime.datetime.strptime(self.min_value, "%Y-%m-%d").timetuple())  
             
            # Se il massimo non è specificato lo sostituisco con inf   
                
            if self.max_value=='':
                
                time_max=float('inf')
                
            else :
                
                #Estraggo la data di creazione del file e la converto il formato timestamp
                
                time_max=time.mktime(datetime.datetime.strptime(self.max_value, "%Y-%m-%d").timetuple())
                
            #Verifico la condizione sulla data di creazione
           
            if  (time_min) < file_object.time_extractor() < (time_max):
            
                return True
            
            else:
                
                return False


'''
Creo la classe derivata 'ImageChecker' che verifica, tramite il metodo 'checker()',
per ogni coppia obj-occurrence, che la condizione sia verificata.

'''   

class ImageChecker(Condition):
   
    def __init__(self, condition_list, obj, occurrence, detector):
       
        
       self.condition_list=condition_list
       self.obj=obj
       self.occurrence=occurrence
       self.detector=detector
       
    
    
    def checker(self,file_object):
        
        #Se il 'file_object' creato fa riferimento ad un formato testuale,
        #restituisce 'True' e salta la condizione relativa al file immagine.
        
        if type(file_object)!= JPEGReader:
            
            return True
        
        else:
            
            #Il metodo 'get_file_content' restituisce la lista di oggetti presente nel file immagine
            
            found_objects=file_object.get_file_content(self.detector)
        
            ripetizioni=0  #Inizializzo il numero di ripetizioni dell'oggetto 

            for found_obj in found_objects: #Confronto ogni oggetto di 'found_objects' con l'oggetto cercato
             
              if found_obj==self.obj: #Se l'oggetto è presente..
                
               ripetizioni+=1  #..incremento
         
            if ripetizioni >= self.occurrence: #Se l'oggetto' è presente almeno tante volte quanto richiesto dalla condizione..
              
               return True
            else :
              
               return False
        
 

'''
Creo la classe 'InputInterpreter' che restituisce, partendo dal file di input,
'lista_classi', ovvero la lista contenente tutte le condizioni da verificare. 
In particolare tale lista contiene la chiamata alle classi che verificano le singole condizioni.
Per ogni specifica condizione viene quindi creato un oggetto diverso.

'''


class InputInterpreter():
    
    def __init__(self): 
        
        pass
        
    def extractor(image_objects,condition_list): 
        
        #inizializzo la lista delle classi da chiamare per verificare le condizioni
        
        lista_classi=[] 
       
        #Estraggo la lista delle differenti tipologie di condizione
        
        lista_condizioni= list(condition_list.keys())

        if 'size'  in lista_condizioni:
            
            '''
            Appendo a 'lista_classi' le diverse chiamate alla classe
            che gestisce la condizione sulla 'size' (dimensione del file). 
            Creo in questo modo due oggetti diversi, uno per soddisfare la
            dimensione minima e uno per la dimensione massima.
            '''
            min_value=condition_list['size']['min']
            max_value=condition_list['size']['max']
            lista_classi.append(SizeChecker(condition_list,min_value,max_value))
        
        if 'time'  in lista_condizioni:
            
            #Appendo a 'lista_classi' le diverse chiamate alla classe
            #che gestisce la condizione sul 'time' (data di creazione del file).
            
            min_value=condition_list['time']['min']
            max_value=condition_list['time']['max']
            lista_classi.append(TimeChecker(condition_list,min_value,max_value))  
        
        if 'wordlist' in lista_condizioni:
            
            '''
            Appendo a 'lista_classi' le diverse chiamate alla classe
            che gestisce la condizione sulla 'wordlist' (lista delle parole cercate).
            Creo tanti oggetti della classe 'OccurrenceChecker' quante sono le coppie parola-occorrenza cercate.
            '''
            for parola in condition_list['wordlist'].keys():
               lista_classi.append(OccurrenceChecker(parola,condition_list['wordlist'][parola]))
        
        if 'objectlist' in lista_condizioni:
            
            # Creo l'oggetto detector
            
            detector = ObjectDetection() 
            
            model_path = "./models/yolo-tiny.h5"
            detector.setModelTypeAsTinyYOLOv3()
            detector.setModelPath(model_path)
            detector.loadModel()
           
            #Appendo a 'lista_classi' le diverse chiamate alla classe
            #che gestisce la condizione sulla 'objectlist' (lista degli oggetti cercati). 
            
            for obj in condition_list['objectlist'].keys():
                
                #controllo se l'oggetto è tra quelli riconoscibili dall'algoritmo
                    
                if obj in image_objects:
            
                    lista_classi.append(ImageChecker(condition_list,obj,condition_list['objectlist'][obj],detector))
                    
                else:
                    
                    print('Oggetto cercato non presente tra quelli riconoscibili dall algoritmo' )
                   
                 
        return lista_classi  #Restituisco la lista contenente la chiamata alle classi per ogni specifica condizione







































                    