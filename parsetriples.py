# ---------------- Ontology Graph Builder ----------------

# Example ontology triples (subject, predicate, object)
triples = [
    ("Dog", "rdfs:subClassOf", "Mammal"),
    ("Cat", "rdfs:subClassOf", "Mammal"),
    ("Mammal", "rdfs:subClassOf", "Animal"),
    ("Animal", "rdfs:subClassOf", "LivingBeing"),
    ("Fish", "rdfs:subClassOf", "Animal"),
    ("Shark", "rdfs:subClassOf", "Fish"),
]

# ---------------- Build Knowledge Graph ----------------
def build_knowledge_graph(triples):
    graph = {}
    for subj, pred, obj in triples:
        if pred == "rdfs:subClassOf":
            if obj not in graph:
                graph[obj] = set()
            graph[obj].add(subj)
    return graph

# ---------------- Query Functions ----------------

# Find all subclasses (direct + indirect)
def find_all_subclasses(graph, superclass):
    subclasses = set()
    direct = graph.get(superclass, set())

    for sub in direct:
        subclasses.add(sub)
        subclasses |= find_all_subclasses(graph, sub)  # recursive call

    return subclasses

# Check if one class is subclass of another
def is_subclass(graph, subclass, superclass):
    # Direct subclass?
    if subclass in graph.get(superclass, set()):
        return True

    # Check indirect subclasses recursively
    for sub in graph.get(superclass, set()):
        if is_subclass(graph, subclass, sub):
            return True
    return False

# ---------------- Main ----------------
if __name__ == "__main__":
    graph = build_knowledge_graph(triples)
    print("Knowledge Graph (Superclass → Subclasses):")
    for key, value in graph.items():
        print(f"  {key} → {', '.join(value)}")

    print("\n--- Queries ---")

    # Query 1: Find all subclasses of 'Animal'
    target_class = "Animal"
    result = find_all_subclasses(graph, target_class)
    print(f"All subclasses of '{target_class}': {', '.join(sorted(result))}")

    # Query 2: Check subclass relationship
    subclass, superclass = "Dog", "LivingBeing"
    print(f"\nIs '{subclass}' a subclass of '{superclass}'? → {is_subclass(graph, subclass, superclass)}")

    subclass, superclass = "Shark", "Mammal"
    print(f"Is '{subclass}' a subclass of '{superclass}'? → {is_subclass(graph, subclass, superclass)}")