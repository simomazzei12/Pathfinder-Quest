# Pathfinder-Quest
HSG students' project for the course Skills: Programming with Advanced Computer Languages

**Pathfinder Quest** **Pathfinder Quest: An Interactive Pathfinding Game**

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

To set up and run the game, follow these steps:

### 1. Install Virtual Environment

Use the following commands to create and activate a virtual environment depending on your operating system:

#### On Linux or macOS:

```bash
python3 -m venv name_environment
source name_environment/bin/activate
```

#### On Windows:

```cmd
python -m venv name_environment
name_environment\Scripts\activate
```

Replace `name_environment` with your desired environment name.

### 2. Install Dependencies

Once the virtual environment is active, install the necessary dependencies:

```bash
pip install networkx pygame
```

### 3. Game Overview

This game generates a graph with a start and an end node. Your objective is to find the shortest path between these two nodes. Here’s a quick overview of how the game works:

- **Graph Generation**: A graph is generated at each level with random edge weights.
- **Objective**: Click nodes to create a path from the start node to the end node, trying to match the shortest path.
- **Controls**:
  - **Finish**: Submit your current path for scoring.
  - **Undo**: Remove the last selected node from your path.
  - **Show/Hide Solution**: Toggle to view or hide the shortest path.
  
If your path length closely matches the computed shortest path, you win the round!

### 4. Run the Game

To start playing, run the following command:

```bash
python3 game.py
```

Enjoy playing **Pathfinder Quest**!
```
