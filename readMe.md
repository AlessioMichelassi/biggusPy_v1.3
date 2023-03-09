[![PayPal](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/alessiomichelassi)
ITA:
BiggusPy è un editor di nodi che ti consente di programmare in modo visuale utilizzando una interfaccia 
grafica intuitiva. Ciascun nodo rappresenta un'istruzione python, come una variabile, una stringa o un 
comando print, che può essere collegato ad altri nodi per creare un flusso di dati e una serie di operazioni. 
Collegando ad esempio una stringa al nodo print posso stampare sullo schermo la celebre frase "Hello World".

ENG:
BiggusPy is a node editor that allows you to program visually using an intuitive graphics interface. Each node
is like a python statement, such as a variable, string or a print command, which can be connected to other nodes 
to create a data stream and a series of operations.
For example, by connecting a string to the print node, you can print the famous phrase "Hello World" on the screen.

![biggusPy](https://user-images.githubusercontent.com/59560406/212428865-288e6843-923e-41ff-b55b-65ede0b39aea.png)

ITA:
Il programma è ancora in fase embrionale ma è già possibile effettuare alcune operazioni base come collegare, 
scollegare, cancellare o salvare un progetto e aprire un progetto. BiggusPy è in grado d'interpretare il codice 
python scritto in modo tradizionale e creare una struttura di nodi corrispondente, rendendo la transizione 
dalla programmazione testuale alla programmazione visiva più semplice e l'obbiettivo è quello di poter esportare 
il progetto sviluppato in BiggusPy in un codice python tradizionale per la condivisione o la distribuzione, ma anche 
creare un programma che permetta di fare a chi non ha le basi di programmazione di poter costruire qualcosa. L'idea
è che la maggior parte delle persone sanno come collegare le cose tra loro e facendo le loro prove in questo modo
possono creare qualcosa di interessante senza dover imparare a programmare.

ENG:
The program is still in its embryonic phase, but it is already possible to perform some basic operations such
as connecting, disconnecting, deleting, or saving a project, and opening a project. BiggusPy is capable 
of interpreting Python code written in the traditional way and creating a corresponding structure of nodes, 
making the transition from textual programming to visual programming easier. The goal is to be able to export 
the project developed in BiggusPy into traditional Python code for sharing or distribution. Additionally, 
the aim is to create a program that allows people without programming knowledge to build something tinkering with node. 
The idea is that most people know how to connect things together, and by experimenting in this way, they can create 
something interesting without having to learn how to code.

ITA:
E' sicuramente un modo diverso di visualizzare il codice e ha il vantaggio di far guardare il proprio progetto 
da un punto di vista diverso e questo in molte occasioni, si traduce in un debugging più avanzato anche perchè 
il nuo modo di visualizzare il codice permette di vedere eventuali errori che potrebbero essere difficili 
da individuare con i sistemi di programmazione tradizionali. Ad esempio, la connessione tra i nodi rende 
immediatamente evidente se si stanno passando parametri sbagliati in una funzione o se si sta utilizzando 
un oggetto invece di un altro. Questo rende BiggusPy uno strumento potente per la risoluzione degli errori 
e per la creazione di codice pulito e ben strutturato.

ENG:
It is certainly a different way of visualizing code, and it has the advantage of looking at one's project from 
a different point of view. In many cases, this translates into more advanced debugging, as the new way of 
visualizing code makes it easier to spot errors that could be difficult to identify with traditional programming 
systems. For example, the connection between nodes immediately highlights if incorrect parameters are being passed 
to a function or if an object is being used instead of another. This makes BiggusPy a powerful tool for error 
resolution and for creating clean and well-structured code.

ITA:
Alcuni nodi sono presenti nel menù contestuale quindi, per poterli inserire basta premere il tasto destro e 
selezionare il nodo da inserire dal menu. Non sono presenti ancora tutti i comandi di Python, però ce ne sono già 
alcuni che permettono di creare un'ampia gamma di esempi. Un altro modo Per inserire nodi nella scena è usando
il tasto tab, scrivere il nome del nodo, premere invio e boom, il nodo sarà pronto li ad essere collegato. 

ENG:
Some nodes are available in the contextual menu, so to insert them, simply right-click and select the node to 
insert from the menu. Not all Python commands are available yet, but there are already some that allow for a 
wide range of examples to be created. Another way to insert nodes into the scene is by using the tab key, 
typing the node name, pressing enter, and boom, the node will be ready to be connected.


IF YOU ARE A DEVELOPER AND YOU WANT TO CONTRIBUTE TO THE PROJECT, YOU CAN DO IT!

ITA:
Il programma è stato sviluppato in collaborazione con Chat Bot Ai e mi ha dato un boost di conoscenze incredibili; E'
stato scritto in python utilizzando la versione dalla 3.7 alla 3.11 e utilizza alcune librerie come ast per lavorare 
il codice, jSon per la serializzazione delle classi e PyQt5 per la creazione dell'interfaccia. Dovrebbe erre compatibile 
con la nuova versione di PyQt6, purtroppo da alcuni test soprattutto con la parte multimediale ho visto che per alcune
cose la versione precedente ha una marcia in più. Alcune chiamate non sono più compatibili nella versione successiva, 
ma più in là farò probabilmente un upgrade.

ENG:
The program was developed in collaboration with Chat Bot Ai and it gave me an incredible boost of knowledge. I
t was written in Python using versions 3.7 to 3.11 and uses some libraries such as ast to work with the code, 
jSon for class serialization, and PyQt5 for creating the interface. It should be compatible with the new version 
of PyQt6, but unfortunately, from some tests, especially with multimedia parts, I have seen that the previous version 
has some advantages in certain areas. Some calls are no longer compatible in the later version, 
but I may upgrade later on.

ITA:
E' un programma scritto a oggetti, ma non è molto hardcore, anzi ho tentato di mantenere il codice il più pulito 
possibile per mantenere alta la leggibilità. Il codice quindi è suddiviso in varie cartelle diviso per argomenti,
nella graphicElements quindi ci sono gli oggetti che possono essere inseriti nella scena, nella graphicEngine, 
gli oggetti per l'overrides dei motori grafici, in widgets, il canvas per creare l'editor vero e proprio ed 
esternamente alle cartelle sono presenti solo due file main.py che fa partire il programma e mainWin che in qt 
si occupa di creare la finestra principale con il menu, la status bar, il menu e via discorrendo.

ENG:
It is an object-oriented program, but it is not very hardcore. In fact, I have tried to keep the code as clean as 
possible to maintain high readability. The code is divided into various folders according to topics. 
For example, in "graphicElements," there are objects that can be inserted into the scene, in "graphicEngine," 
there are objects for overriding the graphic engines, and in "widgets," there is the canvas for creating the actual 
editor. Outside of the folders, there are only two files: "main.py," which starts the program, and "mainWin," 
which in qt is responsible for creating the main window with the menu, status bar, and so on.

ITA:
La struttura dei nodi è stata programmata, mettendo insieme tre classi, una per la parte dati, una per la 
parte grafica che si occupa di disegnare il nodo nella canvas e una classe interfaccia che è quella che si prefigge
di fare fra ponte fra i dati e la grafica, ha funzioni per la modifica dei nodi in modo da farlo adattare alle 
varie esigenze e in più è quella che viene richiamata al momento della creazione. 

ENG:
The structure of the nodes was programmed by combining three classes, one for the data part, one for the 
graphic part that is responsible for drawing the node in the canvas, and one interface class that is responsible
for bridging the data and graphics. It has functions for modifying the nodes in order to adapt them to
various needs, and it is the one that is called at the time of creation.

ITA:
I nodi veri e propri vengono poi creati in base alla libreria di rifermimento che al momento è python. Per creare ad
esempio un NumberNode basta creare un file Python che fa l'override della classe data e inserendo alcune proprietà,
metodi e variabili amplia la classe astratta in modo da mimare una istruzione di int, come funzione per il casting, ma 
anche come variabile che può quindi essere collegata a un SumNode che ha due ingressi e che fornisce in uscita 
una semplice somma. La funzione più complessa è la function nella quale si può inserire una funzione qualsiasi 
e il nodo si ridimensiona in modo da avere tanti ingressi, quante uscite sono necessarie per poter 
calcolare il risultato:

ENG:
The actual nodes are then created based on the reference library, which is currently Python. To create, 
for example, a NumberNode, you simply create a Python file that overrides the interface class and adds some properties, 
methods, and variables to expand the abstract class to mimic an int instruction, such as a function for casting, 
as well as a variable that can be connected to a SumNode that has two inputs and provides a simple sum as output.
The most complex function is the functionNode, in which you can insert any function and the node resizes to have as many
inputs as outputs are needed to calculate the result:

La funzione:
'''
def add_and_multiply(a, b, c):
    d = a + b
    e = d * c
    return e
'''

ITA:
può essere trasformata in un nodo. Grazie alla libreria ast si può calcolare che ha tre ingressi (a, b, c) e una 
uscita e. 

ENG:
can be transformed into a node. Thanks to the ast library, you can calculate that it has three inputs (a, b, c) and one
output e.


ITA:
Per facilitare la creazione di nodi ho creato un editor grafico scratchNode che nella versione finale farà parte di 
biggusPy. E' composto da un editor grafico chiamato pixelSmith che permette di creare nodi graficamente, e da un
code editor ArguePy che nonostante ancora non abbia uno spell corrector, permette di scrivere codice python, indentare
e ha alcune funzioni utili durante la scrittura del codice come l'auto completamento delle parentesi, delle virgolette
dei commenti e via discorrendo.

ENG:
To facilitate the creation of nodes, I created a graphical scratchNode editor that will be part of biggusPy in the final version.
It is composed of a graphical editor called pixelSmith that allows you to create nodes graphically, and a code editor ArguePy
that, despite not having a spell corrector yet, allows you to write Python code, indent and has some useful functions during
the writing of the code such as the automatic completion of parentheses, quotes, comments, and so on.
