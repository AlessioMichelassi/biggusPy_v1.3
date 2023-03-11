"""
Ciao Chat, buongiorno stamani volevo tornare a lavorare sul ForNode, che ieri mi ha dato un po' di filo da torcere.

ti ricordo intanto il link al repository di biggusPy, dove è presente l'intero codice:

https://github.com/AlessioMichelassi/biggusPy_v1.3.git

e nella cartella widgets c'è il CodeToNodeWidget.py, dove è presente il codice che ho scritto per convertire il codice
in un nodo. Riesce a riconoscere il forNode, ma non riesce a riconoscere le variabili che vengono usate dentro il forNode.

ti faccio un esempio:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

Riconosce che fruits è una lista, e che c'è un for node e collega fruits al nodo in input, ma non riesce a creare
un nodo function per il forNode, perchè non riesce a riconoscere le variabili che vengono usate dentro il forNode.

Ieri abbiamo fatto varie prove, test, ma nulla. Ho provato a fare un po' di ricerca, ma non ho trovato nulla che mi aiuti.

La mia idea è quella di creare un nodo function per il forNode, che contenga il codice che viene eseguito
dentro il forNode.

La functionNode funziona bene se ho un codice del tipo:
def my_function():
    print("Hello from a function")

Quindi pensavo di utilizzare un qualcosa più del tipo una stringa, che contenga il codice che viene eseguito dentro
il forNode e passa il codice come stringa alla functionNode. Il primo problema è che devo creare un funzione
all'interno di forNode, che analizzi la stringa e la esegua.

Se la stringa contenuta nella functionNode è del tipo:
for x in fruits:\n  print(x)

la funzione che analizza la stringa deve riuscire a capire che elements è una variabile che trova sempre
in inPlugs[0].getValue()

"""


