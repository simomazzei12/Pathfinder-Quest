# Import the necessary libraries
import pygame  # Library for creating games and visual interfaces
import networkx as nx  # Library for creating and working with graphs
import random  # Library for generating random numbers (used later)

# Initialize pygame to set up the game environment
pygame.init()

# Define screen dimensions and colors for the game
WIDTH, HEIGHT = 800, 600  # Width and height of the game window
WHITE, BLACK, RED, GREEN, BLUE, GRAY, YELLOW = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200), (255, 255, 0)
# Colors are defined using RGB (Red, Green, Blue) values, with each value ranging from 0 to 255)
FONT = pygame.font.SysFont(None, 24)  # Create a font for displaying text on the screen, font size 24, default system font

# Create the game screen (the window where the game is displayed)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder Quest")  # Set the title of the game window

# Initialize global variables to manage the game's state
graph = None  # The graph structure that will represent nodes and connections
pos = None  # Positions of the nodes in the graph
start_node = None  # The starting node in the graph
end_node = None  # The target node in the graph
shortest_path = []  # The shortest path between the start and end nodes (list of nodes)
shortest_path_length = None  # The total weight (value) of the shortest path
selected_path = []  # The path the player selects by clicking on nodes
total_path_weight = [0]  # Running total of weights for the player's selected path
highlighted_edges = []  # Edges (connections) to highlight during gameplay
show_solution = False  # Boolean flag to show or hide the correct solution path

def display_intro_screen():
    """Displays the intro screen with game rules and a Start button."""
    screen.fill(GRAY)  # Fill the background with a gray color
    # Create fonts for the title and rules
    title_font = pygame.font.SysFont(None, 48)  # Larger font for the title
    rule_font = pygame.font.SysFont(None, 24)  # Smaller font for the rules

    # Display the game title in the center of the screen
    title_text = title_font.render("Pathfinder Quest", True, WHITE)  # Render the title text in white
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Center the title on the screen
    screen.blit(title_text, title_rect)  # Draw the title text on the screen

    # Define a list of game rules to display
    rules = [
        "INSTRUCTIONS:",
        "1. The 'value' of each path is shown as a number on the given line",
        "2. The goal is to find path with the shortest total 'value'",
        "3. Click on nodes to create a path",
        "4. Press 'Undo' to remove the last selected node",
        "5. Press 'Show Solution' to see the correct path",
        "6. Close the window to end the game",
    ]

# Loop through each rule and display it on the screen
    for i, rule in enumerate(rules):
        rule_text = rule_font.render(rule, True, WHITE)  # Render each rule as a white text
        rule_rect = rule_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + i * 30))  # Position the rule on the screen with spacing between each line
        screen.blit(rule_text, rule_rect)  # Draw the rule text onto the screen

    # Draw the "Start Game" button
    draw_button("Start Game", WIDTH // 2 - 50, HEIGHT - 100, 100, 40)  # Button at the bottom center of the screen
    pygame.display.flip()  # Update the screen to display all the elements

    # Wait for the player to click "Start Game"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the player closes the window
                pygame.quit()  # Quit the game
                return False  # Stop running the game
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the player clicks the mouse
                mouse_pos = pygame.mouse.get_pos()  # Get the position of the mouse click
                if is_button_clicked(WIDTH // 2 - 50, HEIGHT - 100, 100, 40, mouse_pos):  # Check if the "Start Game" button was clicked
                    return True  # Start the game

def generate_circular_layout(graph, width, height, padding=100):
    """
    Generates a circular layout for the graph nodes and scales it to fit within the screen dimensions.
    Parameters:
        graph: The graph whose nodes need positioning.
        width: The width of the screen.
        height: The height of the screen.
        padding: Optional padding to keep nodes away from screen edges.
    Returns:
        A dictionary of node positions scaled and centered on the screen.
    """
    # Use networkx's circular layout to position nodes in a circle
    pos = nx.circular_layout(graph)
    scale = min(width, height) / 2 - padding  # Scale to fit within the screen with padding

    # Scale and center each node's position
    for node in pos:
        pos[node][0] = int(pos[node][0] * scale + width / 2)  # X-coordinate
        pos[node][1] = int(pos[node][1] * scale + height / 2)  # Y-coordinate
    
    return pos  # Return the updated positions

def handle_click_on_node(node, last_node):
    """
    Handles the player's click on a node, checking if it's a valid move and updating the game state.
    Parameters:
        node: The node clicked by the player.
        last_node: The last node selected by the player.
    Returns:
        True if the move was valid, False otherwise.
    """
    global selected_path, total_path_weight, highlighted_edges
    if graph.has_edge(last_node, node):  # Ensure the nodes are connected
        selected_path.append(node)  # Add the node to the player's selected path
        edge_weight = graph.edges[last_node, node]['weight']  # Get the edge's weight
        total_path_weight[0] += edge_weight  # Add edge weight  # Update the total weight of the path
        highlighted_edges.append((last_node, node))  # Highlight the selected edge
        return True # Move is valid
    return False  # Move is invalid

def undo_last_selection():
    """
    Undoes the player's last selection, removing the last node and its edge from the path.
    Updates the path weight and removes the last highlighted edge.
    """
    global selected_path, total_path_weight, highlighted_edges
    if len(selected_path) > 1:  # If there are multiple nodes in the path
        # Remove the last selected node and update total weight
        last_node = selected_path.pop()  # Remove the last node
        prev_node = selected_path[-1]  # Get the new last node
        edge_weight = graph.edges[prev_node, last_node]['weight']  # Get the edge weight
        total_path_weight[0] -= edge_weight  # Subtract the edge weight
        # Remove the last highlighted edge
        highlighted_edges.pop()
    elif len(selected_path) == 1:
        # If there's only one node left, clear everything
        selected_path.clear()
        total_path_weight[0] = 0  # Reset the path weight
        highlighted_edges.clear()  # Clear highlighted edges


def generate_level_graph(level):
    """
    Generates a graph for the given level with nodes, edges, and weights.
    Parameters:
        level: The current game level, which influences the number of nodes and edges.
    Returns:
        A NetworkX graph object with nodes and weighted edges.
    """
    # Determine the number of nodes based on the level, capped at 10
    nodes_count = min(5 + level * 2, 10)
    graph = nx.Graph()  # Create an empty graph
    graph.add_nodes_from(range(nodes_count))  # Add notes to the graph
    mst = nx.minimum_spanning_tree(nx.complete_graph(nodes_count))  # Generate a Minimum Spanning Tree (MST) from a complete graph
    
    for u, v in mst.edges:
        # Assign random weights (1 to 10) to the edges in the MST
        weight = random.randint(1, 10)
        graph.add_edge(u, v, weight=weight)  # Add edges with weights to the graph

    # Add extra edges to make the graph more complex
    extra_edges = int(nodes_count * 1.0)  # Determine the number of extra edges
    possible_edges = list(nx.non_edges(graph))  # Get all possible edges not already in the graph
    random.shuffle(possible_edges)  # Randomize the order of these edges
    
    for i in range(min(extra_edges, len(possible_edges))):
        u, v = possible_edges[i]  # Select an edge from the shuffled list
        weight = random.randint(1, 10)  # Assign a random weight to the edge
        graph.add_edge(u, v, weight=weight)  # Add the extra edge to the graph
    
    return graph  # Return the completed graph

def setup_level(level, reset_graph=True):
    """
    Sets up the game for a new level, including generating the graph, nodes, and shortest path.
    Parameters:
        level: The current level of the game.
        reset_graph: Whether to generate a new graph for this level.
    """
    global graph, pos, start_node, end_node, shortest_path, shortest_path_length, selected_path, total_path_weight, show_solution, solution_edges
    # Reset game state variables
    selected_path.clear()  # Clear the player's selected path
    total_path_weight[0] = 0  # Reset the total weight of the selected path
    highlighted_edges.clear()  # Clear the highlighted edges
    show_solution = False  # Ensure the solution is not shown initially
    solution_edges = []  # Clear the solution edges for the new round
    
    if reset_graph:
        # Generate a new graph and positions for the nodes
        graph = generate_level_graph(level)
        pos = generate_circular_layout(graph, WIDTH, HEIGHT)  # Layout for nodes
        nodes = list(graph.nodes)  # Get a list of all nodes
        start_node, end_node = random.sample(nodes, 2)  # Randomly select start and end nodes
    
    # Calculate the shortest path and store it
    shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
    # Calculate the total weight of the shortest path
    shortest_path_length = sum(
        graph.edges[shortest_path[i], shortest_path[i + 1]]['weight']
        for i in range(len(shortest_path) - 1)
    )
    
    # Store the edges that make up the shortest path
    solution_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]


def draw_graph():
    """
    Draws the graph on the game screen, including nodes, edges, and highlighting.
    """
    screen.fill(GRAY)  # Fill the background with gray
    node_radius = 15  # Radius of nodes for visualization
    font = pygame.font.SysFont(None, 18)  # Font for displaying text on nodes
    edge_thickness = 6  # Edge thickness for better visibility

    # Draw all edges with conditional coloring based on their state
    for u, v in graph.edges:
        if show_solution and ((u, v) in solution_edges or (v, u) in solution_edges):
            color = RED  # Prioritize solution edges in red
        elif (u, v) in highlighted_edges or (v, u) in highlighted_edges:
            color = YELLOW  # Highlight selected path edges in yellow
        else:
            color = WHITE  # Default color for unselected edges
        pygame.draw.line(screen, color, pos[u], pos[v], edge_thickness)  # Draw the edge

    # Draw all edge weights on top of the edges to ensure they are visible
    for u, v in graph.edges:
        edge_weight = graph.edges[u, v]['weight']  # Get the weight of the edge
        # Calculate the midpoint of the edge to position the weight
        midpoint = ((pos[u][0] + pos[v][0]) // 2, (pos[u][1] + pos[v][1]) // 2)
        weight_text = font.render(str(edge_weight), True, BLACK)  # Render the weight as text
        text_rect = weight_text.get_rect(center=midpoint)  # Position the text at the midpoint
        screen.blit(weight_text, text_rect)  # Draw the weight text on the screen


    # Draw all nodes on top of edges to ensure they are not covered
    for node in graph.nodes:
        color = WHITE  # Default node color
        label = ""  # Label for the node (e.g., Start or End)
        if node == start_node:
            color = GREEN  # Start node color
            label = "Start"  # Label for the start node
        elif node == end_node:
            color = RED  # End node color
            label = "End"  # Label for the end node
        elif node in selected_path:
            color = YELLOW  # Color for nodes in the selected path

        # Draw the node with a black border for better visibility
        pygame.draw.circle(screen, BLACK, pos[node], node_radius + 2)  # Black border
        pygame.draw.circle(screen, color, pos[node], node_radius)  # Node fill color

        if label:
            label_text = font.render(label, True, BLACK)  # Render the node label
            label_rect = label_text.get_rect(center=(pos[node][0], pos[node][1]))  # Position label at node center
            screen.blit(label_text, label_rect)  # Draw the label on the screen

    # Draw action buttons for the game
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
