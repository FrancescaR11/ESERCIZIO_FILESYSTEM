#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 12:19:09 2021

@author: francescaronci,gaiad
"""

import os 
import argparse 
import json  
from os.path import splitext 
import re  
import openpyxl 
import csv  
import pdfplumber 
from abc import ABC, abstractmethod
import datetime,time
from imageai.Detection import ObjectDetection


'''

Uso argparse per la lettura del file di input e la scrittura del file di output.

'''

parser=argparse.ArgumentParser()

parser.add_argument("-i", "--input_data", help="Complete path to the file containing input data",
                    type=str, default='./dati/input.json')

parser.add_argument("-o", "--out_data", help="Complete path to the file containing output data", 
                    type=str, default='./results/output.txt')

parser.add_argument("-i_2", "--input_data_2", help="Complete path to the file containing output data", 
                    type=str, default='./dati/objects.txt')

parser.add_argument("-o_2", "--out_data_2", help="Complete path to the file containing output of the images detector", 
                    type=str, default='./results/')

args=parser.parse_args()


'''

Creo la classe che prende in ingresso il file che stiamo analizzando. 
Se il formato è presente nel file di input, chiamo la classe che verifica la 
seconda condizione.


'''

class PathChecker():
    
    def __init__(self,filename,condition_list):
        
     self.filename=filename
     self.condition_list=condition_list
        
    def function(self) :
       
        suffix = splitext(self.filename)[1][1:].lower()
        

            
        if suffix in self.condition_list['filetypelist']: # Se il formato del file è presente tra i formati del file di input...
               
               return True
        else:
                
                return 'failure'
            
            
            
            
'''

Creo classe astratta sulle condizioni. Questa classe rimanda alla classe PathChecker,
indipendentemente dal formato.
Questa classe contiene il metodo astratto checker(), che viene implementato diversamente
in base alla condizione.

'''

class Condition(ABC):
    """
    interface
    """
    def __init__(self):#,condition_list):
      
      #  self.condition_list=condition_list
     pass

    @staticmethod
    
    def create_instance(condition_list,filename):  

        return PathChecker(filename,condition_list).function()
            
    @abstractmethod
  
    def checker(self) :
        
    #     """
    #     abstract method
    #     """
         pass
        
    

'''

Creo la classe derivata che chiama la funzione importata Occurence_Condition e resituisce in output
la lista dei path dei file che soddisfano sia la condizione sul formato che quella sulle occorrenze delle parole.

'''
 
class OccurrenceChecker(Condition):
    
    def __init__(self,parola,occorrenza):
       
     self.parola= parola
     self.occorrenza=occorrenza
     #super().__init__(condition_list)
    

        
    
    def checker(self,file_object):
     
     if   type(file_object)== JPEGReader:
         
         return True 
     
     else:
     
         lista_parole=file_object.get_file_content()
 
         ripetizioni=0  

         for stringa in lista_parole: 
             
           if stringa==self.parola: 
                
              ripetizioni+=1 
         
         if ripetizioni== self.occorrenza:
              
               return True
         else :
              
               return False

       
      

'''
'''




class SizeChecker(Condition):
    
    
    def __init__(self,condition_list,value):
        
        
        self.condition_list=condition_list
        #super().__init__(condition_list)
        self.value=value
       
    
    def checker(self,file_object):
        
        if (self.condition_list['size']['min'])==self.value :
        
        
          if  self.value < file_object.size_extractor() :
          
              return True
          
          else:
             
                return False
            
        elif (self.condition_list['size']['max'])==self.value :  
             
           if   file_object.size_extractor() < self.value:
          
              return True
          
           else:
             
                return False
            
            
            
'''
'''

class TimeChecker(Condition):
    
    def __init__(self,condition_list,value):
        
        
        #super().__init__(condition_list)
        self.condition_list=condition_list
        self.value=value
        
        
    def checker(self,file_object):   
        
        
        if condition_list['time']['min']==self.value :
            
            if self.value== '':
                
                time_min=0
                
            else :
             
                time_min=time.mktime(datetime.datetime.strptime(self.value, "%Y-%m-%d").timetuple())   
            
            if  (time_min) < file_object.time_extractor():
            
                return True
            
            else:
                
                return False
                
                
        if  condition_list['time']['max']==self.value :
            
            time_max=time.mktime(datetime.datetime.strptime(self.value, "%Y-%m-%d").timetuple())
                
            
            if   file_object.time_extractor() < (time_max):
                
                return True
           
            else:
              
                return False
  


'''
Creo la classe derivata che verifica la seconda condizione sulle immagini.

'''   

class ImageChecker(Condition):
   
    def __init__(self, condition_list, obj, occurrence):
       
        
       self.condition_list=condition_list
       #super().__init__(condition_list) 
       self.obj=obj
       self.occurrence=occurrence
       
    
    
    def checker(self,file_object):
        
        if type(file_object)!= JPEGReader:
            
            return True
        
        else:
         
            found_objects=file_object.get_file_content()
        
            ripetizioni=0  

            for found_obj in found_objects: 
             
              if found_obj==self.obj: 
                
               ripetizioni+=1 
         
            if ripetizioni== self.occurrence:
              
               return True
            else :
              
               return False
        
                     
            
    


'''

Creo classe astratta che legge il formato. Questa classe prende in ingresso il file che sto analizzando e restituisce,
attraverso la chiamata alle classi derivate specifiche per ogni formato, il contenuto del file.
Nel caso di file di testo, restituisce la lista delle parole.

'''


class FormatReader(ABC):
    """
    interface
    """
   
    def __init__(self,filename):  #,size,creation_date):
        
      self.filename=filename
    #     #self.size=size
    #     #self.creation_date=creation_date
    #     pass

    @abstractmethod
    def get_file_content(self):
        """
        abstract method
        """
        pass

    @staticmethod
    def create_instance(filename):
        
        suffix = splitext(filename)[1][1:].lower()
 
        
        if suffix == 'txt':
        
                return TXTReader(filename)
        
        elif suffix == 'csv':
            
                 return CSVReader(filename)
        
        elif suffix == 'xlsx':
            
                 return XLSXReader(filename)
        
        elif suffix == 'pdf':
            
                return PDFReader(filename)
            
            
        elif suffix=='jpeg':
            
                return JPEGReader(filename)    
        
        else:
            
             raise ValueError('unknown file type')


"""
"""
class JPEGReader(FormatReader):

    def __init__(self, filename):
        
       super().__init__(filename)
       
       
        
    def size_extractor(self):
        
      file_size=os.path.getsize (self.filename)
      
      return file_size
  
    def time_extractor(self):
        
        file_time=os.path.getctime(self.filename)
        
        return file_time    

    
    def get_file_content(self):
        
        found_objects=[]
        detector = ObjectDetection()

        model_path = "./models/yolo-tiny.h5"
        #output_path = args.out_dir
        
        detector.setModelTypeAsTinyYOLOv3()
        detector.setModelPath(model_path)
        detector.loadModel()
        
 
        
        detection = detector.detectObjectsFromImage(input_image=file, output_image_path=args.out_data_2+os.path.basename(file),minimum_percentage_probability=30)
        
        for eachItem in detection:
            
            found_objects.append(eachItem["name"]) 
            
        return found_objects     
    



'''

Creo classe derivata per la lettura dei file txt. Questa classe prende in ingresso il file txt che sto analizzando e
restituisce la lista delle parole contenute nel file.

'''            

class TXTReader(FormatReader):

    def __init__(self, filename):
        
       super().__init__(filename)
     
    
    def size_extractor(self):
        
      file_size=os.path.getsize (self.filename)
      
      return file_size
  
    def time_extractor(self):
        
        file_time=os.path.getctime(self.filename)
        
        return file_time
    
   
    def get_file_content(self):
        
        f= open(self.filename) 
        
        file_txt=(f.read()) # Salvo il testo contenuto nel file in una stringa
          
        lista_stringhe_txt=re.findall(r"[\w']+", file_txt.lower()) # Elimino la punteggiatura e divido la stringa (in minuscolo) ad ogni spazio
        
        return lista_stringhe_txt # Restituisco la lista delle parole contenute nel file
    

'''

Creo classe derivata per la lettura dei file csv. Questa classe prende in ingresso il file csv che sto analizzando e
restituisce la lista delle parole contenute nel file.

'''     

class CSVReader(FormatReader):

    def __init__(self, filename):
        
        super().__init__(filename)

     
    def size_extractor(self):
        
      file_size=os.path.getsize (self.filename)
    
      return file_size
  
    def time_extractor(self):
        
        file_time=os.path.getctime(self.filename)
        
        return file_time
  
    def get_file_content(self):
        
        with open(self.filename) as filecsv:
            
            testo=' ' # Inizializzo una stringa vuota
            
            lettore = csv.reader(filecsv,delimiter=";") # Leggo il file csv
            
            for row in lettore: # Scandisco le righe dell'oggetto reader
                
                delimitat= " "
                
                # Aggiungo alla stringa 'testo' le righe del file csv (in minuscolo) separate dagli spazi
                
                testo=testo+(delimitat.join(row)).lower()+' ' 
           
            # Elimino la punteggiatura e divido le stringhe ad ogni spazio
            
            lista_stringhe_csv=re.findall(r"[\w']+", testo) 
        
        return lista_stringhe_csv # Restituisco la lista delle parole contenute nel file

'''

Creo classe derivata per la lettura dei file xlsx. Questa classe prende in ingresso il file xlsx che sto analizzando e
restituisce la lista delle parole contenute nel file.

'''         
    
class XLSXReader(FormatReader):

    def __init__(self, filename):
        
        super().__init__(filename)

    def size_extractor(self):
        
      file_size=os.path.getsize (self.filename)  
    
      return file_size
  
    def time_extractor(self):
        
        file_time=os.path.getctime(self.filename)
        
        return file_time
    
    def get_file_content(self):
        
         stringhe=' ' # Inizializzo una stringa vuota
         
         excel_document = openpyxl.load_workbook(self.filename) # Apro file excel
        
         nomi_fogli=(excel_document.sheetnames) # Salvo il nome dei fogli in una lista
   
         for nome in nomi_fogli: # Scandisco tutti i fogli del file excel
          
          sheet = excel_document[nome]

          for row in sheet.iter_rows(): # Scandisco le righe dei fogli excel
    
            for cell in row: # Scandisco le celle per riga
     
              if (cell.value is None)==False: # Se il valore della cella non è None...
       
                  stringhe=stringhe+((cell.value).lower())+' ' # ... aggiungo il contenuto della cella (in minuscolo) alla stringa                   
                 
                  lista_stringhe_xlsx=re.findall(r"[\w']+", stringhe)  # Elimino la punteggiatura e divido le stringhe ad ogni spazio
        
         return lista_stringhe_xlsx # Restituisco la lista delle parole contenute nel file

'''

Creo classe derivata per la lettura dei file pdf. Questa classe prende in ingresso il file pdf che sto analizzando e
restituisce la lista delle parole contenute nel file.

'''     
    

class PDFReader(FormatReader):

    def __init__(self, filename):
        
        super().__init__(filename)

   
    def size_extractor(self):
        
      file_size=os.path.getsize (self.filename) 
      
      return file_size
  
    def time_extractor(self):
        
        file_time=os.path.getctime(self.filename)
        
        return file_time
   
    def get_file_content(self):
        
        with pdfplumber.open (self.filename) as pdf: # Apro il file pdf
           
           pages = pdf.pages  # Salvo le pagine del file pdf in una lista
           
           stringhe_pdf=' ' # Inizializzo una stringa vuota
           
           for page in pages: # Scandisco ogni pagina contenuta nella lista di pagine
                 
                 # Aggiungo il contenuto della pagina (in minuscolo) alla stringa
                 
                 stringhe_pdf=stringhe_pdf+ (page.extract_text ()).lower() + ' '  
           
           lista_stringhe_pdf=re.findall(r"[\w']+", stringhe_pdf)  # Elimino la punteggiatura e divido le stringhe ad ogni spazio
           
           
        return lista_stringhe_pdf # Restituisco la lista delle parole contenute nel file




class InputInterpreter():
    
    def __init__(self,condition_list):
        
        self.condition_list=condition_list
       # self.image_objects=image_objects
        
    def extractor(self,image_objects):
        
        lista_classi=[]
        lista_condizioni= list(self.condition_list.keys())

        if 'size'  in lista_condizioni:
            
            minima=self.condition_list['size']['min']
            massima=self.condition_list['size']['max']
            lista_classi.append(SizeChecker(self.condition_list,minima))
            lista_classi.append(SizeChecker(self.condition_list,massima))
        
        if 'time'  in lista_condizioni:
            
            minima=self.condition_list['time']['min']
            massima=self.condition_list['time']['max']
            lista_classi.append(TimeChecker(self.condition_list,minima))  
            lista_classi.append(TimeChecker(self.condition_list,massima))
        
        if 'wordlist' in lista_condizioni:
            
            for parola in self.condition_list['wordlist'].keys():
               lista_classi.append(OccurrenceChecker(parola,self.condition_list['wordlist'][parola]))
        
        if 'objectlist' in lista_condizioni:
            
            for obj in self.condition_list['objectlist'].keys():
                
                if obj in image_objects:
                    
                    lista_classi.append(ImageChecker(condition_list,obj,self.condition_list['objectlist'][obj]))
                    
                 
        return lista_classi







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
    

    
    
lista_classi=InputInterpreter(condition_list).extractor(image_objects)   

# Inizializzo la lista che conterrà i file che soddisfano sia la condizione sul formato che quella sulle occorrenze delle parole

searched_file=[]

for file in lista_path: # Scandisco tutti i file trovati nei path passati con il file di input
     
 
    condition=Condition.create_instance(condition_list,file)
       

     
    if condition !='failure':
        
        file_object=FormatReader.create_instance(file)
        
    
        for condizione in lista_classi:
            
            is_verified_condition= condizione.checker(file_object)
              
            if  is_verified_condition== False:
                 
                break 
            
        
        if  is_verified_condition== True:       
              
              searched_file.append(file)
              
            
# Salvo su un file in formato txt la lista dei file che rispettano le condizioni

with open(args.out_data, "w") as output:
    
    output.write(str(searched_file))              
    
    
    
    
    
    
    
    