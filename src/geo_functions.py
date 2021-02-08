from functools import reduce
import operator
import pandas as pd
import geopandas as gpd
import numpy as np
import requests
from dotenv import load_dotenv
import json
from haversine import haversine
import os

def geocode(address):
    """
    Return coordinates from a given address in longitude, lattitude format
    
    Takes: address
    Returns: coordinates
    """
    coordin = requests.get(f"https://geocode.xyz/{address}?json=1").json()
    try:
        return {
            "type":"Point",
            "coordinates":[float(coordin["longt"]),float(coordin["latt"])]}
    except:
        return coordin

def get_from_dict(dictionary,search_map):
    """
    When given a dictionary, returns an item based on the path defined by the search_map
    
    Takes: dictionary and search map (path)
    Returns: wanted item
    """
    
    return reduce (operator.getitem, search_map, dictionary)

def downl_foursquare(address, foursquare_cat):
    """
    Creates a list with names of places and coordinates for the given 
    address for a starting point and foursquare category
    
    Takes: address, foursquare_cat
    Returns: list with name and coordinates
    """
    
    #obtain coordinates of starting point based on address
    start_coordinates = geocode(address)
    
    #geocode sometimes fails, so include a backup option
    if start_coordinates.get('success') == False:
        start_coordinates = {'type': 'Point', 'coordinates': [37.820100, -122.366760]}
    
    #define search parameters
    tok1 = os.getenv("tok1")
    tok2 = os.getenv("tok2")
    parameters = {"client_id" : tok1,
                  "client_secret" : tok2,
                  "v": "20180323",
                  "ll": f"{start_coordinates.get('coordinates')[1]},{start_coordinates.get('coordinates')[0]}",
                  "categoryId": f"{foursquare_cat}",
                  "radius": 5000,
                  "limit": 100
    }
    
    #call foursquare API
    url = 'https://api.foursquare.com/v2/venues/explore'
    resp = requests.get(url= url, params=parameters)
    fq_data = json.loads(resp.text)
    
    #obtaining the data
    decoding_data = fq_data.get("response")
    #we want the data in groups
    obtain = decoding_data.get("groups")[0]
    #name and coordinates are in items
    wanted_places = obtain.get("items")
    
    #reading the obtained dictionaries with the get_from_dict function
    map_name = ["venue","name"]
    map_lat = ["venue","location","lat"]
    map_long = ["venue","location","lng"]
    #list of dictionaries with the info that we want, each item being a unique place
    list_of_places = []
    for dic in wanted_places:
        items_in_dict = {}
        items_in_dict["name"] = get_from_dict(dic,map_name)
        items_in_dict["latitud"] = get_from_dict(dic,map_lat)
        items_in_dict["longitud"] = get_from_dict(dic,map_long)
        list_of_places.append(items_in_dict)
    
    return list_of_places

def count_near_venues(list_offices, list_venues, radius=1):
    """
    Counts the number of a certain type of venues that are closer than the given radius (in kms)
    
    Takes: list of offices, list of venues, radius (kms)
    Returns: df with number of venues in the given radius
    """
    list_venues_in_distance = []
    for comp in list_offices:
        distance_count = 0
        for ven in list_venues:
            distance = haversine(comp["geojson"]["coordinates"][::-1], 
                      [ven["latitud"], ven["longitud"]])
            if distance <= radius:
                distance_count += 1
        # company id included to differentiate when multiple offices with same name
        list_venues_in_distance.append({"company": f"{comp['name']} {comp['_id']}", "num_venues": f"{distance_count}"})  
    list_venues_df = pd.DataFrame(list_venues_in_distance)
    return list_venues_df

def change_column_name(df, old_column, new_column):
    """
    Changes column name in a given df
    
    Takes: df
    Returns: df with new column name
    """
    df = df.rename({old_column: new_column}, axis = 1, inplace = True)
    return df

def convert_to_int(df, list_columns):
    """
    Converts strings in a pandas column to integers
    
    Takes: dataframe and list of columns
    Returns: dataframe with int data type in chosen columns
    """
    for c in list_columns:
        df[c] = df[c].astype(int)
    return df

def give_points(df, columns_with_weights):
    """
    In a df column with integers, creates new column storing points based on the first column's value
    and weight assigned to column.
    If column value is 0, then points are 0.
    If column value is 1, then points are 70% of weight
    If column value is larger than 1, points are 100% of wight
    
    Takes: df, dict with columns and weights
    Returns: df with points
    """
    
    # iterate over dictionary to create new columns
    for k,v in columns_with_weights.items():
        # create a list with the conditions
        conditions = [(df[k] < 1),
                      (df[k] == 1),
                      (df[k] > 1)
                     ]
        # create a list with values depending on conditions
        values = [0, 0.7 * v, v]
        # create new column
        col_name = f"{k}_points"
        df[col_name] = np.select(conditions, values)
    return df

def conv_list_to_df(list_of_places):
    """
    Creates a pandas dataframe with names of places and coordinates for the given 
    a list of places with names and coordinates
    
    Takes: list of places with names and coordinates
    Returns: pandas dataframe with name and coordinates
    """
    #create a pandas df
    df = pd.DataFrame(list_of_places)
    
    return df