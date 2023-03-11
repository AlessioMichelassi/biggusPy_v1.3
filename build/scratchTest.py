TupleNode_2 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
TupleNode_1 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
a = ()
try:
    a = TupleNode_2 + TupleNode_1
except TypeError:
    print('node must be hashable')
except KeyError:
    print('node not in set')

print(a)
