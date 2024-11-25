from node import Node

class Simulation():

    def __init__(self, num_nodes, num_nbr, num_nbr_byz, byz_percent):

        self.num_nodes   = num_nodes
        self.num_nbr     = num_nbr
        self.num_nbr_byz = num_nbr_byz
        self.byz_percent = byz_percent

        self.nodes = []
        
        self.create_nodes()

    def create_nodes(self):
        for i in range(self.num_nodes):
            node = Node(i, i%10, i//10)
            self.nodes.append(node)

if __name__ == "__main__":
    sim = Simulation(100, 4, 1, 0.1)
    sim.create_nodes()
    for i in range(100):
        print(sim.nodes[i].id, sim.nodes[i].x, sim.nodes[i].y)

