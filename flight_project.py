# source myenv/bin/activate for the environment (mac comm)

import json
import datetime
import pandas as pd
import random
import math
import os

alpha = 0.1  
gamma = 0.9 
epsilon = 0.2 
max_times = 10000

q_table = {}

actions = ["Buy", "Wait"]

# encode state function --> for uniqueness to be formatted correctly
def encode_state(source, destination, base_fare, search_day, search_month, flight_day, flight_month):
    return f"{source}-{destination}-{base_fare:.2f}-{search_day}-{search_month}-{flight_day}-{flight_month}"

# qtable initialized 
def init_qtable(state):
    if state not in q_table:
        q_table[state] = {action: 0.0 for action in actions}

# save qtable to a file (so it won't have to be trained every time)
def save_qtable(filename="q_table_10000_100.json"):
    with open(filename, "w") as file:
        json.dump(q_table, file)

# load qtable from a file
def load_qtable(filename="q_table_10000_100.json"):
    global q_table  # needed to be sure it gets updated
    if os.path.exists(filename):
        with open(filename, "r") as file:
            q_table = json.load(file)
    else:
        print(f"No qtable file found. Starting fresh.")

data = pd.read_csv("extracted_data.csv")  # our cleaned data

# sample 1% of the dataset to reduce processing load
data = data.sample(frac=0.1)  # sample 10% of the dataset (82,000,000 * 0.10 = 8,200,000 rows)

# simulates price changes (using random because it's hard to grab from our csv - time issue.. would have liked to use from the real world data)
def simulate_price_change(action, base_fare):
    if action == "Buy":
        # +10 buying was good (we think), -10 if missed opportunity to buy at cheaper price, 0 nothing
        return base_fare, random.choice([10, -10, 0])
    else:
        price_change = random.choice([-20, 0, 20])
        
        if price_change > 0:
            reward = -10  
        elif price_change < 0:
            reward = 10   
        else:
            reward = 0   

        return base_fare + price_change, reward

# trains the agent
def training():
    for episode in range(max_times):
        row = data.sample(1).iloc[0]
        source = row['startingAirport']
        destination = row['destinationAirport']
        base_fare = row['baseFare']
        search_day = row['searchDay']
        search_month = row['searchMonth']
        flight_day = row['flightDay']
        flight_month = row['flightMonth']

        # encode/initialize the state
        state = encode_state(source, destination, base_fare, search_day, search_month, flight_day, flight_month)
        init_qtable(state)

        # training loop
        for step in range(10):
            action = random.choice(actions) 
                
            # simulate environment response --> always random
            base_fare, reward = simulate_price_change(action, base_fare) 

            # update search day and month if waiting
            if action == "Wait":
                search_day += 1
                if search_day > 28:  
                    search_day = 1
                    search_month += 1
                    if search_month > 12:
                        search_month = 1

            # new state
            new_state = encode_state(source, destination, base_fare, search_day, search_month, flight_day, flight_month)
            init_qtable(new_state)

            # update qtable
            for s in q_table.keys():
                for a in q_table[s].keys():
                    q_table[s][a] += alpha * (
                        reward + gamma * max(q_table[new_state].values()) - q_table[s][a]
                    )
            
            state = new_state

        # save the Q-table every 1000 episodes
        if episode % 1000 == 0:
            save_qtable()

if __name__ == "__main__":
    # load pretrained model if available
    load_qtable() 
    
    training()   
    
    save_qtable()
