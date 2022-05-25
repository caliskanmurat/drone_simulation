# -*- coding: utf-8 -*-
"""
Created on Mon May  9 20:39:31 2022

@author: Murat
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import os


path = "./veriler/sim_boundary.gpkg"

drones = gpd.read_file(path, layer="drone_start")
targets = gpd.read_file(path, layer="targets")

target_parameters = pd.read_excel(r".\veriler\data.xlsx", sheet_name="RandomTarget", header=None, index_col=0).iloc[:9,0].squeeze().to_dict()
drone_parameters = pd.read_excel(r".\veriler\data.xlsx", sheet_name="RandomDrone", header=None, index_col=0).iloc[:7,0].squeeze().to_dict()


NUMBER_OF_TARGETS = target_parameters["number_of_targets"] if target_parameters["number_of_targets"] < 100 else 100
TARGET_SPEED_MIN = target_parameters["speed_min"]
TARGET_SPEED_MAX = target_parameters["speed_max"]
TARGET_ANGLE_MIN = target_parameters["angle_min"]
TARGET_ANGLE_MAX = target_parameters["angle_max"]


NUMBER_OF_DRONES = drone_parameters["number_of_drones"]
DRONE_SPEED_MIN = drone_parameters["speed_min"]
DRONE_SPEED_MAX = drone_parameters["speed_max"]


OUTPUT_FOLDER_PATH = "./sonuclar"
NAME_OF_OUTPUT_FILE = "random_data_beytepe"

#%%

def create_target(number):
    points = targets.sample(number).rename(columns={"name":"Name"})
    points.insert(1, "Speed", np.random.randint(TARGET_SPEED_MIN, TARGET_SPEED_MAX+1, points.shape[0]))
    points.insert(2, "X", points.geometry.x)
    points.insert(3, "Y", points.geometry.y)
    points.insert(4, "Angle", np.random.randint(TARGET_ANGLE_MIN, TARGET_ANGLE_MAX+1, points.shape[0])%360)

    return points.drop(columns=["geometry"])


#%%

def create_drone(number):
    point_x = drones.geometry.x
    point_y = drones.geometry.y
    
    names = [f"Drone_{i}" for i in range(1, number+1)]
    speeds = np.random.randint(DRONE_SPEED_MIN, DRONE_SPEED_MAX+1, number)
    x = np.full(number, point_x)
    y = np.full(number, point_y)
    
    df_operator = pd.DataFrame({
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

