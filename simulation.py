import signal
import sys
import time
import random
from node import Node, Message


class Simulation:
    def __init__(self, num_nodes, num_nbr, prob_infection, delay_prob):
        self.num_nodes = num_nodes
        self.num_nbr = num_nbr
        self.prob_infection = prob_infection
        self.delay_prob = delay_prob
        self.nodes = []
        self.update_value = 1

        self.create_nodes()
        self.generate_neighbors()

    def create_nodes(self):
        for i in range(self.num_nodes):
            node = Node(i, i % 10, i // 10, "AntiEntropy", 0.5)
            self.nodes.append(node)

    def generate_neighbors(self):
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < self.num_nbr / self.num_nodes:
                    self.nodes[i].add_neighbor(self.nodes[j])
                    self.nodes[j].add_neighbor(self.nodes[i])

    def generate_update(self):
        starting_node = random.choice(self.nodes)
        starting_node.message.update(Message(self.update_value, "Updated Data"))
        starting_node.state = "Infected"
        self.update_value += 1

    def run(self):
        
        self.generate_update()
        try:
            while True:
                time.sleep(2)
                count = sum([1 for node in self.nodes if node.state == "Infected"])
                print(f"Infected Nodes: {count}/{self.num_nodes}")
        except KeyboardInterrupt:                 
            self.stop_simulation()
            sys.exit(0)

    def stop_simulation(self):
        print("Stopping simulation...")
        for node in self.nodes:
            node.stop()

if __name__ == "__main__":
    def signal_handler(sig, frame):
        sim.stop_simulation()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    sim = Simulation(num_nodes=50, num_nbr=4, prob_infection=1, delay_prob=0.1)
    sim.run()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)