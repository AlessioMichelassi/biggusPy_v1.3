n = 0
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for x in iterable:
    n += 1
    a += 1
    b += 1
    c += 1
    d += 1
    e += 1
    f += 1
    g += 1
    if n == 5:
        break

"""
quando nel nodeSearch si trova un ast.For, crea un nodo ForNode, adesso ha solo la parte
senza for, ma avevi ragione te prima:
c'è bisogno che la funzione sia almeno:
for x in iterable:
    n += 1
    a += 1
    b += 1
    c += 1
    d += 1
    e += 1
    f += 1
    g += 1
    if n == 5:
        break
        
per essere calcolata.

Il problema è che n, a, b, c, d, e, f, g, sono variabili che non esistono nel nodo.
iterable lo collego al nodo in input, ma non posso collegare in input anche le variabili n, a, b, c, d, e, f, g.

Queste variabili, diventano outPlugs del nodo ForNode, ovvero il nodo forNode ha un outPlug per ogni variabile che
viene usata dentro il for.

l'altro problema è che all'interno del forNode, non posso usare le variabili n, a, b, c, d, e, f, g, ma devo usare
perchè non sono state inizializzate. quindi devo fare in modo che quando creo la funzione per il ciclo for, le variabili
n, a, b, c, d, e, f, g, scritte tipo:
n = 0
a = 0
b = 0
etc etc
e per ogni variabile che viene usata dentro il for, devo fare in modo che venga aggiornata andando a controllare il loro valore nel codice.
per esempio:

"""