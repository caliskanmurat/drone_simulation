# -*- coding: utf-8 -*-
"""
Created on Mon May  9 20:39:31 2022

@author: Murat
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point

#%%

target_parameters = pd.read_excel(r".\veriler\data.xlsx", sheet_name="RandomTarget", header=None, index_col=0).iloc[:9,0].squeeze().to_dict()
drone_parameters = pd.read_excel(r".\veriler\data.xlsx", sheet_name="RandomDrone", header=None, index_col=0).iloc[:7,0].squeeze().to_dict()

NUMBER_OF_TARGETS = target_parameters["number_of_targets"]
TARGET_SPEED_MIN = target_parameters["speed_min"]
TARGET_SPEED_MAX = target_parameters["speed_max"]
TARGET_X_COOR_MIN = target_parameters["x_coor_min"]
TARGET_X_COOR_MAX = target_parameters["x_coor_max"]
TARGET_Y_COOR_MIN = target_parameters["y_coor_min"]
TARGET_Y_COOR_MAX = target_parameters["y_coor_max"]
TARGET_ANGLE_MIN = target_parameters["angle_min"]
TARGET_ANGLE_MAX = target_parameters["angle_max"]


NUMBER_OF_DRONES = drone_parameters["number_of_drones"]
DRONE_SPEED_MIN = drone_parameters["speed_min"]
DRONE_SPEED_MAX = drone_parameters["speed_max"]
DRONE_X_COOR_MIN = drone_parameters["x_coor_min"]
DRONE_X_COOR_MAX = drone_parameters["x_coor_max"]
DRONE_Y_COOR_MIN = drone_parameters["y_coor_min"]
DRONE_Y_COOR_MAX = drone_parameters["y_coor_max"]

OUTPUT_FOLDER_PATH = "./sonuclar"
NAME_OF_OUTPUT_FILE = "random_data"

#%%

def create_target(number_of_points):
    minx = TARGET_X_COOR_MIN
    miny = TARGET_Y_COOR_MIN
    maxx = TARGET_X_COOR_MAX
    maxy = TARGET_Y_COOR_MAX
    
    x = np.round(np.random.uniform(minx, maxx + 0.01, number_of_points), 3)
    y = np.round(np.random.uniform(miny, maxy + 0.01, number_of_points), 3)
    
    names = [f"Target {i}" for i in range(1, number_of_points+1)]
    speeds = np.random.randint(TARGET_SPEED_MIN, TARGET_SPEED_MAX+1, number_of_points)
    angles = np.random.randint(TARGET_ANGLE_MIN, TARGET_ANGLE_MAX+1, points.shape[0])%360)

    df_targets = pd.DataFrame({
        "Name" : names,
        "Speed" : speeds,
        "X" : x,
        "Y" : y,
        "Angle" : angles})
    
    return df_targets


#%%

def create_drone(number_of_points):
    minx = DRONE_X_COOR_MIN
    miny = DRONE_Y_COOR_MIN
    maxx = DRONE_X_COOR_MAX
    maxy = DRONE_Y_COOR_MAX
    
    x = np.round(np.random.uniform(minx, maxx + 0.01, number_of_points), 3)
    y = np.round(np.random.uniform(miny, maxy + 0.01, number_of_points), 3)
    
    names = [f"Drone_{i}" for i in range(1, number_of_points+1)]
    speeds = np.random.randint(DRONE_SPEED_MIN, DRONE_SPEED_MAX+1, number_of_points)
    
    df_operator = gpd.GeoDataFrame({
        "Name" : names,
        "Speed" : speeds,
        "X" : x,
        "Y" : y
        })
    
    return df_operator

#%%
        
df_operator = create_drone(NUMBER_OF_DRONES)
df_target = create_target(NUMBER_OF_TARGETS)

with pd.ExcelWriter(f"{OUTPUT_FOLDER_PATH}/{NAME_OF_OUTPUT_FILE}.xlsx") as ex:
    df_operator.to_excel(excel_writer=ex, sheet_name="Operator", index=False)
    df_target.to_excel(excel_writer=ex, sheet_name="Target", index=False)

