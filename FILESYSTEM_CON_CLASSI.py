# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:14:47 2021

@author: gaiad, francescaronci
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
from Occurrence_Condition import Occurrence_Condition

parser=argparse.ArgumentParser()

parser.add_argument("-i", "--input_data", help="Complete path to the file containing input data",
                    type=str, default='./dati/input.json')

#parser.add_argument("-o", "--out_data", help="Complete path to the file containing output data", 
#                    type=str, default='./results/output.txt')

args=parser.parse_args()


'''
CREO CLASSE ASTRATTA SULLE CONDIZIONI

'''

class Conditions(ABC):
    """
    interface
    """
    @classmethod
    #@abstractmethod
    def path_condition(self):
        """
        abstract method
        """
        pass
    @classmethod
    #@abstractmethod
    def occurrence_condition(self):
        """
        abstract method
        """
        pass

    @staticmethod
    def create_instance(filename):  #se ho file di testo indirizzo alle classi di controllo sul path e le occorrenze senno alle future classi si controllo sul path e sul contenuto delle immagini
        suffix = splitext(filename)[1][1:].lower()
        if (suffix == 'txt') | (suffix == 'csv') | (suffix == 'xlsx') | (suffix == 'pdf'):
            return PathFinder(filename), suffix , OccurrenceFinder(filename) 
        else:
            raise ValueError('unknown file type')
            

class PathFinder(Conditions):

    def __init__(self, filename):
        
        self.filename = filename

    def path_condition(self,suffix):         
        
        for formato in dati[chiavi[1]]:
            
            if suffix==formato: 
                  
             lista_cond_uno.append(file) # se questa condizione è verificata vado alla classe sulla seconda condizione 
             
             lista_output=reader[2].occurrence_condition()
             
        return lista_cond_uno , lista_output

 
class OccurrenceFinder(Conditions):

    def __init__(self, filename):
        
        self.filename = filename

    def occurrence_condition(self):     
        
        lista_output1=Occurrence_Condition(dati,lista_stringhe,chiavi,file,lista_output)
        
        return lista_output1

'''
CREO CLASSE ASTRATTA CHE LEGGE IL FORMATO

'''


class FormatReader(ABC):
    """
    interface
    """

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
        else:
            raise ValueError('unknown file type')
            

class TXTReader(FormatReader):

    def __init__(self, filename):
        
        self.filename = filename

    def get_file_content(self):
        
        f= open(file) 
        
        file_txt=(f.read())
          
        lista_stringhe_txt=re.findall(r"[\w']+", file_txt.lower()) #Elimino la punteggiatura e divido le stringhe ad ogni spazio
        
        return lista_stringhe_txt
    
    
class CSVReader(FormatReader):

    def __init__(self, filename):
        
        self.filename = filename

    def get_file_content(self):
        
        with open(file) as filecsv:
            testo=' '
            lettore = csv.reader(filecsv,delimiter=";")
            for row in lettore:
                delimitat= " "
                testo=testo+(delimitat.join(row)).lower()+' '
            lista_stringhe_csv=re.findall(r"[\w']+", testo)
        
        return lista_stringhe_csv
        
    
class XLSXReader(FormatReader):

    def __init__(self, filename):
        self.filename = filename

    def get_file_content(self):
        
         stringhe=' '
         excel_document = openpyxl.load_workbook(file)
         nomi_fogli=(excel_document.get_sheet_names())
   
         for nome in nomi_fogli:
          sheet = excel_document.get_sheet_by_name(nome)

          for row in sheet.iter_rows():
    
            for cell in row:
     
              if (cell.value is None)==False:
       
                  stringhe=stringhe+((cell.value).lower())+' '                        
                  lista_stringhe_xlsx=re.findall(r"[\w']+", stringhe) 
        
         return lista_stringhe_xlsx
    
    
class PDFReader(FormatReader):

    def __init__(self, filename):
        self.filename = filename

    def get_file_content(self):
        
        with pdfplumber.open (file) as pdf: 
           pages = pdf.pages 
           stringhe_pdf=' '
           for page in pages: 
              stringhe_pdf=stringhe_pdf+ page.extract_text () + ' '
           lista_stringhe_pdf=re.findall(r"[\w']+", stringhe_pdf)  
           
           
        return lista_stringhe_pdf
    
    
        
#Apertura file input
            
with open(args.input_data) as json_file:
   dati=json.load(json_file)

chiavi=list(dati.keys())
lista_path=[]

# dirs contiene le sottocartelle 
# name contiene nome del file

for path in dati[chiavi[0]]:
 for root,dirs, files in os.walk(path, topdown=False):
   for name in files:
       if name!= ".DS_Store":
        lista_path.append(os.path.join(root, name)) 
        
lista_cond_uno=[]     
lista_output=[]
   
for file in lista_path:        
                   
    reader = FormatReader.create_instance(file)
    lista_stringhe = reader.get_file_content()
    
    reader = Conditions.create_instance(file)
    lista_cond_uno,lista_output= reader[0].path_condition(reader[1])

