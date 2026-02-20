# -------------------------------
# Backward Chaining Implementation
# -------------------------------

from typing import List, Dict, Tuple, Union

# Type definitions
Fact = str
Variable = str
Rule = Tuple[List[str], str]  # (premises, conclusion)

class KnowledgeBase:
    def __init__(self):
        self.facts: List[Fact] = []        # e.g., ["vertebrate('duck')"]
        self.rules: List[Rule] = []        # e.g., (["vertebrate(A)", "flying(A)"], "bird(A)")

    def add_fact(self, fact: Fact):
        self.facts.append(fact)

    def add_rule(self, premises: List[str], conclusion: str):
        self.rules.append((premises, conclusion))

# -------------------------------
# Helper functions for unification
# -------------------------------

def is_variable(x: str) -> bool:
    return x[0].isupper()

def unify(x: str, y: str, theta: Dict[str, str]) -> Union[Dict[str,str], None]:
    """
    Attempt to unify two literals x and y with substitution theta.
    Returns updated substitution or None if cannot unify.
    """
    if theta is None:
        return None
    if x == y:
        return theta
    if is_variable(x):
        return unify_var(x, y, theta)
    if is_variable(y):
        return unify_var(y, x, theta)
    return None  # cannot unify different constants

def unify_var(var: str, x: str, theta: Dict[str,str]) -> Union[Dict[str,str], None]:
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta

# -------------------------------
# Backward Chaining
# -------------------------------

def subst(theta: Dict[str,str], literal: str) -> str:
    """
    Apply substitution theta to a literal.
    """
    for var, val in theta.items():
        literal = literal.replace(var, val)
    return literal

def backward_chain(kb: KnowledgeBase, goal: str, theta: Dict[str,str]={}) -> bool:
    """
    Attempt to prove goal using backward chaining with knowledge base kb.
    Returns True if goal can be derived, else False.
    """
    # 1. Check if goal is a known fact
    for fact in kb.facts:
        theta_new = unify(goal, fact, theta.copy())
        if theta_new is not None:
            return True

    # 2. Try to apply rules
    for premises, conclusion in kb.rules:
        theta_new = unify(goal, conclusion, theta.copy())
        if theta_new is not None:
            # recursively prove all premises
            all_proved = True
            for premise in premises:
                substituted_premise = subst(theta_new, premise)
                if not backward_chain(kb, substituted_premise, theta_new):
                    all_proved = False
                    break
            if all_proved:
                return True

    return False

# -------------------------------
# Example Knowledge Base
# -------------------------------

kb = KnowledgeBase()

# Facts
kb.add_fact('vertebrate("duck")')
kb.add_fact('flying("duck")')
kb.add_fact('mammal("cat")')

# Rules
kb.add_rule(['mammal(A)'], 'vertebrate(A)')
kb.add_rule(['vertebrate(A)'], 'animal(A)')
kb.add_rule(['vertebrate(A)', 'flying(A)'], 'bird(A)')

# -------------------------------
# Query
# -------------------------------

queries = ['bird("duck")', 'animal("cat")', 'bird("cat")']

for query in queries:
    result = backward_chain(kb, query)
    print(f"Can we prove {query}? {'Yes' if result else 'No'}")
