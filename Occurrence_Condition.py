# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 19:26:18 2021

@author: gaiad
"""

def Occurrence_Condition(dati,lista_stringhe,chiavi,file,lista_output):
    
    #lista_output=[]
    rip=[]  
            
    for occorrenza in dati[chiavi[2]].keys():
         ripetizioni=0
      
         for parola in lista_stringhe:
       
             if parola==occorrenza:
                ripetizioni+=1
         rip.append(ripetizioni)
      
    if rip==list(dati[chiavi[2]].values()):
           lista_output.append(file)
           
    return lista_output