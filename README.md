# Physics-based Graph Visualizer

Simple graph visualizer and editor.

https://github.com/user-attachments/assets/1b05bc75-4d04-42c3-a2e3-dfa7383b79e8



## Features
- **Force-based node placement** — nodes repel each other and edges act like springs, dynamically adjusting to keep the layout tidy.
- **Interactive editing** — add, remove, and connect nodes using your mouse (click and drag).
- **Supports directed graphs** with arrowed edges.
- **Dynamic component coloring** — each connected component is assigned a unique color.
- **Cut vertex highlighting** — vertices that, when removed, increase the number of connected components are outlined in red.
- **Zooming and panning**.
- **Real-time rendering** — smooth updates at ~60 FPS for graphs of up to 100 nodes.

### **Graph class**:

Generic, versioned graph implementation supporting directed/undirected and weighted/unweighted graphs.

- Adjacency dictionary storage.
- Add/remove vertices and edges.
- Detect if directed, reverse edges, extract subgraphs.
- BFS/DFS traversal.
- Connected components / strongly connected components.
- Cut vertices (Tarjan’s algorithm for non directed graphs).
- Strong articulation points (Implemented the following paper: "Finding strong bridges and strong articulation points in linear time, by Giuseppe F. Italiano, Luigi Laura, Federico Santaroni")
- Dijkstra shortest paths.


## Getting Started

### Dependencies

Python 3.11 and pygame

### Running program

Run Either 'ShowDirectedGraph.py' or 'ShowHousesGraph.py' for example graphs based on Game of Thrones.

### Controls:
- Left Click on empty space: Create a new node.
- Left Click + Drag from one node to another: Create an edge.
- Right Click + Drag: Delete edges that the drag line crosses.
- Middle Mouse Button (or scroll-wheel) drag: Pan the camera.
- Mouse Wheel: Zoom in and out.

## Authors

Gael Denise
