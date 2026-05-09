
child(X) :- boy(X).
child(X) :- girl(X).


girl(_):- fail.  


gets(X, doll) :- child(X), \+ boy(X).
gets(X, train) :- child(X).
gets(X, lump_of_coal) :- child(X), \+ good(X).

boy(jack).
