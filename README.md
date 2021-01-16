# ESERCIZIO_FILESYSTEM
Questa versione del software ha lo scopo di ricevere in ingresso il file "input", contenuto nella cartella dati. Questo file contiente l'informazione su quale porzione del filesystem effettuare la ricerca e una lista delle condizioni che devono essere verificate.
All'interno di questa cartella è presente anche il file 'objects.txt', contenente la lista di oggetti riconoscibili all'interno delle immagini.
In uscita restituisce un file in formato txt contenente la lista dei file che rispettano le condizioni.
Le condizioni finora considerate sono:
- il formato del file che si vuole cercare;
- la presenza nei file di testo di parole con k occorrenze;
- la presenza nei file immagine di oggetti con n occorrenze;
- il formato del file deve essere compreso tra un valore min e uno max;
- la data di creazione del file deve essere compresa tra due date ( min e max) .
La cartella test contiene due sottocartelle che a loro volta contengono i file nei vari formati, utilizzati per eseguire il testing. 
Per poter eseguire il codice è necessario installare i seguenti moduli:
- os;
- argparse;
- openpyxl;
- pdfplumber;
- ObjectDetection.
Inoltre, per eseguire il programma senza warning è necessario installare:
- openpyxl;
- pdfplumber;
- tensorflow==2.2.0;
- opencv;
- keras==2.4.3;
- ImageAI==2.1.6.

