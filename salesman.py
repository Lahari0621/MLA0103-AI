from itertools import permutations
n = int(input("Enter the number of cities: "))
cities = []
for i in range(n):
    city = input(f"Enter city name {i + 1}: ")
    cities.append(city)
graph = {}
for city in cities:
    graph[city] = {}
print("\nEnter the distances between each pair of cities:")
for i in range(n):
    for j in range(i + 1, n):
        dist = int(input(f"Distance between {cities[i]} and {cities[j]}: "))
        graph[cities[i]][cities[j]] = dist
        graph[cities[j]][cities[i]] = dist  
start = input("\nEnter the starting city: ")
shortest_distance = float('inf')
best_route = []
for perm in permutations([city for city in cities if city != start]):
    route = [start] + list(perm) + [start]
    distance = 0
    
    for i in range(len(route) - 1):
        distance += graph[route[i]][route[i + 1]]
    
    if distance < shortest_distance:
        shortest_distance = distance
        best_route = route
print("\nShortest Route:", " -> ".join(best_route))
print("Total Distance:", shortest_distance)