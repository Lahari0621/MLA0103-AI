# Backward Chaining in AI (Horn Clauses)

KB = [
    ("mammal(A)", "vertebrate(A)"),
    ("vertebrate(A)", "animal(A)"),
    ("vertebrate(A),flying(A)", "bird(A)")
]

facts = {"vertebrate('duck')", "flying('duck')", "mammal('cat')"}

def substitute(var, val, expr):
    return expr.replace(var, val)

def backward_chain(goal):
    print(f"Proving: {goal}")
    if goal in facts:
        print(f"✅ {goal} is a fact")
        return True
    for premise, conclusion in KB:
        if conclusion.split("(")[0] in goal:
            var = conclusion[conclusion.find("(")+1:conclusion.find(")")]
            val = goal[goal.find("(")+1:goal.find(")")]
            new_premises = [substitute(var, val, p.strip()) for p in premise.split(",")]
            if all(backward_chain(p) for p in new_premises):
                facts.add(goal)
                print(f"✅ Derived {goal} from {premise} ⇒ {conclusion}")
                return True
    print(f"❌ Cannot prove {goal}")
    return False

# --- Main ---
goal = input("Enter goal (e.g., bird('duck')): ")
if backward_chain(goal):
    print(f"\n✅ Goal {goal} proven.")
else:
    print(f"\n❌ Goal {goal} not proven.")