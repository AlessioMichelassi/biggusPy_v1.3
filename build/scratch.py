"""
ora il problema sembra essere print(x)...

Ho creato una serie di nodi che rappresentano le varie operazioni di python...
c'è ad esempio NumberNode che rappresenta un numero, StringNode che rappresenta una stringa,
ListNode che rappresenta una lista, SetNode che rappresenta un set, ecc...
Ogni nodo ha un menu contestuale che permette di eseguire operazioni su quel tipo di dato.
Ad esempio il nodo NumberNode ha un menu contestuale che permette di settarlo come un random int, un random float, ecc...
Il nodo StringNode ha un menu contestuale che permette di usarlo come replace, upper, lower, ecc...
I nodi variable servono per creare variabili che possono essere usate in altri nodi. Possono essere settati su un
valore oppure se collegati ad un nodo che restituisce il cast se accettabile, ad esempio se collego un nodo NumberNode
ad uno stringNode, il valore del nodo stringNode sarà settato al valore del nodo str(NumberNode). se però collego
uno stringNode ad un nodo NumberNode, il valore del nodo NumberNode se può essere castato a int o float sarà settato,
altrimenti sarà settato a 0.

Ho creato un nodo per le funzioni, che permette di creare una funzione e di usarla in altri nodi. quindi ad esempio
 posso scrivervi dentro:
def my_function(x):
    return x + 1

e in base al tipo di dato che passo alla funzione, il nodo funzione restituirà il tipo di dato corretto.

Ho creato anche un nodo ifNode che permette di fare if, elif, else, ecc... ma non è ancora finito.

e ora sto lavorando al nodo for.

Ho creato un widget che si chiama codeToNode che permette di trasformare del codice python in nodi. Quando i nodi
vengono riconosciuti, vengo aggiunti al canvas, altrimenti vengono ignorati. Il widget è ancora in fase di sviluppo.

per il momento riesco a trasformare codice python in nodi anche un codice complesso:

def SieveOfEratosthenes(n):
    prime_list = []
    for i in range(2, n+1):
        if i not in prime_list:
            print (i)
            for j in range(i*i, n+1, i):
                prime_list.append(j)


crea una function node che contiene il codice sopra.

def add_and_multiply(a, b, c):
    d = a + b
    e = d * c
    return e

x = add_and_multiply(1, 2, 3)
y = add_and_multiply(4, 5, 6)
z = x + y
print(z)

crea una function node che contiene la funzione add_and_multiply, quindi crea una variable node x e una variable node y
gli associa la funzione add_and_multiply a cui collega 3 nodi NumberNode, quindo crea y fa una copia della funzione
perchè viene usata con variabili diverse e la collega come prima a 3 nodi NumberNode, quindi crea una variable node z
che viene collegata a x e y, quindi crea un print node che viene collegato a z.

ora sto testando la funzione:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

crea la lista, crea il for node. Il node For ha due ingressi uno per gli iterables e uno per la funzione da eseguire.

a questo punto ho innanzi tutto un dilemma. print(x) viene riconosciuto come una functionNode e la sua funzione viene
settata come: <ast.Call object at 0x7f9587884520> e non so come fare a settare la funzione come print(x).

l'altra cosa è che il functionNode viene creato dopo il forNode, quindi non so come fare a collegare il forNode alla
functionNode.



"""