import csv

def gen_header(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Seed", "Total Nodes", "Neighbor %", "Bizantine %", "Protocol", "Time", "Infected Nodes", "Total Messages"])

def store_data(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

if __name__ == "__main__":
    gen_header("sim_data.csv")
        
    