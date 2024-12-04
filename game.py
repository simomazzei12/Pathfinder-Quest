import pygame
import networkx as nx
import random

# Initialize pygame
pygame.init()

# Define some constants
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, RED, GREEN, BLUE, GRAY, YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200), (255, 255, 0)
FONT = pygame.font.SysFont(None, 24)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder Quest")

# Global game state variables
graph = None
pos = None
start_node = None
end_node = None
shortest_path = []  # Store the shortest path itself, not just the length
shortest_path_length = None
selected_path = []
total_path_weight = [0]
highlighted_edges = []  # List of edges that should be highlighted
show_solution = False  # Flag to indicate if solution should be shown

def display_intro_screen():
    """Displays the intro screen with game rules and a Start button."""
    screen.fill(GRAY)
    title_font = pygame.font.SysFont(None, 48)
    rule_font = pygame.font.SysFont(None, 24)

    # Title
    title_text = title_font.render("Pathfinder Quest", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Rules
    rules = [
        "INSTRUCTIONS:",
        "1. The 'value' of each path is shown as a number on the given line",
        "2. The goal is to find path with the shortest total 'value'",
        "3. Click on nodes to create a path",
        "4. Press 'Undo' to remove the last selected node",
        "5. Press 'Show Solution' to see the correct path",
        "6. Close the window to end the game",
    ]


    for i, rule in enumerate(rules):
        rule_text = rule_font.render(rule, True, WHITE)
        rule_rect = rule_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + i * 30))
        screen.blit(rule_text, rule_rect)

    # Start Button
    draw_button("Start Game", WIDTH // 2 - 50, HEIGHT - 100, 100, 40)
    pygame.display.flip()

    # Wait for the player to click "Start Game"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_button_clicked(WIDTH // 2 - 50, HEIGHT - 100, 100, 40, mouse_pos):
                    return True  # Start the game

def generate_circular_layout(graph, width, height, padding=100):
    pos = nx.circular_layout(graph)
    scale = min(width, height) / 2 - padding
    
    for node in pos:
        pos[node][0] = int(pos[node][0] * scale + width / 2)
        pos[node][1] = int(pos[node][1] * scale + height / 2)
    
    return pos

def handle_click_on_node(node, last_node):
    global selected_path, total_path_weight, highlighted_edges
    if graph.has_edge(last_node, node):  # Only allow adjacent nodes
        selected_path.append(node)
        edge_weight = graph.edges[last_node, node]['weight']
        total_path_weight[0] += edge_weight  # Add edge weight
        highlighted_edges.append((last_node, node))  # Highlight the selected edge
        return True
    return False

def undo_last_selection():
    global selected_path, total_path_weight, highlighted_edges
    if len(selected_path) > 1:
        # Remove the last selected node and update total weight
        last_node = selected_path.pop()  # Remove the last node
        prev_node = selected_path[-1]  # Get the new last node
        edge_weight = graph.edges[prev_node, last_node]['weight']
        total_path_weight[0] -= edge_weight  # Subtract the edge weight
        # Remove the last highlighted edge
        highlighted_edges.pop()
    elif len(selected_path) == 1:
        # If there's only one node left, clear everything
        selected_path.clear()
        total_path_weight[0] = 0
        highlighted_edges.clear()


def generate_level_graph(level):
    nodes_count = min(5 + level * 2, 10)
    graph = nx.Graph()
    graph.add_nodes_from(range(nodes_count))
    mst = nx.minimum_spanning_tree(nx.complete_graph(nodes_count))
    
    for u, v in mst.edges:
        weight = random.randint(1, 10)
        graph.add_edge(u, v, weight=weight)
    
    extra_edges = int(nodes_count * 1.0)
    possible_edges = list(nx.non_edges(graph))
    random.shuffle(possible_edges)
    
    for i in range(min(extra_edges, len(possible_edges))):
        u, v = possible_edges[i]
        weight = random.randint(1, 10)
        graph.add_edge(u, v, weight=weight)
    
    return graph

def setup_level(level, reset_graph=True):
    global graph, pos, start_node, end_node, shortest_path, shortest_path_length, selected_path, total_path_weight, show_solution, solution_edges
    selected_path.clear()
    total_path_weight[0] = 0
    highlighted_edges.clear()
    show_solution = False  # Reset the solution display flag for the new round
    solution_edges = []  # Clear the solution edges for the new round
    
    if reset_graph:
        # Generate a new graph for the level
        graph = generate_level_graph(level)
        pos = generate_circular_layout(graph, WIDTH, HEIGHT)
        nodes = list(graph.nodes)
        start_node, end_node = random.sample(nodes, 2)
    
    # Calculate the shortest path and store it
    shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
    shortest_path_length = sum(
        graph.edges[shortest_path[i], shortest_path[i + 1]]['weight']
        for i in range(len(shortest_path) - 1)
    )
    
    # Store the edges in the shortest path
    solution_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]


def draw_graph():
    screen.fill(GRAY)
    node_radius = 15
    font = pygame.font.SysFont(None, 18)
    edge_thickness = 6  # Edge thickness for better visibility

    # Draw all edges with conditional coloring for solution edges and highlighted edges
    for u, v in graph.edges:
        if show_solution and ((u, v) in solution_edges or (v, u) in solution_edges):
            color = RED  # Prioritize solution edges in red
        elif (u, v) in highlighted_edges or (v, u) in highlighted_edges:
            color = YELLOW  # Highlight selected path edges in yellow
        else:
            color = WHITE  # Default edge color
        pygame.draw.line(screen, color, pos[u], pos[v], edge_thickness)

    # Draw all edge weights after edges, to ensure weights are visible
    for u, v in graph.edges:
        edge_weight = graph.edges[u, v]['weight']
        midpoint = ((pos[u][0] + pos[v][0]) // 2, (pos[u][1] + pos[v][1]) // 2)
        weight_text = font.render(str(edge_weight), True, BLACK)
        text_rect = weight_text.get_rect(center=midpoint)
        screen.blit(weight_text, text_rect)

    # Draw nodes on top of everything to ensure lines don't cover them
    for node in graph.nodes:
        color = WHITE
        label = ""
        if node == start_node:
            color = GREEN
            label = "Start"
        elif node == end_node:
            color = RED
            label = "End"
        elif node in selected_path:
            color = YELLOW  # Color for selected nodes

        # Draw node with a black border for better visibility
        pygame.draw.circle(screen, BLACK, pos[node], node_radius + 2)  # Black border
        pygame.draw.circle(screen, color, pos[node], node_radius)

        if label:
            label_text = font.render(label, True, BLACK)
            label_rect = label_text.get_rect(center=(pos[node][0], pos[node][1]))
            screen.blit(label_text, label_rect)

    # Draw buttons as part of the graph
    draw_button("Finish", 650, 550, 100, 40)
    draw_button("Undo", 520, 550, 100, 40)
    solution_button_text = "Hide Solution" if show_solution else "Show Solution"
    draw_button(solution_button_text, WIDTH - 150, 10, 130, 40)

    pygame.display.flip()


def get_node_from_position(mouse_pos, radius=20):
    for node, coord in pos.items():
        if (coord[0] - mouse_pos[0]) ** 2 + (coord[1] - mouse_pos[1]) ** 2 < radius ** 2:
            return node
    return None

def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    label = FONT.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(label, label_rect)

def is_button_clicked(x, y, width, height, mouse_pos):
    return x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height

def display_popup(message, button_text, score):
    popup_rect = pygame.Rect(200, 200, 400, 200)
    pygame.draw.rect(screen, WHITE, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 3)

    message_label = FONT.render(message, True, BLACK)
    message_rect = message_label.get_rect(center=(popup_rect.centerx, popup_rect.y + 50))
    screen.blit(message_label, message_rect)

    score_label = FONT.render(f"Score: {score}", True, BLACK)
    score_rect = score_label.get_rect(center=(popup_rect.centerx, popup_rect.y + 90))
    screen.blit(score_label, score_rect)

    button_rect = pygame.Rect(popup_rect.centerx - 50, popup_rect.y + 130, 100, 40)
    draw_button(button_text, button_rect.x, button_rect.y, button_rect.width, button_rect.height)

    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_button_clicked(button_rect.x, button_rect.y, button_rect.width, button_rect.height, event.pos):
                    return "next"

def main():
    # Show the intro screen and wait for user to start the game
    if not display_intro_screen():
        return

    level = 1
    score = 0
    
    running = True
    while running:
        setup_level(level, reset_graph=True)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Properly exit the game
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if is_button_clicked(650, 550, 100, 40, mouse_pos):
                        if abs(total_path_weight[0] - shortest_path_length) <= 1:
                            score += 10
                            result = display_popup("You won!", "Next", score)
                            if result == "next":
                                level += 1
                                setup_level(level, reset_graph=True)
                                break
                        else:
                            result = display_popup("You lost!", "Retry", score)
                            if result == "next":
                                setup_level(level, reset_graph=False)
                                break
                    elif is_button_clicked(520, 550, 100, 40, mouse_pos):
                        undo_last_selection()
                    elif is_button_clicked(WIDTH - 150, 10, 100, 40, mouse_pos):
                        global show_solution
                        show_solution = not show_solution
                    else:
                        node = get_node_from_position(mouse_pos)
                        if node is not None:
                            last_node = selected_path[-1] if selected_path else start_node
                            handle_click_on_node(node, last_node)

            draw_graph()  # This will now handle drawing the buttons


        if not running:
            break

    pygame.quit()

if __name__ == "__main__":
    main()
