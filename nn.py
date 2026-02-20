import pygame
import numpy as np

# ---------------- Activation Functions ----------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)


# ---------------- Feedforward Neural Network ----------------
class FeedforwardNN:
    def _init_(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2


# ---------------- Pygame Visualization ----------------
pygame.init()
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feedforward Neural Network Visualization")

FONT = pygame.font.SysFont("Arial", 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
GREEN = (50, 255, 100)

def draw_network(nn, X, outputs):
    WIN.fill(WHITE)
    
    # Layer positions
    layers = [len(X[0]), len(nn.a1[0]), len(nn.a2[0])]
    x_spacing = WIDTH // (len(layers) + 1)
    
    positions = []
    for i, num_nodes in enumerate(layers):
        y_spacing = HEIGHT // (num_nodes + 1)
        layer_pos = []
        for j in range(num_nodes):
            pos = (x_spacing*(i+1), y_spacing*(j+1))
            layer_pos.append(pos)
            pygame.draw.circle(WIN, BLUE, pos, 25)
        positions.append(layer_pos)
    
    # Draw connections
    for i in range(len(layers)-1):
        for j, (x1, y1) in enumerate(positions[i]):
            for k, (x2, y2) in enumerate(positions[i+1]):
                pygame.draw.line(WIN, BLACK, (x1, y1), (x2, y2), 2)
    
    # Draw outputs on neurons
    for i, layer in enumerate(positions):
        for j, (x, y) in enumerate(layer):
            if i == 0:
                val = X[0][j]  # first input for visualization
            elif i == 1:
                val = nn.a1[0][j]
            else:
                val = outputs[0][j]
            text = FONT.render(f"{val:.2f}", True, GREEN)
            WIN.blit(text, (x-20, y-10))
    
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    nn = FeedforwardNN(input_size=2, hidden_size=2, output_size=1)
    
    # XOR input
    X = np.array([[0,1]])
    
    outputs = nn.forward(X)
    
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_network(nn, X, outputs)
    
    pygame.quit()


if __name__ == "__main__":
    main()