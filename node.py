import random
import socket
import threading
import signal
import sys
import time

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.state = "Susceptible"  # "Susceptible", "Infected" or "Removed"
        self.neighbors = []
        self.prob_infection = 1
        self.stop_event = threading.Event()

        ''' Create Socket > Bind > Get Port > Start Listening '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 0))
        self.port = self.socket.getsockname()[1]

        self.listen_thread = threading.Thread(target=self.accept_connection, args=[self.socket])
        self.listen_thread.start()

        print(f"Node {self.id} is listening on port {self.port}")

    def __str__(self):
        nbs = [neighbor.id for neighbor in self.neighbors]
        return f"Node {self.id}: {self.state}\nNeighbors: {nbs}"

    ''''''''''''''''''''''''''''''''''''''
    '''    COMMUNICATION FUNCTIONS     '''
    ''''''''''''''''''''''''''''''''''''''
    def accept_connection(self, socket):
        socket.listen(5)
        while not self.stop_event.is_set():
            try:
                conn, addr = socket.accept()
                threading.Thread(target=self.handle_connection, args=(conn, addr)).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def handle_connection(self, conn, addr):
        while not self.stop_event.is_set():
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Node {self.id} received data: {message}")
            except socket.timeout:
                continue
            except OSError:
                break
        conn.close()

    def send_message(self, message, neighbor):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
                conn.connect(('localhost', neighbor.port))
                conn.send(message.encode())
                print(f"Node {self.id} sent message to Node {neighbor.id}: {message}")
        except Exception as e:
            print(f"Node {self.id} failed to send message to Node {neighbor.id}: {e}")

    def stop(self):
        self.stop_event.set()
        self.socket.close()
        self.listen_thread.join()

    ''''''''''''''''''''''''''''''''
    '''    PROTOCOL FUNCTIONS    '''
    ''''''''''''''''''''''''''''''''

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def push(self):
        # random int for nr of neighbors
        n = random.randint(0, len(self.neighbors)-1)
        neighbor_to_push = self.neighbors[n]

        self.set_timeout()
        pass

    def gossip_protocol(self):
        pass

if __name__ == "__main__":
    nodes = []

    def signal_handler(sig, frame):
        print("Ctrl+C pressed, stopping all nodes...")
        for node in nodes:
            node.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    node1 = Node(1, 0, 0)
    node2 = Node(2, 1, 1)
    nodes.append(node1)
    nodes.append(node2)

    node1.add_neighbor(node2)
    node2.add_neighbor(node1)

    node1.send_message("Hello", node2)
    node2.send_message("Hi", node1)
    node1.send_message("How are you?", node2)
    node2.send_message("I'm fine", node1)

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)