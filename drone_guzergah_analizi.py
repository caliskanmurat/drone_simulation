# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:12:16 2022

@author: caliskan.murat
"""

import math
import numpy as np
import pandas as pd
from collections import deque
from collections import defaultdict
from typing import Iterable

#%%

RETURN_COORS = (350, 500)

#%%
def generateOperator(number_of_operators:int ,speed_range:Iterable, x_coor_range:Iterable, y_coor_range:Iterable):
    speed = np.random.randint(int(speed_range[0]), int(speed_range[1]), number_of_operators)
    x_coor = np.random.randint(int(x_coor_range[0]), int(x_coor_range[1]), number_of_operators)
    y_coor = np.random.randint(int(y_coor_range[0]), int(y_coor_range[1]), number_of_operators)
    
    operators = pd.DataFrame({"Speed":speed, "X":x_coor, "Y":y_coor})
    operators.insert(0, "Name", "Drone " + (operators.index+1).astype(str))
    
    return operators

def generateTarget(number_of_targets:int ,speed_range:Iterable, x_coor_range:Iterable, y_coor_range:Iterable, angle_range:Iterable):
    speed = np.random.randint(int(speed_range[0]), int(speed_range[1]), number_of_targets)
    x_coor = np.random.randint(int(x_coor_range[0]), int(x_coor_range[1]), number_of_targets)
    y_coor = np.random.randint(int(y_coor_range[0]), int(y_coor_range[1]), number_of_targets)
    angle = np.random.randint(int(angle_range[0]), int(angle_range[1]), number_of_targets)
    
    targets = pd.DataFrame({"Speed":speed, "X":x_coor, "Y":y_coor, "Angle":angle})
    targets.insert(0, "Name", "Target " + (targets.index+1).astype(str))
    
    return targets

class Calculator():
    def angle(self, p1,p2, degree=False):
        x1,y1 = p1
        x2,y2 = p2
        dx = x2-x1
        dy = y2-y1
        
        if dy == 0:
            if dx > 0:
                alpha = math.pi/2
            elif dx < 0:
                alpha = 3 * (math.pi/2)
            else:
                alpha = 0
        else:
            alpha = math.atan(dx/dy)
            if dy < 0:
                alpha += math.pi
            else:
                alpha += (2*math.pi)
                
        alpha = alpha%(2*math.pi)
        return (math.degrees(alpha) + 360)%360 if degree else alpha

    def coors(self, p0, dist, angle, angle_unit = "radian"):
        x0,y0 = p0
        if angle_unit == "degree":
            angle_radian = angle * (math.pi/180)
        
        elif angle_unit == "grad":
            angle_radian = angle * (math.pi/200)
        
        else:
            angle_radian = angle * 1
            
        px = x0 + math.sin(angle_radian) * dist
        py = y0 + math.cos(angle_radian) * dist
        
        return px, py
    
    def dist(self, p1x, p1y ,p2x, p2y):
        return math.sqrt((p1x - p2x)**2 + (p1y - p2y)**2)

class Operator(Calculator):
    def __init__(self, name, pos_x, pos_y, speed):
        self.NAME = name
        self.POS_X = pos_x
        self.POS_Y = pos_y
        self.SPEED = speed
        self.DELAY_TIME = 0
    
    def __str__(self):
        return "Operator_" + str(self.NAME)    
    
    def __repr__(self):
        return "Operator_" + str(self.NAME)
    
    def moveToTarget(self, Target, delay=0):
        self.TARGET_NAME = Target.NAME
        self.TARGET_X_ = Target.POS_X
        self.TARGET_Y_ = Target.POS_Y
        self.TARGET_SPEED = Target.SPEED
        self.TARGET_ANGLE = Target.ANGLE
        self.ANGLE_TYPE = Target.ANGLE_TYPE
        self.DELAY_TIME = delay
        
        self.TARGET_X, self.TARGET_Y = self.coors((self.TARGET_X_, self.TARGET_Y_), self.DELAY_TIME*self.TARGET_SPEED, self.TARGET_ANGLE, self.ANGLE_TYPE)
        
        if self.SPEED <= self.TARGET_SPEED:
            return None,None, None
        
        if self.ANGLE_TYPE == "radian":
            self.beta = self.TARGET_ANGLE       
        elif self.ANGLE_TYPE == "degree":
            self.beta = self.TARGET_ANGLE * (math.pi/180)         
        else:
            self.beta = self.TARGET_ANGLE * (math.pi/200)
        
        if self.angle((self.TARGET_X, self.TARGET_Y), (self.POS_X, self.POS_Y)) == self.beta:
            self.speed_ratio = self.SPEED / (self.SPEED + self.TARGET_SPEED)
            
            self.b = self.dist(self.POS_X, self.POS_Y, self.TARGET_X, self.TARGET_Y) * self.speed_ratio
            self.angle_ac = self.angle((self.POS_X, self.POS_Y), (self.TARGET_X, self.TARGET_Y))            
            self.ot_last_x, self.ot_last_y = self.coors((self.POS_X, self.POS_Y), self.b, self.angle_ac)
            
            self.distToTarget = self.dist(self.POS_X, self.POS_Y, self.ot_last_x, self.ot_last_y)
            self.delay_time = (self.distToTarget / self.SPEED)
            
            return (self.ot_last_x, self.ot_last_y), self.delay_time, (math.degrees(self.angle_ac)+360)%360
        
        if self.angle((self.POS_X, self.POS_Y), (self.TARGET_X, self.TARGET_Y)) == self.beta:
            self.speed_ratio = self.SPEED / (self.SPEED - self.TARGET_SPEED)
            
            self.b = self.dist(self.POS_X, self.POS_Y, self.TARGET_X, self.TARGET_Y) * self.speed_ratio
            self.angle_ac = self.angle((self.POS_X, self.POS_Y), (self.TARGET_X, self.TARGET_Y))            
            self.ot_last_x, self.ot_last_y = self.coors((self.POS_X, self.POS_Y), self.b, self.angle_ac)
            
            self.distToTarget = self.dist(self.POS_X, self.POS_Y, self.ot_last_x, self.ot_last_y)
            self.delay_time = (self.distToTarget / self.SPEED)
            
            return (self.ot_last_x, self.ot_last_y), self.delay_time, (math.degrees(self.angle_ac)+360)%360
        
        self.alpha = self.angle((self.TARGET_X, self.TARGET_Y), (self.POS_X, self.POS_Y)) - self.beta
        self.gama = math.asin(math.sin(self.alpha) * (self.TARGET_SPEED/self.SPEED)) #sinus theorem
        self.teta = math.pi - (self.alpha + self.gama)
        
        self.c = math.sqrt((self.TARGET_X - self.POS_X)**2 + (self.TARGET_Y - self.POS_Y)**2)
        self.a = (math.sin(self.gama) * self.c) / math.sin(self.teta) #sinus theorem
        self.b = (math.sin(self.alpha) * self.c) / math.sin(self.teta) #sinus theorem
        
        self.angle_ac = self.angle((self.POS_X, self.POS_Y), (self.TARGET_X, self.TARGET_Y)) + self.gama
        
        self.ot_last_x, self.ot_last_y = self.coors((self.POS_X, self.POS_Y), self.b, self.angle_ac)
        
        self.distToTarget = self.dist(self.POS_X, self.POS_Y, self.ot_last_x, self.ot_last_y)
        self.delay_time = (self.distToTarget / self.SPEED)
        
        self.POS_X_before = self.POS_X
        self.POS_Y_before = self.POS_Y
        
        self.POS_X = self.ot_last_x
        self.POS_Y = self.ot_last_y
        
        return (self.ot_last_x, self.ot_last_y), self.delay_time, (math.degrees(self.angle_ac)+360)%360
    
class Target(Calculator):
    def __init__(self, name, pos_x, pos_y, speed, angle, angle_type="degree"):
        self.NAME = name
        self.POS_X = pos_x 
        self.POS_Y = pos_y
        self.SPEED = speed
        self.ANGLE = angle
        self.ANGLE_TYPE = angle_type
        
    def getReturnInfo(self, start_coor, dest_coor, current_time):        
        distance = self.dist(start_coor[0], start_coor[1], dest_coor[0], dest_coor[1])
        duration = 0 if self.SPEED == 0 else distance / self.SPEED
        angle = self.angle((start_coor[0], start_coor[1]), (dest_coor[0], dest_coor[1]), degree=True)
        
        return duration, angle
    
    def __str__(self):
        return "Target_" + str(self.NAME)    
    
    def __repr__(self):
        return "Target_" + str(self.NAME) 
        
calc=Calculator()

#%% READ DRONE AND TARGET INFO

path = "./veriler/data.xlsx"

operator_sheetname = "Operator"
target_sheetname = "Target"

df_operator = pd.read_excel(path, operator_sheetname).iloc[:,:4].dropna()
df_targets = pd.read_excel(path, target_sheetname).iloc[:,:5].dropna()

#%% CREATE RESULTS

target_deque = deque() 
operator_dict = defaultdict(list)
target_info = []

for i,row in df_operator.iterrows():
    op_name, op_speed, op_x, op_y = row
    o = Operator(name=op_name, pos_x=op_x, pos_y=op_y, speed=op_speed)
    operator_dict[op_name] = o

for i,row in df_targets.iterrows():
    t_name, t_speed, t_pos_x, t_pos_y, t_angle = row        
    t = Target(name=t_name, pos_x=t_pos_x, pos_y=t_pos_y, speed=t_speed, angle=t_angle)
    target_deque.appendleft((t_name, t))

availability = {o.NAME:o.DELAY_TIME for o in operator_dict.values()}    

delay = defaultdict(float)
is_break = True
cnt_target = 0
max_iter = len(operator_dict) * len(target_deque)
t=0

while is_break:
    t+=1
    if cnt_target > max_iter:
        break
    
    for o_name, end_time in sorted(availability.items(), key=lambda x:x[0]):
        if end_time <= t:
            operator = operator_dict[o_name]
            try:
                t_name, target = target_deque.pop()
                target_coor, d, a = operator.moveToTarget(target, delay=delay[o_name])
                if target_coor:
                    start = delay[o_name]
                    delay[o_name] += d
                    
                    availability[o_name] = delay[o_name]
                    
                    target_return_duration, target_return_angle = target.getReturnInfo(target_coor, RETURN_COORS, delay[o_name])
                    target_info.append([o_name, operator.POS_X_before, operator.POS_Y_before, a, operator.SPEED, start, d, t_name,  target.POS_X, target.POS_Y, target.ANGLE, target.SPEED, delay[o_name]+target_return_duration, target_return_duration, target_return_angle, *RETURN_COORS, delay[o_name], *target_coor])                
                    
                else:
                    target_deque.appendleft((t_name, target))  
                
                cnt_target += 1
                
            except Exception as e:
                is_break = False
                break

df_target_info = pd.DataFrame(target_info, columns=["o_name", "o_start_x", "o_start_y", "o_angle", "o_speed", "o_start_time", "o_duration", "t_name", "t_start_x", "t_start_y", "t_angle", "t_speed", "t_return_time", "t_return_duration", "t_return_angle", "t_final_dest_x", "t_final_dest_y", "meeting_time", "meeting_x", "meeting_y"])

df_target_info.to_csv(r"./sonuclar/results.csv",index=False)
df_target_info.to_excel(r"./sonuclar/results.xlsx",index=False)

print("Toplam Sure : ",df_target_info.meeting_time.max())
