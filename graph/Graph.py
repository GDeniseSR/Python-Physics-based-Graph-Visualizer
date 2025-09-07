from __future__ import annotations
import typing
from collections import deque
from functools import wraps
from enum import Enum
import math
import time

class Order(Enum):
    DEPTH = 1,
    WIDTH = 2

class Graph[T]:
    def __init__(self: typing.Self, adjacency_dict : dict[T, dict[T, float | bool]] = None, debug_log=False):
        if adjacency_dict == None:
            adjacency_dict = {}
        
        self.__adj : dict[T, dict[T, float | bool]] = {}
        for v, neighbors in adjacency_dict.items():
            self.__adj[v] = neighbors.copy()
        
        self.__version = 0
        self.__cache : dict[str, tuple[str, int]] = {}
        
        self.debug_log=debug_log
    
    def versioned_cache(key):
        def decorator(func):
            wraps(func)
            def wrapper(self:typing.Self, *args, **kwargs):
                val, version = self.__cache.get(key, (None, -1))
                if version != self.__version:
                    start = time.perf_counter()
                    val = func(self, *args, **kwargs)
                    end = time.perf_counter()
                    if self.debug_log:
                        print(f"Func: '{func.__name__}' took {end-start} seconds")
                    self.__cache[key] = (val, self.__version)
                return val
            return wrapper
        return decorator
    
    def _change(self):
        if self.debug_log:
            print(f"Change: version = {self.__version} -------------")
        self.__version += 1
    
    
    ### Full graph methods ##########################################
    def copy(self):
        return Graph(self.__adj)
    
    def get_subgraph(self, vertices : set[T]) -> Graph[T]:
        new_adj = {}
        for v in vertices:
            new_adj[v] = {v2 : w for v2, w in self.__adj[v].items() if v2 in vertices}
                
        return Graph(new_adj)
    
    @property
    @versioned_cache("reverse_graph")
    def reverse_graph(self) -> Graph[T]:
        reverse_adj = {v : {} for v in self.__adj.keys()}
        
        for v1, neighbors in self.__adj.items():
            for v2, w in neighbors.items():
                reverse_adj[v2][v1] = w
        
        reverse_graph = Graph(reverse_adj)
        
        return reverse_graph
    
    
    ### Vertex methods ##########################################
    @property
    @versioned_cache("vertices")
    def vertices(self):
        return tuple(self.__adj.keys())
    
    def contains(self: typing.Self, vertex: T) -> bool: 
        return vertex in self.__adj

    def add(self: typing.Self, vertex: T) -> Graph[T]: 
        if not self.contains(vertex):
            self.__adj[vertex] = {}

            self._change()
        
        return self

    def remove(self: typing.Self, vertex: T) -> Graph[T]: 
        if self.contains(vertex):
            self.__adj.pop(vertex)
            
            for v in self.__adj:
                self.__adj[v].pop(vertex, None)
        
            self._change()
        
        return self
        
    def adjacent_vertices(self: typing.Self, vertex: T) -> set[T]: 
        return self.__adj[vertex].keys()
    
    def predecessors(self: typing.Self, vertex: T) -> set[T]: 
        return self.reverse_graph.__adj[vertex].keys()
    
    
    ### Connection methods ##########################################
    
    def connected(self: typing.Self, source: T, target: T) -> bool: 
        return target in self.__adj[source]

    def get_connection_weight(self: typing.Self, source: T, target: T) -> float | bool: 
        return self.__adj[source][target]
    
    def connect(self: typing.Self, source: T, target: T, weight: float|bool) -> Graph[T]: 
        if self.contains(source) and self.contains(target):
            self.__adj[source][target] = weight
            self._change()

        return self

    def disconnect(self: typing.Self, source: T, target: T) -> Graph[T]: 
        if self.contains(source) and self.contains(target):
            self.__adj[source].pop(target)
            self._change()
        return self

    @property
    @versioned_cache("is_directed")
    def is_directed(self):
        # Check symmetry
        for v1, neighbors in self.__adj.items():
            for v2, w in neighbors.items():
                if v1 not in self.__adj[v2] or self.__adj[v2][v1] != w:
                    return True
                
        return False
    
    
    ### Component methods ##########################################
    
    @property
    @versioned_cache("is_connected")
    def is_connected(self) -> bool:
        start = self.vertices[0]
        visited = self.travel_connected_component(start, order=Order.DEPTH)

        return len(visited) == len(self.vertices)


    def travel_connected_component(self, start: T, order: Order):
        if self.is_directed:
            forwards = self._travel_connected_component_forwards(start, order)
            backwards = self._travel_connected_component_backwards(start, order)
            return [v for v in forwards if v in backwards] # A compoñente fortemente conexa é a intersección
        else:
            return self._travel_connected_component_forwards(start, order)
    
    def _travel_connected_component_forwards(self, start: T, order: Order):
        visited : list[T] = []
        vertices_to_visit : deque[T] = deque()
        vertices_to_visit.append(start)
        
        while len(vertices_to_visit) > 0:
            if order == Order.WIDTH: # Uses a queue
                vertex = vertices_to_visit.popleft()
            else: # Uses a stack
                vertex = vertices_to_visit.pop()
            
            visited.append(vertex)
            adjacent = self.adjacent_vertices(vertex)
            
            vertices_to_visit.extend([v for v in adjacent if (v not in visited and v not in vertices_to_visit)])
        return visited
    
    def _travel_connected_component_backwards(self, start: T, order: Order):
        visited : list[T] = []
        vertices_to_visit : deque[T] = deque()
        vertices_to_visit.append(start)
        
        while len(vertices_to_visit) > 0:
            if order == Order.WIDTH: # Usa unha cola
                vertex = vertices_to_visit.popleft()
            else: # Usa unha pila
                vertex = vertices_to_visit.pop()
            
            visited.append(vertex)
            predecessors = self.predecessors(vertex)
            
            vertices_to_visit.extend([v for v in predecessors if (v not in visited and v not in vertices_to_visit)])
        return visited
    
    def travel_full_graph(self, start: T, order: Order) -> list[T]:
        if not self.contains(start):
            raise(f"There is no vertex {start} in the graph")

        visited : list[T] = []
        remaining_vertices = set(self.vertices)  # Create a set of unvisited vertices
        
        while remaining_vertices:
            if len(visited) > 0:
                start = remaining_vertices.pop()  # Pick any vertex from remaining vertices
            
            component = self.travel_connected_component(start, order)
            
            for v in component:
                if v in visited:
                    visited.remove(v)
            visited.extend(component)
            remaining_vertices.difference_update(component)
                
        return visited
    
    @property
    @versioned_cache("connected_components")
    def connected_components(self) -> list[list[T]]:
        """
        In directed graphs returns the strongly connected components
        
        In undirected graphs returns the connected components
        """
        
        connected_components: list[list[T]] = []
        remaining_vertices = set(self.vertices)  # Create a set of unvisited vertices
        
        while remaining_vertices:
            start = remaining_vertices.pop()  # Pick any vertex from remaining vertices
            
            component = self.travel_connected_component(start, order=Order.DEPTH)
            
            connected_components.append(component) 
            remaining_vertices.difference_update(component)
        
        return connected_components
    
    
    
    @property
    @versioned_cache("cut_vertices")
    def cut_vertices(self) -> set[T]:
        """
        In directed graphs returns the strong cut vertices
        
        In undirected graphs return the cut vertices
        """
        if self.is_directed:
            return self.__find_strong_cut_vertices()
        else:
            return self.__find_cut_vertices()
    
    def __find_cut_vertices(self) -> set[T]:
        """
        Tarjan's algorithm
        """
        def depth_fist_search(v, parent=None, visited=None, cut_vertices=None):
            nonlocal low_values
            if visited is None:
                visited = []
            if cut_vertices is None:
                cut_vertices = set()
            
            children = 0
            
            visited.append(v)
            i = len(visited)
            low_values[v] = i

            for u in self.adjacent_vertices(v):
                if u not in visited:
                    children += 1
                    depth_fist_search(u, v, visited, cut_vertices)
                    low_values[v] = min(low_values[v], low_values[u])
                    
                    if parent is not None and i <= low_values[u]:
                        cut_vertices.add(v)
                    
                elif u != parent:
                    low_values[v] = min(low_values[v], visited.index(u) + 1)
            
            if parent is None and children >= 2:
                cut_vertices.add(v)
    
            return visited, cut_vertices
        
        cut_vertices : set[T] = set()
        
        visited : list[T] = []
        
        low_values : dict[T, int] = {}
        
        for v in self.vertices:
            if v not in visited:
                new_component, new_cut_vertices = depth_fist_search(v)

                visited.extend(new_component)
                cut_vertices.update(new_cut_vertices)
        
        return cut_vertices        
    
    
    def __find_strong_cut_vertices(self) -> set[T]:
        """
        Calculates the dominators of the graph and its inverse. The union
        of these two sets is the set of strong cut vertices.
        
        Paper implemented:
        
        Giuseppe F. Italiano, Luigi Laura, Federico Santaroni,
        Finding strong bridges and strong articulation points in linear time,
        Theoretical Computer Science,
        Volume 447,
        2012

        """
        dom : set[T] = self.calculate_graph_dominators()
        dom_r : set[T] = self.reverse_graph.calculate_graph_dominators()
        
        cut_vertices = dom.union(dom_r)
        
        return cut_vertices
    
    
    def calculate_graph_dominators(self) -> dict[T, set[T]]:
        # We get the strongly connected components following a depth search
        strongly_connected_components = self.connected_components
        dom : set[T] = set()
        
        for component in strongly_connected_components:
            if len(component) > 2:
                new_dominators = self.get_component_dominators(component)
                dom.update(new_dominators)

        return dom

    def get_component_dominators(self, component_by_depth : list[T]) -> set[T]:
        """
        We remove the trivial dominators from the set obtained with 'calculate_dominators'.
        That is, for every vertex's dominator list, we remove the start vertex and itself.
        We then flatten the dictionary of dominators into a list, and check if we shall
        add the start vertex as a dominator of its own by manually removing it and checking if
        the number of strongly connected components changed.
        """
        start = component_by_depth[0]
        
        dom = self.get_connected_comp_dominators(component_by_depth)
        dom[start].remove(start)
        for v in component_by_depth[1:]:
            dom[v].remove(start)
            dom[v].remove(v)
        
        dominators = set()
        for v in dom:
            dominators.update(dom[v])

        # For the start vertex, we must check it manually
        subgraph = self.get_subgraph(component_by_depth)
        subgraph.remove(start)
        if len(subgraph.connected_components) > 1:
            dominators.add(start)
        
        return dominators
    
    def get_connected_comp_dominators(self, component_by_depth : list[T]) -> dict[T, set[T]]:
        dom = {v: set(component_by_depth) for v in component_by_depth}
        dom[component_by_depth[0]] = {component_by_depth[0]}
        
        changed = True
        while changed:
            changed = False
            
            # Process each node (skipping the start node, which always only dominates itself)
            for i in range(1, len(component_by_depth)):
                v = component_by_depth[i]
                # New dominator set for v: intersection of dominators of all predecessors
                new_dom = set(dom[v])  # Start with current dom[v] as a basis for comparison
                for u in self.predecessors(v):
                    if u in component_by_depth:
                        new_dom.intersection_update(dom[u])
                new_dom.add(v)  # Each node always dominates itself
                
                # We need to keep checking everything until there's no more updates
                if new_dom != dom[v]:
                    dom[v] = new_dom 
                    changed = True
                            
        return dom

    
    def dijkstra(self, source : T):
        pending = list(self.vertices)

        distances : dict[T, float] = {v : math.inf for v in self.__adj}
        paths : dict[T, list[T]] = {v : [] for v in self.__adj}
        
        distances[source] = 0
        paths[source] = [source]
        
        while pending:
            v = min(pending, key = lambda v : distances[v])
                
            pending.remove(v)
            
            for u in self.adjacent_vertices(v):
                new_distance = distances[v] + self.get_connection_weight(v, u)
                if new_distance < distances[u]:
                    distances[u] = new_distance
                    paths[u] = paths[v].copy()
                    paths[u].append(u)
        
        return distances, paths
    
    def path(self, source: T, target: T) -> list[T]:
        _, paths  = self.dijkstra(source)
        return paths[target]
    
    
    def __str__(self: typing.Self) -> str:
        string = "Vertices: "
        string += ", ".join(str(v) for v in self.__adj.keys()) + "\n\n"
        for v1, neighbors in self.__adj.items():
            for v2, w in neighbors.items():
                string += f"{v1} --- {w} --> {v2}\n"
                
        return string