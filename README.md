# ESERCIZIO_FILESYSTEM
Questa versione del software, sviluppata con python 3.7, ha lo scopo di ricevere in ingresso il file "input", contenuto nella cartella dati. Questo file contiente l'informazione su quale porzione del filesystem effettuare la ricerca e una lista delle condizioni che devono essere verificate.
All'interno di questa cartella è presente anche il file 'objects.txt', contenente la lista di oggetti riconoscibili all'interno delle immagini.
In uscita restituisce un file in formato txt contenente la lista dei file che rispettano le condizioni.
Le condizioni finora considerate sono:
- il formato del file che si vuole cercare;
- la presenza nei file di testo di parole con almeno k occorrenze;
- la presenza nei file immagine di oggetti con almeno n occorrenze;
- il formato del file deve essere compreso tra un valore min e uno max;
- la data di creazione del file deve essere compresa tra due date ( min e max) .
La cartella test contiene due sottocartelle che a loro volta contengono i file nei vari formati, utilizzati per eseguire il testing. 
Per poter eseguire il codice è necessario installare:
- os;
- openpyxl;
- pdfplumber;
- tensorflow==2.2.0;
- opencv;
- keras==2.4.3;
- ImageAI==2.1.6.
Per l'esecuzione del programma è consigliabile creare un nuovo ambiente virtuale ed installarvi i requisiti necessari, scpecificati all'interno del file requirements.txt.
Per una migliore leggibilità il programma è stato suddiviso in tre file:
- Main_Program.py, contenente il programma principale che deve essere eseguito;
- Reader_Class.py e Conditions_Classes.py, contenenti le classi e i metodi che vengono importati in Main_Program.py.
Per non far restituire al programma le immagini su cui l'algoritmo effettua l'analisi, sono state apportate delle modifica al file __init__.py di imageai:
 - riga 200: output_type=None;
 - riga 387: elif (output_type==None): return detections;
 - riga:396: elif (output_type==None): return detections.
