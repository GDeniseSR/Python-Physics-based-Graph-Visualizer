import GraphDrawer
from DataLoader import DataLoader

if __name__ == "__main__":
    N = 80
    graphs = DataLoader.load_houses()
    
    for house, graph in graphs.items():
        print(house)
        GraphDrawer.main(graph)


