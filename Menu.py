import GraphDrawer
from DataLoader import DataLoader
from Graph import Graph, Order
from os import system
import math
import cProfile, pstats
import random

if __name__ == "__main__":
    N = 60
    graph = DataLoader.load_relationships()
    
    # Let's filter any person who doesn't have enough connections. The minimum will be random between 0 and 2
    for v in graph.vertices:
        if len(graph.adjacent_vertices(v)) <= random.choice([0, 1, 1, 1, 1, 2]):
            graph.remove(v)
    
    n = len(graph.vertices)
    
    print(n)
    if n > N:
        for _ in range(n - N):
            graph.remove(graph.vertices[0])
    
    profiler = cProfile.Profile()
    profiler.enable()
    GraphDrawer.start(graph)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats(30)       # top 20 slow functions
    stats.dump_stats("out.prof")

