import signal
import sys
import time
import random
from node import Node, Message
from store_data import store_data

class Simulation:
    def __init__(self, num_nodes, num_nbr, num_bizantines, protocol="AntiEntropy", T_max=20, seed=42):
        self.num_nodes      = num_nodes
        self.num_nbr        = num_nbr
        self.num_bizantines = num_bizantines
        self.protocol       = protocol
        self.T_max          = T_max
        self.seed           = seed
        random.seed(seed)

        self.nodes = []
        self.update_value = 1

        self.create_nodes()
        self.generate_neighbors()

    def create_nodes(self):
        for i in range(self.num_nodes):
            node = Node(i, i % 10, i // 10, self.protocol, 0.5)
            self.nodes.append(node)
        byz = 0

        # Randomly select nodes to be Byzantine
        while byz < self.num_bizantines:
            node = random.choice(self.nodes)        # escolhidos com seed
            if node.behavior == "Normal":
                self.nodes[i].behavior = "Byzantine"
                self.nodes[i].prob_infection = 0

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

        print("Starting simulation...")
        timer = 0
        active_count = 1

        start_time = time.time()
        self.generate_update()

        try:
            while timer < self.T_max and active_count > 0:
                time.sleep(0.1)
                sus_count = sum([1 for node in self.nodes if node.state == "Susceptible"])
                active_count = sum([1 for node in self.nodes if node.state == "Infected"])
                infected = self.num_nodes - sus_count

                timer = time.time() - start_time
                if int(timer)%2 == 0:
                    print(f"Infected Nodes: {infected}/{self.num_nodes} (active: {active_count})")
        except KeyboardInterrupt:                 
            self.stop_simulation()
            sys.exit(0)

        print(f"Simulation finished in {timer:.2f} seconds")
        msg_num = sum([node.msg_counter for node in self.nodes])
        infected_percent = infected / self.num_nodes * 100

        data = [self.seed, self.num_nodes, self.num_nbr/self.num_nodes*100, self.num_bizantines/self.num_nodes*100, self.protocol, round(timer, 3), infected_percent, msg_num]
        store_data("sim_data.csv", data)
        
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

    for i in range(3): 
        for j in range(30):
            sim = Simulation(num_nodes=50, num_nbr=5, num_bizantines=0, protocol="AntiEntropy", T_max=20)
            sim.run()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)