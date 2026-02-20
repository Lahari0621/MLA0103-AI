import pygame
import sys
import math

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map Coloring Game")

FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 80, 80)
GREEN = (100, 255, 100)
BLUE = (80, 150, 255)
YELLOW = (255, 255, 100)
COLORS = {"Red": RED, "Green": GREEN, "Blue": BLUE, "Yellow": YELLOW}
color_names = list(COLORS.keys())

# --- Graph (Map) Definition ---
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['A', 'C', 'E'],
    'E': ['B', 'C', 'D']
}

# --- Node positions (for drawing) ---
positions = {
    'A': (200, 200),
    'B': (400, 100),
    'C': (400, 300),
    'D': (600, 200),
    'E': (500, 400)
}

# --- Node colors ---
node_colors = {node: None for node in graph}
selected_color = "Red"

# --- Function to draw the graph ---
def draw_graph():
    screen.fill(WHITE)

    # Draw edges
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            start = positions[node]
            end = positions[neighbor]
            pygame.draw.line(screen, BLACK, start, end, 2)

    # Draw nodes
    for node, (x, y) in positions.items():
        color = node_colors[node]
        pygame.draw.circle(screen, BLACK, (x, y), 40)
        pygame.draw.circle(screen, color if color else GRAY, (x, y), 35)
        text = FONT.render(node, True, BLACK)
        screen.blit(text, (x - 10, y - 12))

    # Draw color palette
    pygame.draw.rect(screen, GRAY, (50, 450, 700, 100), border_radius=15)
    label = FONT.render("Select Color:", True, BLACK)
    screen.blit(label, (60, 460))

    for i, cname in enumerate(color_names):
        rect = pygame.Rect(220 + i * 120, 460, 60, 60)
        pygame.draw.rect(screen, COLORS[cname], rect)
        if cname == selected_color:
            pygame.draw.rect(screen, BLACK, rect, 4)

        txt = SMALL_FONT.render(cname, True, BLACK)
        screen.blit(txt, (220 + i * 120, 525))

    # Display check result
    result_text = check_coloring()
    result_label = FONT.render(result_text, True, BLACK)
    screen.blit(result_label, (300, 550))

    pygame.display.flip()

# --- Check coloring validity ---
def check_coloring():
    for node, neighbors in graph.items():
        for n in neighbors:
            if node_colors[node] and node_colors[n] == node_colors[node]:
                return "❌ Invalid Coloring!"
    if all(node_colors[n] for n in node_colors):
        return "✅ Valid Coloring!"
    return "🟡 In Progress..."

# --- Detect if click is inside node ---
def get_clicked_node(pos):
    for node, (x, y) in positions.items():
        if math.dist(pos, (x, y)) < 40:
            return node
    return None

# --- Main Loop ---
running = True
while running:
    draw_graph()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Color selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Check if clicked on color palette
            for i, cname in enumerate(color_names):
                rect = pygame.Rect(220 + i * 120, 460, 60, 60)
                if rect.collidepoint(mx, my):
                    selected_color = cname

            # Check if clicked on node
            node = get_clicked_node((mx, my))
            if node:
                node_colors[node] = COLORS[selected_color]

pygame.quit()
sys.exit()