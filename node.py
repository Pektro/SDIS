
class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x  = x
        self.y  = y
        self.state = "Supscetible"      # "Supscetible", "Infected" or "Removed"
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def push(self):
        pass

    def pull(self):
        pass

    def push_pull(self):
        pass

    def gossip_protocol(self):
        pass
        
