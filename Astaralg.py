import pygame
import sys
import math
import heapq

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Game")

FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (80, 150, 255)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
ORANGE = (255, 180, 80)
PURPLE = (180, 100, 255)
RED = (255, 80, 80)

# --- Graph Definition ---
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 3, 'E': 5},
    'C': {'A': 4, 'F': 2},
    'D': {'B': 3, 'E': 1, 'F': 1},
    'E': {'B': 5, 'D': 1, 'F': 2},
    'F': {'C': 2, 'D': 1, 'E': 2}
}

positions = {
    'A': (150, 250),
    'B': (300, 150),
    'C': (300, 350),
    'D': (500, 150),
    'E': (500, 350),
    'F': (650, 250)
}

start_node = None
goal_node = None

# --- Heuristic ---
def heuristic(n1, n2):
    (x1, y1), (x2, y2) = positions[n1], positions[n2]
    return math.hypot(x2 - x1, y2 - y1)

# --- A* Algorithm ---
def astar(start, goal):
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    visited_order = []

    while open_heap:
        current = heapq.heappop(open_heap)[1]
        visited_order.append(current)

        if current == goal:
            break

        for neighbor, weight in graph[current].items():
            tentative_g = g_score[current] + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    path = []
    node = goal
    if node not in came_from and node != start:
        return visited_order, [], float('inf')
    while node in came_from:
        path.insert(0, node)
        node = came_from[node]
    path.insert(0, start)
    return visited_order, path, g_score[goal]

# --- Draw Graph ---
def draw_graph(visited=set(), path=set()):
    screen.fill(WHITE)

    # Draw edges
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            start_pos = positions[node]
            end_pos = positions[neighbor]
            pygame.draw.line(screen, GRAY, start_pos, end_pos, 3)
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2
            text = SMALL_FONT.render(str(weight), True, BLACK)
            screen.blit(text, (mid_x - 10, mid_y - 10))

    # Draw nodes
    for node, (x, y) in positions.items():
        color = BLUE
        if node in visited:
            color = YELLOW
        if node in path:
            color = GREEN
        if node == start_node:
            color = ORANGE
        if node == goal_node:
            color = PURPLE
        pygame.draw.circle(screen, BLACK, (x, y), 40)
        pygame.draw.circle(screen, color, (x, y), 35)
        text = FONT.render(node, True, BLACK)
        screen.blit(text, (x - 10, y - 12))

    # Instructions
    instruction = "Click Start Node" if not start_node else \
                  "Click Goal Node" if not goal_node else "Pathfinding..."
    text_inst = FONT.render(instruction, True, RED)
    screen.blit(text_inst, (50, 20))

    pygame.display.flip()

# --- Detect clicked node ---
def get_clicked_node(pos):
    for node, (x, y) in positions.items():
        if math.dist(pos, (x, y)) < 40:
            return node
    return None

# --- Main Loop ---
running = True
visited_order, final_path, cost = [], [], 0
step = 0  # animation step

while running:
    draw_graph(set(visited_order[:step]), set(final_path[:step]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = get_clicked_node(event.pos)
            if clicked:
                if not start_node:
                    start_node = clicked
                elif not goal_node:
                    goal_node = clicked
                    visited_order, final_path, cost = astar(start_node, goal_node)
                    print("Node Expansion Order:", " → ".join(visited_order))
                    print("Final Path:", " → ".join(final_path))
                    print(f"Total Cost: {cost}")
                    step = 0  # reset animation

    if start_node and goal_node and step < len(visited_order):
        step += 1
        pygame.time.delay(500)

pygame.quit()
sys.exit()
