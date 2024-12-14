import json
import datetime
import pandas as pd
import random
import math
import os

# open and load the dataset in chunks of 10k
data_chunks = pd.read_csv('flight_prices.csv', chunksize=10000)  

extracted_data = []

for i, chunk in enumerate(data_chunks):
    # fetch and copy over the needed columns
    required_columns = ['searchDate', 'flightDate', 'startingAirport', 'destinationAirport', 'baseFare']
    extracted_chunk = chunk[required_columns].copy() 

    # change/convert search and flight date to real time format
    extracted_chunk['searchDate'] = pd.to_datetime(extracted_chunk['searchDate'])
    extracted_chunk['flightDate'] = pd.to_datetime(extracted_chunk['flightDate'])

    # get the day and month from the search and flight dates
    extracted_chunk.loc[:, 'searchDay'] = extracted_chunk['searchDate'].dt.day
    extracted_chunk.loc[:, 'searchMonth'] = extracted_chunk['searchDate'].dt.month
    extracted_chunk.loc[:, 'flightDay'] = extracted_chunk['flightDate'].dt.day
    extracted_chunk.loc[:, 'flightMonth'] = extracted_chunk['flightDate'].dt.month

    # rmeove the original search and flight date columns
    extracted_chunk = extracted_chunk.drop(columns=['searchDate', 'flightDate'])

    # save/append the extracted data
    extracted_data.append(extracted_chunk)

    # print out a progress every chunk (10k rows)
    # if (i + 1) * 10000 <= len(chunk):
    #     print(f'Went over { (i + 1) * 10000 } rows')

# stich/connect all the chunks of data together
final_extracted_data_chunks = pd.concat(extracted_data, ignore_index=True)


# save the data to a new csv file
final_extracted_data_chunks.to_csv('extracted_data.csv', index=False)
