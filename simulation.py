from node import Node
import random

class Simulation():

    def __init__(self, num_nodes, num_nbr, num_nbr_byz, byz_percent):

        self.num_nodes   = num_nodes
        self.num_nbr     = num_nbr
        self.num_nbr_byz = num_nbr_byz
        self.byz_percent = byz_percent

        self.nodes = []
        
        self.create_nodes()
        self.generate_neighbors()

    def create_nodes(self):
        for i in range(self.num_nodes):
            node = Node(i, i%10, i//10)
            self.nodes.append(node)

    def generate_neighbors(self):
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if random(0, 1) < self.num_nbr/self.num_nodes:
                    self.nodes[i].add_neighbor(self.nodes[j])
                    self.nodes[j].add_neighbor(self.nodes[i])

if __name__ == "__main__":
    sim = Simulation(100, 4, 1, 0.1)
    for i in range(10):

