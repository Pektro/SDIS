import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GUI:
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = ctk.CTk()
        self.root.title("Mesh Network Visualization")

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

        self.draw_mesh()

    def draw_mesh(self):
        G = nx.Graph()
        for node in self.simulation.nodes:
            G.add_node(node.id, pos=(node.x, node.y))
            for neighbor in node.neighbors:
                G.add_edge(node.id, neighbor.id)

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=50, font_size=8)
        self.canvas.draw()

    def run(self):
        self.root.mainloop()

# Example usage
if __name__ == "__main__":
    from simulation import Simulation
    import signal
    import time
    import sys

    def signal_handler(sig, frame):
        sim.stop_simulation()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    sim = Simulation(num_nodes=100, num_nbr=4, prob_infection=1, delay_prob=0.1)
    gui = GUI(sim)
    gui.run()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)