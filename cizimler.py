# -*- coding: utf-8 -*-
"""
Created on Tue May 24 21:31:30 2022

@author: Murat
"""

from  matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point
import geopandas as gpd
from collections import defaultdict

from shapely import speedups
speedups.disable()


df_target_info = pd.read_csv("./sonuclar/results.csv")

#%%

fig1 = plt.figure(figsize=(9,5))
ax=plt.subplot() 

c = {i:np.random.random(3) for i in df_target_info.o_name.unique()}

handles, labels = [],[]

target_prev = defaultdict(str)
for i, row in df_target_info.sort_values(by=["o_name", "o_start_time"]).iterrows():
    x0 = row["o_start_time"]
    x1 = row["meeting_time"]
    
    y0 = row["t_name"]
    y1 = row["t_name"]
    
    o = row["o_name"]
    
    m = ax.plot([x0,x1],[y0,y1], "-o", c=c[o])
    if target_prev[o]:
        ax.plot([x0, x0], [target_prev[o], y1], c=c[o], ls="--")
    
    target_prev[o] = y0
    
    if o not in labels:
        handles.append(m[0])
        labels.append(o)


ax.set_xlabel("Zaman", size=15)
ax.set_ylabel("Hedef", size=15)
ax.grid(c="gray", alpha=0.35, ls="--")

ax.legend(handles, labels)

fig1.tight_layout()


fig1.savefig(r"./sonuclar/drone_timing.png", dpi=300)

#%% PLOT DRONE AND ROUTES

fig2 = plt.figure(figsize=(9,9))
geometry_operator_line = gpd.GeoSeries(df_target_info[['o_start_x', 'o_start_y', 'meeting_x', 'meeting_y']].apply(lambda x:LineString([[x[0], x[1]], [x[2], x[3]]]), axis=1))
geometry_target_line = gpd.GeoSeries(df_target_info[['t_start_x', 't_start_y', 'meeting_x', 'meeting_y']].apply(lambda x:LineString([[x[0], x[1]], [x[2], x[3]]]), axis=1))

geometry_operator_init = gpd.GeoSeries(df_target_info[['o_start_x', 'o_start_y']].apply(lambda x:Point(*x), axis=1))
geometry_target_init = gpd.GeoSeries(df_target_info[['t_start_x', 't_start_y']].apply(lambda x:Point(*x), axis=1))

geometry_meeting_points = gpd.GeoSeries(df_target_info[['meeting_x', 'meeting_y']].apply(lambda x:Point(*x), axis=1))

ax = plt.subplot()
df_target_info[['o_name', 'meeting_x', 'meeting_y']].groupby(by="o_name").last().plot.scatter("meeting_x","meeting_y", color="green", s=100, label="Drone Nihai Nokta", ax=ax)

geometry_target_line.plot(color="blue", linewidth=1, label="Hedef Güzergâhı", ax=ax)
geometry_target_init.plot(color="blue", label="Hedef Hareket Noktası", ax=ax)

geometry_operator_line.plot(color="red", linewidth=1, label="Drone Güzergâhı", ax=ax)
geometry_meeting_points.plot(color="red", label="Hedef Varış Noktası", ax=ax)


for s in df_target_info[['o_name', 'o_start_x', 'o_start_y']].groupby(by="o_name").first().reset_index().values:
    ax.text(*s[1:]+5, s[0])

df_target_info[['o_name', 'o_start_x', 'o_start_y']].groupby(by="o_name").first().plot.scatter("o_start_x","o_start_y", color="k", s=100, label="Drone Başlama Noktası", ax=ax)

ax.set_xlabel("X", size=15)
ax.set_ylabel("Y", size=15)
ax.grid(c="gray", alpha=0.35, ls="--")


handles, labels = plt.gca().get_legend_handles_labels()
order = [5, 0, 3, 2, 4, 1]
plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])

fig2.tight_layout()


fig2.savefig(r"./sonuclar/drone_routes.png", dpi=300)
