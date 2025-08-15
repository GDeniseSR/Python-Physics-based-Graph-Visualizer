from Character import Character
from Graph import Graph
import json
from collections import defaultdict
from Node import Node
from random import random

class DataLoader:
    @staticmethod
    def load_houses(filename="data.json") -> dict[str, Graph]:
        def add_family_connections(character:Character, house):
            nonlocal houses, nodes
            house_nodes : dict[str, Node] = nodes[house] 
            for sibling in character.siblings:
                if not houses[house].contains(sibling) or sibling not in house_nodes:
                    continue
                houses[house].connect(house_nodes[character.name], house_nodes[sibling], 0)
                houses[house].connect(house_nodes[sibling], house_nodes[character.name], 0)
            for parent in character.parents:
                if not houses[house].contains(parent) or parent not in house_nodes:
                    continue
                houses[house].connect(house_nodes[character.name], house_nodes[parent], 0)
                houses[house].connect(house_nodes[parent], house_nodes[character.name], 0)
            for guardian in character.guardedBy:
                if not houses[house].contains(guardian) or guardian not in house_nodes:
                    continue
                houses[house].connect(house_nodes[character.name], house_nodes[guardian], 0)
                houses[house].connect(house_nodes[guardian], house_nodes[character.name], 0)
        
        # load characters from json file
        characters: list[Character] = []
        
        with open(filename, "r") as file:
            characters = json.load(file, object_hook=lambda data: Character(**data))

        # create the dict containing all the graphs
        houses : dict[str, Graph] = defaultdict(Graph)
        nodes : dict[str, dict[str, Node]] = defaultdict(dict)
        
        # add all characters to his house graph
        for character in characters:
            x = (random() - 0.5) * 300
            y = (random() - 0.5) * 300
            if isinstance(character.house, str):
                node = Node(character.name, x, y)
                houses[character.house].add(node)
                nodes[character.house][character.name] = node
            else:
                for house in character.house:
                    node = Node(character.name, x, y)
                    houses[house].add(node)
                    nodes[house][character.name] = node

        # add connections between characters
        for character in characters:
            if isinstance(character.house, str):
                add_family_connections(character, character.house)
            else:
                for house in character.house:
                    add_family_connections(character, house)
        
        return houses
    
    
    @staticmethod
    def load_relationships(filename="data.json") -> Graph:
        # load characters from json file
        characters: list[Character] = []
        with open(filename, "r") as file:
            characters = json.load(file, object_hook=lambda data: Character(**data))

        # create the dict containing all the graphs
        graph : Graph[Node] = Graph(debug_log=False)

        nodes : dict[str, Node] = {}
        # add all characters to his house graph
        n = len(characters)
        for character in characters:
            node = Node(character.name, random() * 300 + 200, random() * 200 + 140)
            nodes[character.name] = node
        
        for _, node in nodes.items():
            graph.add(node)

        # add connections between characters
        for character in characters:
            for sibling in character.siblings:
                if sibling in nodes:
                    graph.connect(nodes[character.name], nodes[sibling], 1)
            for parent in character.parents:
                if parent in nodes:
                    graph.connect(nodes[character.name], nodes[parent], 1)
            for guardian in character.guardedBy:
                if guardian in nodes:
                    graph.connect(nodes[character.name], nodes[guardian], 1)
            for guarded in character.guardianOf:
                if guarded in nodes:
                    graph.connect(nodes[character.name], nodes[guarded], 1)
            for partner in character.marriedEngaged:
                if partner in nodes:
                    graph.connect(nodes[character.name], nodes[partner], 1)
            
            for ally in character.allies:
                if ally in nodes:
                    graph.connect(nodes[character.name], nodes[ally], 3)
            
            for servant in character.servedBy:
                if servant in nodes:
                    graph.connect(nodes[character.name], nodes[servant], 5)
            for master in character.serves:
                if master in nodes:
                    graph.connect(nodes[character.name], nodes[master], 5)
            
            for victim in character.abducted:
                if victim in nodes:
                    graph.connect(nodes[character.name], nodes[victim], 15)
            for kidnapper in character.abductedBy:
                if kidnapper in nodes:
                    graph.connect(nodes[character.name], nodes[kidnapper], 15)
            
            for victim in character.killed:
                if victim in nodes:
                    graph.connect(nodes[character.name], nodes[victim], 40)
            for killer in character.killedBy:
                if killer in nodes:
                    graph.connect(nodes[character.name], nodes[killer], 40)
        
        return graph
