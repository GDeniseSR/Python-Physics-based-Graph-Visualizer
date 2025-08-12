from Character import Character
from Graph import Graph
import json
from collections import defaultdict
from Node import Node
from random import random

class GraphLoader:
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
        graph : Graph[Node] = Graph()

        # add all characters to his house graph
        for character in characters:
            graph.add(Node(character.name, random() * 300 + 200, random() * 200 + 140))

        # add connections between characters
        for character in characters:
            for sibling in character.siblings:
                graph.connect(character.name, sibling, 1)
            for parent in character.parents:
                graph.connect(character.name, parent, 1)
            for guardian in character.guardedBy:
                graph.connect(character.name, guardian, 1)
            for guarded in character.guardianOf:
                graph.connect(character.name, guarded, 1)
            for partner in character.marriedEngaged:
                graph.connect(character.name, partner, 1)
            
            for ally in character.allies:
                graph.connect(character.name, ally, 3)
            
            for servant in character.servedBy:
                graph.connect(character.name, servant, 5)
            for master in character.serves:
                graph.connect(character.name, master, 5)
            
            for victim in character.abducted:
                graph.connect(character.name, victim, 15)
            for kidnapper in character.abductedBy:
                graph.connect(character.name, kidnapper, 15)
            
            for victim in character.killed:
                graph.connect(character.name, victim, 40)
            for killer in character.killedBy:
                graph.connect(character.name, killer, 40)
            
        
        return graph
        
        
