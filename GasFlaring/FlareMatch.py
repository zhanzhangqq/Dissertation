# Import necessary libraries
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import os
import matplotlib.pyplot as plt
import warnings
import random
import multiprocessing as mp
import datetime

# Change directory accordingly
root_path = '/Geodata_Backup/'
fielddata_path = root_path + 'fields_withflare/'
flaredata_path = root_path + 'flaring_2020/'
result_path = root_path + 'flaring_inside_outside/'

# csv to geodf
def cvt_point_to_geodf(df, latname='Latitude', lonname='Longitude'):
    df['coords'] = list(zip(df[lonname], df[latname]))
    df['coords'] = df['coords'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='coords')
    return gdf

# load flare
def load_Flare(flaredata_path, country):
    flare = pd.read_csv(flaredata_path + "csv/" + country + ".csv")
    flare = cvt_point_to_geodf(flare, lonname='Longitude', latname='Latitude')
    flare = flare.rename(columns={'Avg. temp., K': 'Avg_temp_K'})
    flare = flare.rename(columns={'Clear Obs.': 'Clear_Obs'})
    flare = flare.rename(columns={'BCM 2020': 'BCM_2020'})
    flare = flare.set_crs(epsg=4326)

    return flare

# load field
def load_Field(fielddata_path, country):
    field = gpd.GeoDataFrame.from_file(fielddata_path + country + ".shp")
    field = field.set_crs(epsg=4326, allow_override=True)
    return field

# Join points inside to polygons
def join_Inside(flaredata_path, fielddata_path, country):
    flare = load_Flare(flaredata_path, country)
    field = load_Field(fielddata_path, country)
    flare['flare_count'] = 1
    field_in = gpd.tools.sjoin(field, flare, op='intersects', how='left')

    field_in = field_in.drop(columns=['index_right', 'Country_right', 'ISO Code', 'Catalog ID', 'ID 2020', 'Latitude', 'Longitude', 'Avg_temp_K', 'Ellipticity', 'Detection frequency 2020', 'Clear_Obs', 'Type'])

    field_in_groupby = field_in.groupby(['Number']).agg({'Country_left': 'first', 'Product_Ty': 'first', 'Number': 'first', 'N_Fldname': 'first', 'SUM_OIL_PR': 'first', 'SUM_GOR': 'first', 'BCM_2017': 'first', 'BCM_2018': 'first', 'BCM_2012': 'first', 'BCM_2013': 'first', 'BCM_2014': 'first', 'BCM_2015': 'first', 'BCM_2016': 'first', 'BCM_2020': np.sum, 'flare_count': np.sum})
    field_in_groupby = field_in_groupby.reset_index(level=0, drop=True).reset_index(drop=True)
    field_in_groupby = gpd.GeoDataFrame(field_in_groupby, crs="EPSG:4326", geometry=field_in_groupby["geometry"])
    field_in_groupby = field_in_groupby.rename(columns={'Country_left': 'Country'})

    return field_in_groupby

# Generate field buffer for outside flaring
def buffer_Field(fielddata_path, country, dist):
    field = load_Field(fielddata_path, country)
    field_buffer = field.to_crs("EPSG:3857")
    field_buffer.geometry = field_buffer.geometry.buffer(dist)
    field_buffer = field_buffer.to_crs("EPSG:4326")

    return field_buffer

# Remove flares within fields
def remove_Flarewithin(flaredata_path, fielddata_path, country):
    flare = load_Flare(flaredata_path, country)
    field = load_Field(fielddata_path, country)
    flare_out = gpd.tools.sjoin(field, flare, op='intersects', how='right')
    flare_out = flare_out[flare_out['index_left'].isna()]
    flare_out = flare_out.drop(columns=['index_left', 'Country_left', 'Product_Ty', 'Number', 'N_Fldname', 'SUM_OIL_PR', 'SUM_GOR', 'BCM_2017', 'BCM_2018', 'BCM_2012', 'BCM_2013', 'BCM_2014', 'BCM_2015', 'BCM_2016', 'BCM_2019'])
    flare_out = gpd.GeoDataFrame(flare_out, crs="EPSG:4326", geometry=flare_out["coords"])
    return flare_out

# Join points outside to polygons
def join_Outside(flaredata_path, fielddata_path, country, dist):
    field_buffer = buffer_Field(fielddata_path, country, dist)
    flare_out = remove_Flarewithin(flaredata_path, fielddata_path, country)
    flare_out['flare_count'] = 1
    field_out = gpd.tools.sjoin(field_buffer, flare_out, op='intersects', how='left')

    field_out = field_out.drop(columns=['index_right', 'Country_right', 'ISO Code', 'Catalog ID', 'ID 2020', 'Latitude', 'Longitude', 'Avg_temp_K', 'Ellipticity', 'Detection frequency 2020', 'Clear_Obs', 'Type'])

    field_out_groupby = field_out.groupby(['Number']).agg({'Country': 'first', 'Product_Ty': 'first', 'Number': 'first', 'N_Fldname': 'first', 'SUM_OIL_PR': 'first', 'SUM_GOR': 'first', 'BCM_2017': 'first', 'BCM_2018': 'first', 'BCM_2012': 'first', 'BCM_2013': 'first', 'BCM_2014': 'first', 'BCM_2015': 'first', 'BCM_2016': 'first', 'BCM_2020': np.sum, 'flare_count': np.sum})
    field_out_groupby = field_out_groupby.reset_index(level=0, drop=True).reset_index(drop=True)
    field_out_groupby = gpd.GeoDataFrame(field_out_groupby, crs="EPSG:4326", geometry=field_out_groupby["geometry"])
    return field_out_groupby

def main():
    
    # Set the country
    country = 'your_country'  # Replace with the actual country

    # Join points inside to polygons
    field_in_groupby = join_Inside(flaredata_path, fielddata_path, country)
    print("Joined points inside to polygons:")
    print(field_in_groupby.head())

    # Generate field buffer for outside flaring
    buffer_distance = 1000  # Replace with the desired buffer distance
    field_buffer = buffer_Field(fielddata_path, country, buffer_distance)
    print("Generated field buffer for outside flaring:")
    print(field_buffer.head())

    # Remove flares within fields
    flare_out = remove_Flarewithin(flaredata_path, fielddata_path, country)
    print("Removed flares within fields:")
    print(flare_out.head())

    # Join points outside to polygons
    field_out_groupby = join_Outside(flaredata_path, fielddata_path, country, buffer_distance)
    print("Joined points outside to polygons:")
    print(field_out_groupby.head())

if __name__ == "__main__":
    main()

