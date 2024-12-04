import random
import socket
import threading
import signal
import sys
import time
import json

class Message:
    def __init__(self, value, content, msg_type="UPDATE"):
        self.value   = value        
        self.content = content
        self.type    = msg_type    # "UPDATE" or "REPLY" 

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def update(self, msg):
        self.value   = msg.value
        self.content = msg.content

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Message(data['value'], data['content'])


class Node:
    def __init__(self, id, x, y, protocol, timeout):
        self.id = id
        self.x = x
        self.y = y
        self.state = "Susceptible"  # "Susceptible", "Infected" or "Removed"
        self.protocol = protocol
        self.timeout = timeout
        self.neighbors = []
        self.prob_infection = 1

        self.message = Message(0, "Default message")

        self.stop_event = threading.Event()

        ''' Create Socket > Bind > Get Port > Start Listening '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 0))
        self.port = self.socket.getsockname()[1]

        self.listen_thread = threading.Thread(target=self.accept_connection, args=[self.socket])
        self.listen_thread.start()

        print(f"Node {self.id} is listening on port {self.port}")

        ''' Create'''
        if protocol == "AntiEntropy":
            self.protocol_thread = threading.Thread(target=self.run_AntiEntropyProtocol)
        else:
            self.protocol_thread = threading.Thread(target=self.run_DisseminationProtocol)

        self.protocol_thread.start()

    def __str__(self):
        nbs = [neighbor.id for neighbor in self.neighbors]
        return f"Node {self.id}: {self.state}\nNeighbors: {nbs}"

    ''''''''''''''''''''''''''''''''''''''
    '''    COMMUNICATION FUNCTIONS     '''
    ''''''''''''''''''''''''''''''''''''''
    def accept_connection(self, sock):
        sock.listen(5)
        while not self.stop_event.is_set():
            try:
                conn, addr = sock.accept()
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
                rcv_message = Message.from_json(message)
                #print(f"Node {self.id} received data: {message}")

                if self.protocol == "AntiEntropy":
                    self.rcv_AntiEntropy(rcv_message)
                else:
                    self.rcv_Dissemination(rcv_message)
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
                #print(f"Node {self.id} sent message to Node {neighbor.id}: {message}")
        except Exception as e:
            pass

    def stop(self):
        self.stop_event.set()
        self.socket.close()
        self.protocol_thread.join()
        self.listen_thread.join()

    ''''''''''''''''''''''''''''''''
    '''    PROTOCOL FUNCTIONS    '''
    ''''''''''''''''''''''''''''''''

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def run_AntiEntropyProtocol(self):
        while not self.stop_event.is_set():
            try:
                time.sleep(self.timeout)
                self.push_message()
            except OSError:
                break

    def rcv_AntiEntropy(self, rcv_msg):
        if rcv_msg.value > self.message.value:
            self.state = "Infected"
            self.message.update(rcv_msg)

    def run_DisseminationProtocol(self):
        while not self.stop_event.is_set():
            try:    
                time.sleep(self.timeout)
                if random.uniform(0, 1) < self.prob_infection:
                    self.push_message()
                else:
                    self.state = "Removed"
            except OSError:
                break

    def rcv_Dissemination(self, rcv_msg, neighbor):
        if rcv_msg.msg_type == "UPDATE":
            if rcv_msg.value > self.message.value:
                self.send_message(Message(self.message.value, "REPLY").to_json(), neighbor)     # Reply with previous message value
                self.state = "Infected"
                self.message.update(rcv_msg)

        elif rcv_msg.msg_type == "REPLY":
            if rcv_msg.value == self.message.value:
                self.prob_infection -= 0.25

    def push_message(self):
        if not self.neighbors or self.state != "Infected":
            return
        neighbor = random.choice(self.neighbors)
        self.send_message(self.message.to_json(), neighbor)

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

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)