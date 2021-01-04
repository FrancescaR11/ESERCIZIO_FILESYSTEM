#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 17:35:23 2020

@author: francescaronci, gaiad
"""
from tqdm import tqdm
import time
'''

Creo la funzione che controlla se le colonne del DataFrame di Input contengono valori Nan. 
In tal caso sostituisce i NaN con degli zeri.
Importo il modulo 'tqdm' per aggiornare l'utente sullo stato di esecuzione tramite barra di avanzamento

'''

def replace_Nan_with_zeros(DataFrame):
 
    nomi_colonne=list(DataFrame.columns) # Creo lista contenente i nomi delle colonne del DataFrame
    
    for i in tqdm(range(len(nomi_colonne)),desc='Esecuzione eliminazione NaN'): # Scandisco i nomi delle colonne del DataFrame e aggiorno la barra di avanzamento
     if DataFrame[nomi_colonne[i]].isnull().sum().sum() > 0: # Se la colonna considerata ha dei valori nulli...
        DataFrame[nomi_colonne[i]].fillna(0, inplace=True)   #...li scostituisco con zero
