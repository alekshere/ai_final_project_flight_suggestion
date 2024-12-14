#!/usr/bin/env python
# coding: utf-8

import json
import datetime
import pandas as pd
import random
import math
import os

def encode_state(source, flight_destination, base_fare, search_day, search_month, flight_day, flight_month):
    return f"{source}-{flight_destination}-{base_fare:.2f}-{search_day}-{search_month}-{flight_day}-{flight_month}"

def load_qtable(filename="q_table_10000_10.json"):      # using the q-table with 10,000 times and 10% of data coverage
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    else:
        print("wrong qtable name or doesnt exist")

        return None

def find_similar_states(state, q_table, threshold=0.2):
    source, flight_destination, base_fare, search_day, search_month, flight_day, flight_month = state.split("-")
    base_fare = float(base_fare)
    search_day, search_month, flight_day, flight_month = map(int, [search_day, search_month, flight_day, flight_month])

    similar_states = []

    for q_state in q_table.keys():
        # skip states that don't match the expected format
        q_parts = q_state.split("-")

        if len(q_parts) != 7:
            # print("Skiped the invalid state: {q_state}")

            continue

        q_source, q_flight_destination, q_fare, q_s_day, q_s_month, q_f_day, q_f_month = q_parts
        q_fare = float(q_fare)
        q_s_day, q_s_month, q_f_day, q_f_month = map(int, [q_s_day, q_s_month, q_f_day, q_f_month])

        # check for similar airports to the one provided
        if q_source == source and q_flight_destination == flight_destination:
            # Check for closeness in the base fare and dates
            fare_diff = abs(base_fare - q_fare)
            date_diff = abs(search_day - q_s_day) + abs(search_month - q_s_month)

            # if differences in threshold then consider similar
            if fare_diff <= base_fare * threshold and date_diff <= 5:
                similar_states.append(q_state)

    return similar_states
    
def estimate_action_from_similar_states(similar_states, q_table):
    
    if not similar_states:

        return "Wait", 0  # tell/inform user to wait if the ticket are not worth buyting

    action_sums = {"Buy": 0, "Wait": 0}

    for state in similar_states:
        for action, q_value in q_table[state].items():
            action_sums[action] = action_sums[action] +  q_value

    # return the action with the highest Q-value (which means it's the best possible action)
    best_action = max(action_sums, key = action_sums.get)

    return best_action, action_sums[best_action]

def get_user_decision(q_table):
    print("Provide flight details below:")

    source = input("sourceing airport (e.g., JFK): ").strip()
    flight_destination = input("destination airport (e.g., SFO): ").strip()

    try:
        # The user's input is asked for here
        base_fare = float(input("Enter estimated base fare (xxx.xx): "))
        search_day = int(input("Search day (1-31): ")) 
        search_month = int(input("Search month (1-12): "))
        flight_day = int(input("Flight day (1-31): "))
        flight_month = int(input("Flight month (1-12): "))

    except ValueError:

        print("Enter numbers for base fare, day, and month.")

        return

    # sets the current state 
    state = encode_state(source, flight_destination, base_fare, search_day, search_month, flight_day, flight_month)

    # checks Q-table given user's state
    if state in q_table:
        action = max(q_table[state], key=q_table[state].get)

        print("You should " + {action.lower()} + " the ticket.")
    else:
        similar_states = find_similar_states(state, q_table)
        best_action, confidence = estimate_action_from_similar_states(similar_states, q_table)

        print(f"Decision (estimated): You should {best_action.lower()} the ticket (confidence: {confidence:.2f}).")

if name == "main":
    # the given Q table can be trained more,
    # in the load_qtable function we can update 
    # what file the qtable accesses and provide a 
    # more trained one

    q_table = load_qtable()

    if q_table:
        get_user_decision(q_table)