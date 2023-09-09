import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Collidable Nodes with Connections")

# Define some colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Node:
    def __init__(self, id, x, y, radius, color):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dragging = False
        self.connections = []

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collision(self, mouse_pos):
        x, y = mouse_pos
        dist = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return dist <= self.radius

    def set_dragging(self, dragging):
        self.dragging = dragging

def draw_nodes(nodes):
    for node in nodes:
        node.draw()

def check_collision(mouse_pos, node):
    x, y = mouse_pos
    dist = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
    return dist <= node.radius

def check_node_collision(node1, node2):
    distance = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
    return distance <= node1.radius + node2.radius

def draw_connections(nodes):
    for node in nodes:
        for connection in node.connections:
            pygame.draw.line(screen, BLUE, (node.x, node.y), (connection.x, connection.y), 2)
            

def main():
    nodes = [Node(0, 100, 100, 30, BLUE), Node(1, 300, 200, 30, BLUE), Node(2, 500, 500, 30, BLUE)]
    nodes[0].connections.append(nodes[1])  # Example connection

    dragging = False
    selected_node = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for node in nodes:
                    if node.check_collision(mouse_pos):
                        selected_node = node
                        node.set_dragging(True)
                        dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                for node in nodes:
                    node.set_dragging(False)
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                selected_node.x = mouse_x
                selected_node.y = mouse_y

        # Check for node collisions
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if check_node_collision(nodes[i], nodes[j]):
                    # Handle collision by moving the nodes apart
                    dx = nodes[i].x - nodes[j].x
                    dy = nodes[i].y - nodes[j].y
                    distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                    overlap = (nodes[i].radius + nodes[j].radius) - distance

                    if distance != 0:
                        move_x = (dx / distance) * (overlap / 2)
                        move_y = (dy / distance) * (overlap / 2)

                        nodes[i].x += move_x
                        nodes[i].y += move_y
                        nodes[j].x -= move_x
                        nodes[j].y -= move_y

        screen.fill(WHITE)
        draw_connections(nodes)
        draw_nodes(nodes)
        pygame.display.flip()

if __name__ == "__main__":
    main()
