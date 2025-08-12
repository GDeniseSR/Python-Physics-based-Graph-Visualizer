import GraphDrawer
from GraphLoader import GraphLoader
from Graph import Graph, Order
from os import system
import math
import cProfile, pstats


if __name__ == "__main__":
    N = 30
    graph = GraphLoader.load_relationships()
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
    stats.print_stats(20)       # top 20 slow functions
    stats.dump_stats("out.prof")

