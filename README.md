# Pathfinder-Quest
HSG students' project for the course Skills: Programming with Advanced Computer Languages

**Pathfinder Quest** is a game where you find the shortest path between nodes in a graph. You click on nodes to create a path from the start to the end node, trying to match the shortest path length. The game offers visual highlights and lets you toggle to view or hide the solution path.

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
