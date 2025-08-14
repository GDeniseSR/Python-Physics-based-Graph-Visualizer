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
            nonlocal houses
            for sibling in character.siblings:
                houses[house].connect(character.name, sibling, 0)
                houses[house].connect(sibling, character.name, 0)
            for parent in character.parents:
                houses[house].connect(character.name, parent, 0)
                houses[house].connect(parent, character.name, 0)
            for guardian in character.guardedBy:
                houses[house].connect(character.name, guardian, 0)
                houses[house].connect(guardian, character.name, 0)
        
        # load characters from json file
        characters: list[Character] = []
        with open(filename, "r") as file:
            characters = json.load(file, object_hook=lambda data: Character(**data))

        # create the dict containing all the graphs
        houses = defaultdict(Graph)

        # add all characters to his house graph
        for character in characters:
            x = (random() - 0.5) * 300
            y = (random() - 0.5) * 300
            if isinstance(character.house, str):
                houses[character.house].add(Node(character.name, x, y))
            else:
                for house in character.house:
                    houses[house].add(Node(character.name, x, y))

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
        graph : Graph[Node] = Graph(debug_log=True)

        nodes : dict[str, Node] = {}
        # add all characters to his house graph
        for character in characters:
            node = Node(character.name, random() * 300 + 200, random() * 200 + 140)
            nodes[character.name] = node
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
