**Pathfinder Quest: An Interactive Pathfinding Game**

Pathfinder Quest is an engaging and educational game designed to help players understand and explore graph theory and pathfinding algorithms in a fun, interactive way. The objective of the game is to find the shortest path between nodes on a graph, leveraging your logical thinking and strategic planning skills.

### How It Works

The game is played on a visual graph, a network of interconnected nodes (points) and edges (lines connecting the nodes). Your task is to navigate the graph, starting from a designated **start node** and reaching an **end node** by selecting a sequence of nodes that forms the shortest possible path. 

### Gameplay Features

1. **Interactive Node Selection**: 
   Players interact with the graph by clicking on nodes. Each click represents a step in the path they are constructing. The sequence of selected nodes forms the path that the player believes is the shortest.

2. **Graph Visualization**:
   The game provides a clear graphical representation of nodes and edges, making it easy to visualize and plan your path. Nodes and edges are dynamically highlighted based on your interactions, creating a visually engaging experience.

3. **Shortest Path Challenge**:
   The ultimate goal is to match the length of the shortest path determined by a built-in pathfinding algorithm. This algorithm uses well-known techniques like Dijkstra's or A* to calculate the most efficient path between the start and end nodes.

4. **Solution Path Toggle**:
   To aid in learning and improve understanding, the game includes a toggle feature to reveal or hide the solution path. This helps players compare their attempts to the algorithmically generated shortest path, offering insights into optimal strategies and potential mistakes.

5. **Feedback and Iteration**:
   After completing a path, the game evaluates the player's selection against the calculated shortest path. Feedback on the length and efficiency of the chosen path encourages players to iterate and refine their strategies.

6. **Dynamic Difficulty**:
   The complexity of the graph can vary, featuring a range of node configurations and edge densities. This ensures the game remains challenging and engaging, catering to players with different levels of familiarity with graph theory.

### Learning Objectives

Pathfinder Quest is not just a game; it's a tool for learning and exploration. By playing, users can:
- Develop an intuitive understanding of graph structures and shortest path algorithms.
- Explore the importance of planning and optimization in decision-making.
- Gain insights into algorithmic problem-solving techniques in a hands-on manner.

### Applications and Benefits

Pathfinder Quest can be used for educational purposes, helping students and enthusiasts learn about fundamental computer science concepts in a practical, interactive way. Additionally, it serves as a tool for improving problem-solving skills and strategic thinking.

Whether you're a computer science student, a math enthusiast, or just someone looking for an entertaining way to challenge your brain, Pathfinder Quest offers a compelling experience that blends learning and fun.

## Setup Instructions

To set up and run the game, follow these steps (For Linux and macOS see below):

## **Windows**

### Step 1: Open Command Prompt
1. Press `Win + R` to open the "Run" dialog box.
2. Type `cmd` and press Enter. This opens the Command Prompt.

### Step 2: Create a Virtual Environment
1. Navigate to the folder where you want your environment (e.g., `C:\Projects`):
   ```cmd
   cd C:\Projects
   ```
2. Create a virtual environment:
   ```cmd
   python -m venv myenv
   ```
   Replace `myenv` with the name you want for your environment.

### Step 3: Activate the Environment
1. Activate the virtual environment:
   ```cmd
   myenv\Scripts\activate
   ```
   You'll see `(myenv)` appear in the prompt, meaning the environment is active.

### Step 4: Install Dependencies
1. Use pip to install packages:
   ```cmd
   pip install networkx pygame
   ```


---

**## **Linux****


### Step 1: Create a Virtual Environment
1. Navigate to the folder where you want your environment:
   ```bash
   cd ~/projects
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   ```
   Replace `myenv` with your preferred environment name.

### Step 2: Activate the Environment
1. Activate the virtual environment:
   ```bash
   source myenv/bin/activate
   ```
   The prompt will now show `(myenv)`.

### Step 3: Install Dependencies
1. Use `pip` to install libraries or tools:
   ```bash
   pip install networkx pygame
   ```

---

## **macOS**


### Step 1: Open Terminal
1. Open Terminal from the **Applications > Utilities** folder or by searching "Terminal" in Spotlight.

### Step 2: Create a Virtual Environment
1. Navigate to the folder where you want your environment:
   ```bash
   cd ~/projects
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   ```
   Replace `myenv` with your preferred name.

### Step 3: Activate the Environment
1. Activate the virtual environment:
   ```bash
   source myenv/bin/activate
   ```
   You’ll see `(myenv)` in the terminal prompt.

### Step 4: Install Dependencies
1. Use `pip` to install any required libraries:
   ```bash
   pip install networkx pygame
   ```

---

## **General Notes for All Platforms**

- **Deactivate the Environment**:
  - When done, deactivate the environment:
    ```bash
    deactivate
    ```
- **Reactivate Later**:
  - Go back to the folder and use the `activate` command again.



###  Game Overview

This game generates a graph with a start and an end node. Your objective is to find the shortest path between these two nodes. Here’s a quick overview of how the game works:

- **Graph Generation**: A graph is generated at each level with random edge weights.
- **Objective**: Click nodes to create a path from the start node to the end node, trying to match the shortest path.
- **Controls**:
  - **Finish**: Submit your current path for scoring.
  - **Undo**: Remove the last selected node from your path.
  - **Show/Hide Solution**: Toggle to view or hide the shortest path.
  
If your path length closely matches the computed shortest path, you win the round!

##  Run the Game
To start playing, run the following command:

###  Windows
```cmd
python game.py
```
### Linux and macOS
```bash
python3 game.py
```

##  Error handling:
---
Please make sure:
- Your terminal or command prompt is inside the directory where game.py is located
- The required Python dependencies (like pygame and networkx) are installed in the active virtual environment

Enjoy playing **Pathfinder Quest**!
