#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 11:35:17 2021

@author: francescaronci, gaiad
"""

import os
#import pandas as pd
import argparse
# dirs contiene le sottocartelle 
# name contiene nome del file
import json
from os.path import splitext
from Eliminazione_Nan import replace_Nan_with_zeros
import re
import openpyxl
import csv

parser=argparse.ArgumentParser()

parser.add_argument("-i", "--input_data", help="Complete path to the file containing yellow_tripdata",
                    type=str, default='./dati/input.json')

args=parser.parse_args()


with open(args.input_data) as json_file:
   dati=json.load(json_file)

chiavi=list(dati.keys())
lista_path=[]


for path in dati[chiavi[0]]:
 for root,dirs, files in os.walk(path, topdown=False):
   for name in files:
       if name!= ".DS_Store":
        lista_path.append(os.path.join(root, name))

# Condizione di lettura del file

lista_cond_uno=[]
lista_output=[]

for file in lista_path:
    aggiunto=False
    suffix = splitext(file)[1][1:].lower()
    
    for formato in dati[chiavi[1]]:
     # mando alla classe che legge quel suffix 
     
     if suffix==formato: # questa condizione va inserita nella classe relativa a suffix
         
      lista_cond_uno.append(file) # se questa condizione è verificata vado alla classe che verifica seconda condizione    
         
      if suffix=="txt": #entro nella classe txt
          
        f= open(file) 
        
        file_txt=(f.read())
          
        lista_stringhe=re.findall(r"[\w']+", file_txt.lower()) #Elimino la punteggiatura per eseguire il comando split()
        rip=[]  
        
        for occorrenza in dati[chiavi[2]].keys():
            ripetizioni=0
            for parola in lista_stringhe:
                if parola==occorrenza:
                   ripetizioni+=1
            rip.append(ripetizioni)
        if rip==list(dati[chiavi[2]].values()):
            lista_output.append(file)

          
      if suffix=="csv": # entro nella classe csv
          
          with open(file) as filecsv:
             testo=' '
             lettore = csv.reader(filecsv,delimiter=";")
             for row in lettore:
               delimitat= " "
               testo=testo+(delimitat.join(row)).lower()+' '
             lista_stringhe=re.findall(r"[\w']+", testo)
             rip=[]  
        
             for occorrenza in dati[chiavi[2]].keys():
                  ripetizioni=0
           
                  for parola in lista_stringhe:
                
                      if parola==occorrenza:
                         ripetizioni+=1
                  rip.append(ripetizioni)
       
             if rip==list(dati[chiavi[2]].values()):
                    lista_output.append(file)
              
      if suffix=="xlsx": # entro nella classe xlsx
          
         stringhe=' '
         excel_document = openpyxl.load_workbook(file)
         nomi_fogli=(excel_document.get_sheet_names())
   
         for nome in nomi_fogli:
          sheet = excel_document.get_sheet_by_name(nome)

          for row in sheet.iter_rows():
    
            for cell in row:
     
              if (cell.value is None)==False:
       
                  stringhe=stringhe+((cell.value).lower())+' '                        
                  lista_stringhe=re.findall(r"[\w']+", stringhe)                                 
                  rip=[]  
        
                  for occorrenza in dati[chiavi[2]].keys():
                   ripetizioni=0
           
                   for parola in lista_stringhe:
                
                      if parola==occorrenza:
                       ripetizioni+=1
                   rip.append(ripetizioni)
       
                  if rip==list(dati[chiavi[2]].values()):
                    lista_output.append(file)
          

        
    
 
    
 
    
 
    
 
    
 
    
 
    
 
                                  

 
