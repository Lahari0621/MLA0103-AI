% Facts about gender
male(bob).
male(bill).
male(john).
male(tom).
female(sue).
female(mary).
female(linda).
female(alice).

% Facts defining parent-child relationships (parent(Parent, Child))
parent(bill, bob).
parent(mary, bob).
parent(john, bill).
parent(linda, bill).
parent(john, sue).
parent(linda, sue).
parent(bob, alice).
parent(sue, tom).

% Define father: Father(X, Y) means X is father of Y
father(X, Y) :-
    parent(X, Y),
    male(X).

% Define mother: Mother(X, Y) means X is mother of Y
mother(X, Y) :-
    parent(X, Y),
    female(X).

% Define sibling relationship: siblings share a parent
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% Define brother: Brother(X, Y) means X is brother of Y
brother(X, Y) :-
    sibling(X, Y),
    male(X).

% Define sister: Sister(X, Y) means X is sister of Y
sister(X, Y) :-
    sibling(X, Y),
    female(X).

% Define grandfather: Grandfather(X, Z) means X is grandfather of Z
grandfather(X, Z) :-
    father(X, Y),
    parent(Y, Z).

% Define grandchild: Grandchild(X, Y) means X is grandchild of Y
grandchild(X, Y) :-
    parent(Y, Z),
    parent(Z, X).

% Define uncle: Uncle(X, Y) means X is uncle of Y
uncle(X, Y) :-
    brother(X, P),
    parent(P, Y).

