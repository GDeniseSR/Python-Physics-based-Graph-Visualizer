import visualizer.GraphDrawer
from example.DataLoader import DataLoader

if __name__ == "__main__":
    N = 80
    graphs = DataLoader.load_houses()
    
    for house, graph in graphs.items():
        print(house)
        visualizer.GraphDrawer.main(graph)


