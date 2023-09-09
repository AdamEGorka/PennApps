import pygame
import sys
import time 
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collidable Nodes with Connections")

# Define some colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Globals yipee
nodes = {} # dictionary of nodes
highest_id = -1
events = [] # store all events to be performed in next step in a list 

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
        font = pygame.font.Font(None, 20)  # Create a font object
        text = font.render(str(self.id), True, WHITE)  # Render the text
        text_rect = text.get_rect(center=(self.x, self.y))  # Position the text
        screen.blit(text, text_rect)  # Blit the text onto the screen

    def check_collision(self, mouse_pos):
        x, y = mouse_pos
        dist = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return dist <= self.radius

    def set_dragging(self, dragging):
        self.dragging = dragging


# BUTTON USED FOR STEP FORWARD
class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def draw_nodes(nodes):
    for node in nodes.values():
        node.draw()

def check_collision(mouse_pos, node):
    x, y = mouse_pos
    dist = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
    return dist <= node.radius

def check_node_collision(node1, node2):
    distance = ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5
    return distance <= node1.radius + node2.radius

def draw_connections(nodes):
    for node in nodes.values():
        for connection in node.connections:
            pygame.draw.line(screen, BLUE, (node.x, node.y), (connection.x, connection.y), 2)
            
      
      
def add_connection(n1, n2):
    add_event(lambda: __add_connection(n1, n2))
               
def __add_connection(id1, id2):
    n1 = nodes[id1]
    n2 = nodes[id2]
    n1.connections.append(n2)
    n2.connections.append(n1)               

# def __add_connection(n1, n2):  # changing to do it by id instead of node object
#     n1.connections.append(n2)
#     n2.connections.append(n1)
    
def remove_connection(n1, n2):
    add_event(lambda: __remove_connection(n1, n2))

def __remove_connection(n1, n2):
    n1.connections.remove(n2)
    n2.connections.remove(n1)

    
def add_node(x = None, y = None, color = BLUE, id = None):
    add_event(lambda: __add_node(x, y, color, id))
    
def __add_node(x, y, color = BLUE, id = None):
    print("adding node")
    radius = 30
    global highest_id
    global nodes    
    
    if id is None:
        highest_id += 1
        
    if x is None:
        x = random.randint(radius, SCREEN_WIDTH - radius)
    if y is None:
        y = random.randint(radius, SCREEN_HEIGHT - radius)

    new_id = highest_id if id is None else id
    
    nodes[new_id] = Node(new_id, x, y, radius, color)
    
def remove_node(id):
    add_event(lambda: __remove_node(id))
    
def __remove_node(id):
    global nodes
    n = nodes[id]
    for m in n.connections:
        m.connections.remove(n)
    del nodes[id]

def add_event(event_function):
    events.append(event_function)
    
def apply_events():
    print(events)
    for event in events:
        event()
    events.clear()


def visualizer():
    
    # add some nodes for testing :D
    # add_node(100, 100)
    # add_node(200, 200)
    add_node()
    add_node()
        
    add_connection(0, 1)
    
    #nodes[0].connections.append(nodes[1])  # Example connection
    
    step_button = Button(600, 500, 150, 50, BLUE, "Step")

    dragging = False
    selected_node = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if step_button.check_click(mouse_pos):
                    # Perform step forward action
                    print("Step Forward clicked!")
                    apply_events()
                    print(nodes)
                    print(len(nodes))
                
                for node in nodes.values():
                    if node.check_collision(mouse_pos):
                        selected_node = node
                        node.set_dragging(True)
                        dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                for node in nodes.values():
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
        step_button.draw()
        pygame.display.flip()
        

if __name__ == "__main__":
    visualizer()
