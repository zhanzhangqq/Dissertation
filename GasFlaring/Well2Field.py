# Import necessary libraries
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import contextily as cx
from shapely.ops import transform
from shapely.prepared import prep
import pyproj
from functools import partial
import rtree
import numpy as np
import os
import matplotlib.pyplot as plt
import warnings
import random
import multiprocessing as mp
import dill
import progressbar
import datetime

# Change directory accordingly
root_path = '/Geodata_Backup/'
welldata_path = root_path + 'well2field_2023/csv/'
result_path = root_path + 'well2field_2023/field_output/'

# csv to geodf
def cvt_point_to_geodf(df, lonname, latname):
    df['coords'] = list(zip(df[lonname], df[latname]))
    df['coords'] = df['coords'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='coords')
    return gdf

# load well
def load_Well(welldata_path, country):
    well = pd.read_csv(welldata_path + country + "_well.csv")
    well = well[['id_well_pk', 'country_name', 'well_associated_field', 'well_th_long_decimal_wgs84', 'well_th_lat_decimal_wgs84']]  # optional
    well = cvt_point_to_geodf(well, 'well_th_long_decimal_wgs84', 'well_th_lat_decimal_wgs84')
    well = well.set_crs(epsg=4326)
    return well

# Generate well buffer for wells
def buffer_Well(well, dist):
    well_buffer = well.to_crs("EPSG:3857")
    well_buffer.geometry = well_buffer.geometry.buffer(dist)
    well_buffer = well_buffer.to_crs("EPSG:4326")
    return well_buffer

# Dissolve well buffers with the same field name into one field
def dissolve_buffer(well_buffer):
    field = well_buffer.dissolve(by='well_associated_field', aggfunc='first')
    return field


def main():
    country = "your_country"  # Replace with the actual country
    well = load_Well(welldata_path, country)

    buffer_distance = 1000  # Replace with the desired buffer distance
    well_buffer = buffer_Well(well, buffer_distance)

    field = dissolve_buffer(well_buffer)
    return field
  
if __name__ == "__main__":
    main()
