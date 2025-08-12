from __future__ import annotations
import typing
from collections import deque
from functools import wraps
from enum import Enum
import math

class Order(Enum):
    DEPTH = 1,
    WIDTH = 2

class Graph[T]:
    def __init__(self: typing.Self, vertices: set[T] = set(), edges: set[tuple[T, T, float]] = set()):
        self.__vertices: list[T] = list(vertices)
        self.__matrix: list[list[float | bool]] = [
            [False for _ in range(len(vertices))] for _ in range(len(vertices)) 
        ]
        
        for source, target, weight in edges:
            self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] = weight
        
        self.__version = 0
        self.__cache : dict[str, tuple[str, int]] = {}

    def versioned_cache(key):
        def decorator(func):
            wraps(func)
            def wrapper(self:typing.Self, *args, **kwargs):
                val, version = self.__cache.get(key, (None, -1))
                if version != self.__version:
                    val = func(self, *args, **kwargs)
                    self.__cache[key] = (val, self.__version)
                return val
            return wrapper
        return decorator
    
    def __change(self):
        self.__version += 1
    
    
    ### Full graph methods ##########################################
    def copy(self):
        matrix_copy = [row.copy() for row in self.__matrix]
        return Graph(self.vertices).__set_adjacency_matrix(matrix_copy)
    
    def get_subgraph(self, vertices : set[T]) -> Graph[T]:
        edges = [(v, u, self.__matrix[i][j]) for i, v in enumerate(self.__vertices) for j, u in enumerate(self.__vertices)
                 if v in vertices and u in vertices]
        return Graph(vertices, edges)
    
    @property
    @versioned_cache("reverse_graph")
    def reverse_graph(self) -> Graph[T]:
        reverse_edges = set()
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[i])):
                if self.__matrix[i][j] is not False:
                    reverse_edge  = (self.__vertices[j], self.__vertices[i], self.__matrix[i][j])
                    reverse_edges.add(reverse_edge)
        
        reverse_graph = Graph(self.vertices, reverse_edges)
        return reverse_graph
    
    
    ### Vertex methods ##########################################
    
    @property
    def vertices(self):
        return self.__vertices.copy()    
    
    def contains(self: typing.Self, vertex: T) -> bool: 
        return vertex in self.__vertices

    def add(self: typing.Self, vertex: T) -> Graph[T]: 
        if not self.contains(vertex):
            #add the vertex
            self.__vertices.append(vertex)
            # add a new False to each row
            for row in self.__matrix:
                row.append(False)
            # add a new row for the new vertex
            self.__matrix.append([False for _ in range(len(self.__vertices))])

        self.__change()
        
        return self

    def remove(self: typing.Self, vertex: T) -> Graph[T]: 
        if self.contains(vertex):
            index = self.__vertices.index(vertex)
            # remove the vertex 
            del self.__vertices[index]
            # remove from each row
            for row in self.__matrix:
                del row[index]
            # remove the row for the vertex
            del self.__matrix[index]

        self.__change()
        
        return self
        
    def adjacent_vertices(self: typing.Self, vertex: T) -> set[T]: 
        index = self.__vertices.index(vertex)
        vertices = set()

        for i in range(len(self.__matrix[index])):
            # check in the vertex row every column
            if self.__matrix[index][i] is not False:
                vertices.add(self.__vertices[i])

        return vertices
    
    def predecessors(self: typing.Self, vertex: T) -> set[T]: 
        index = self.__vertices.index(vertex)
        vertices = set()
        
        for i in range(len(self.__matrix[index])):
            # check in the vertex row every column
            if self.__matrix[i][index] is not False:
                vertices.add(self.__vertices[i])

        return vertices
    
    
    ### Connection methods ##########################################
    
    def __set_adjacency_matrix(self, matrix : list[list[float | bool]]):
        self.__matrix = matrix
        self.__change()
        return self
    
    def connected(self: typing.Self, source: T, target: T) -> bool: 
        return self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] is not False

    def get_connection_weight(self: typing.Self, source: T, target: T) -> float | bool: 
        return self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)]
    
    def connect(self: typing.Self, source: T, target: T, weight: float) -> Graph[T]: 
        if self.contains(source) and self.contains(target):
            self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] = weight
            self.__change()

        return self

    def disconnect(self: typing.Self, source: T, target: T) -> Graph[T]: 
        if self.contains(source) and self.contains(target):
            self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] = False
            self.__change()
            
        return self

    @property
    @versioned_cache("is_directed")
    def is_directed(self):
        val = False
        # Check symmetry
        for i in range(len(self.__matrix)):
            for j in range(i, len(self.__matrix)):  # Only need to check upper half
                if self.__matrix[i][j] != self.__matrix[j][i]:
                    val = True
        
        return val
    
    
    ### Component methods ##########################################
    
    @property
    @versioned_cache("is_connected")
    def is_connected(self) -> bool:
        start = self.__vertices[0]
        visited = self.travel_connected_component(start, order=Order.DEPTH)

        return len(visited) == len(self.__vertices)


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
        if start not in self.__vertices:
            raise(f"There is no vertex {start} in the graph")

        visited : list[T] = []
        remaining_vertices = set(self.__vertices)  # Create a set of unvisited vertices
        
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
        remaining_vertices = set(self.__vertices)  # Create a set of unvisited vertices
        
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
            new_dominators = self.get_component_dominators(component, len(strongly_connected_components))
            dom.update(new_dominators)

        return dom

    def get_component_dominators(self, component_by_depth : list[T], connected_component_number) -> set[T]:
        """
        We remove the trivial dominators from the set obtained with 'calculate_dominators'.
        That is, for every vertex's dominator list, we remove the start vertex and itself.
        We then flatten the dictionary of dominators into a list, and check if we shall
        add the start vertex as a dominator of its own by manually removing it and checking if
        the number of strongly connected components changed.
        """
        start = component_by_depth[0]
        
        dom = self.get_conn_comp_dominators(component_by_depth)
        dom[start].remove(start)
        for v in component_by_depth[1:]:
            dom[v].remove(start)
            dom[v].remove(v)
        
        dominators = set()
        for v in dom:
            dominators.update(dom[v])

        copy = self.copy()
        copy.remove(start)
        if len(copy.connected_components) > connected_component_number:
            dominators.add(start)
        
        return dominators
    
    def get_conn_comp_dominators(self, component_by_depth : list[T]) -> dict[T, set[T]]:
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
        pending = self.vertices

        distances : dict[T, float] = {v : math.inf for v in self.__vertices}
        paths : dict[T, list[T]] = {v : [] for v in self.__vertices}
        
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
        result = ""
        max_len_key = max(len(str(vertex)) for vertex in self.__vertices)
        max_len_val = max(len(str(v)) for r in self.__matrix for v in r )
        max_len = max(max_len_key, max_len_val)

        result = result + f"{' ' * max_len} {' '.join([str(vertex).rjust(max_len) for vertex in self.__vertices])}\n"
        
        for i in range(len(self.__vertices)):
            result = result + f"{str(self.__vertices[i]).rjust(max_len)} {' '.join([str(j).rjust(max_len) for j in self.__matrix[i]])}\n"

        return result