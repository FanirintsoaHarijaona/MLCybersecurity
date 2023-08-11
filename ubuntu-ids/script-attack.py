import pandas as pd
from scapy.all import *
import numpy as np
import traceback

def prepare_data(path): 
    # Load the dataset
    dataset = pd.read_csv(path)
    dataset.columns = dataset.columns.str.lower()
    dataset.drop(columns = "binary label", inplace = True)
    dataset = dataset[(dataset.label == "Diversion") | (dataset.label == "Normal")].reset_index(drop = True)
    dataset["port number"] = dataset["port number"].apply(lambda x: int(x[-1:]))
    
    n = dataset.shape[0]
    np.random.seed(42)
    idx = np.arange(n)
    np.random.shuffle(idx)
    dataset = dataset.iloc[idx]
    dataset.reset_index(drop = True, inplace = True)
    return dataset


def send_attack(path):
    df = prepare_data(path)
    
    for i in range(df.shape[0]):
        try: 
           data_row = df.iloc[i]
           # Create a new Ethernet packet
           packet = Ether()
    
           # Set the source and destination MAC addresses 
           packet.src = "02:42:ac:13:00:02"  # Ubuntu container
           packet.dst = "02:42:ac:13:00:03"  # Switch container
    
           # Create an IP packet
           ip_packet = IP()
    
           # Set the source and destination IP addresses
           ip_packet.src = "172.19.0.2"  # Ubuntu container
           ip_packet.dst = "172.19.0.3"  # Switch container
    
           # Create a TCP packet
           tcp_packet = TCP(flags = "S")
    
           # Set the source and destination ports
           tcp_packet.sport = 9080
           tcp_packet.dport = 80  # HTTP
           tcp_packet.dataofs = 10 
           # Set the packet payload to the data from the dataset
           payload = Raw(load=str(data_row['received bytes']).encode("utf-8"))
    
           # Combine the packets
           packet = packet/ip_packet/tcp_packet/payload
    
           # Send the packet
           sendp(packet)
        except Exception as e:
           print("Error occurred:", e)
           traceback.print_exc()
           return False    
    return True

success = send_attack("Sample_Synthetic_UNR-IDD.csv")
if success:
    print("Script ran successfully!")
else:
    print("Script failed to run.")
    




