import signal
import sys
import time
from random import random
from node import Node

class Simulation:
    def __init__(self, num_nodes, num_nbr, prob_infection, delay_prob):
        self.num_nodes = num_nodes
        self.num_nbr = num_nbr
        self.prob_infection = prob_infection
        self.delay_prob = delay_prob
        self.nodes = []
        self.create_nodes()
        self.generate_neighbors()

    def create_nodes(self):
        for i in range(self.num_nodes):
            node = Node(i, i % 10, i // 10)
            self.nodes.append(node)

    def generate_neighbors(self):
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random() < self.num_nbr / self.num_nodes:
                    self.nodes[i].add_neighbor(self.nodes[j])
                    self.nodes[j].add_neighbor(self.nodes[i])

    def stop_simulation(self):
        print("Stopping simulation...")
        for node in self.nodes:
            node.stop()

if __name__ == "__main__":
    def signal_handler(sig, frame):
        sim.stop_simulation()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    sim = Simulation(num_nodes=100, num_nbr=4, prob_infection=1, delay_prob=0.1)

    print(sim.nodes[0])

    node1 = sim.nodes[0]

    node1.send_message("Hello", node1.neighbors[0])

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)