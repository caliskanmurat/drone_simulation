# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:12:16 2022

@author: caliskan.murat
"""

import math, sys
import pygame
import numpy as np
import pandas as pd
from collections import defaultdict


#%%

RETURN_TO_CENTER = True
SCREEN_WIDTH, SCREEN_HEIGHT = 544, 751

#%%

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
        return math.degrees(alpha) if degree else alpha

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
    
    def scale(self, a,b, series):
        n = (series - series.min()) * (b-a)
        d = series.max() - series.min()
        return a + (n/d)

class Drone(Calculator):
    def __init__(self, screen, name, start_x, start_y, moving_angle, speed_ratio):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.X = start_x
        self.Y = self.SCREEN_HEIGHT - start_y
        self.NAME = name
        self.SPEED_RATIO = speed_ratio
        self.ANGLE = moving_angle
        
    def moveTo(self, speed_x, speed_y):
        self.X += speed_x * self.SPEED_RATIO
        self.Y -= speed_y * self.SPEED_RATIO
                    
    def __str__(self):
        return f"{self.NAME}"
    
    def __repr__(self):
        return f"{self.NAME}"
    
    def targetCoors(self, Target, delay=0):
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

class MovingObject():
    def __init__(self, screen, name, start_x, start_y, moving_angle, speed_ratio):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.X = start_x
        self.Y = self.SCREEN_HEIGHT - start_y
        self.NAME = name
        self.SPEED_RATIO = speed_ratio
        self.ANGLE = moving_angle
        
    def moveTo(self, speed_x, speed_y):
        self.X += speed_x * self.SPEED_RATIO
        self.Y -= speed_y * self.SPEED_RATIO
    
    def __str__(self):
        return f"{self.NAME}"
    
    def __repr__(self):
        return f"{self.NAME}"

class Simulation(Calculator):
    def __init__(self, width, height, simulation_data, speed_ratio):
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.SPEED_RATIO = speed_ratio
        self.SIMULATION_DATA = simulation_data.loc[simulation_data.meeting_x.between(0,self.WIDTH) & simulation_data.meeting_y.between(0,self.HEIGHT)].sort_values(by="meeting_time", ascending=True)
        
        
        self.drone_img = pygame.image.load("./veriler/drone.png").convert_alpha()
        self.drone_img = pygame.transform.scale(self.drone_img, (30,30))        
        
        self.bg = pygame.image.load("./veriler/bg.png").convert()
        
        self.target_color = (0,0,255)
        self.target_catched_color = (255,0,0)
        self.target_start_color = (0, 255, 255)
        self.score_board_color = (200,200,200)
    
    def start(self, randomize=False):
        global out_jpg_folder
        clock = pygame.time.Clock()
        pygame.init()
        myfont = pygame.font.SysFont("arialblack", 15)
        
        dr_list = self.SIMULATION_DATA.groupby("o_name").first()
        drone_list = [[o_n, Drone(self.screen, o_n, *dr.iloc[:3].values, self.SPEED_RATIO)] for o_n, dr in dr_list.iterrows()]
        
        obj_list = [[tr.meeting_time, tr.t_final_dest_x, tr.t_final_dest_y, tr.t_speed_final_x, tr.t_speed_final_y, tr.t_speed_x, tr.t_speed_y, tr.o_name, MovingObject(self.screen, *tr.iloc[7:11].values, self.SPEED_RATIO)] for i, tr in self.SIMULATION_DATA.iterrows()]
        
        running = True
        drone_scores = defaultdict(set)
        t=0
        return_time_max = self.SIMULATION_DATA.loc[:,"t_return_time"].max()
        fps = 60
        
        while running:
            clock.tick(fps)
            
            for event in pygame.event.get():
                if (event.type ==  pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    pygame.quit()
                    sys.exit()
            
            self.screen.blit(self.bg, (0,0))
            
            rect_height = dr_list.shape[0] * 20 + 60
            pygame.draw.rect(self.screen, self.score_board_color, pygame.Rect(0,0, 220, rect_height))
            
            
            if RETURN_TO_CENTER:
                center_x, center_y = self.SIMULATION_DATA[["t_final_dest_x","t_final_dest_y"]].iloc[0].values
            else:                
                center_x, center_y = None, None
            
            if center_x and center_y:
                pygame.draw.rect(self.screen, (0,255,255), pygame.Rect(center_x-20, self.HEIGHT-center_y-20, 40, 40))            
            
            
            self.screen.blit(myfont.render(f'Number of Drones : {dr_list.shape[0]}', False, (0, 0, 255)), (10,0))
            self.screen.blit(myfont.render(f'Number of Targets : {self.SIMULATION_DATA.shape[0]}', False, (0, 0, 255)), (10,20))
            
            for i, tr in self.SIMULATION_DATA.iterrows():                    
                pygame.draw.circle(self.screen, self.target_start_color, (tr.t_start_x+3, self.HEIGHT-tr.t_start_y+3), 6)
            
            if t < return_time_max:
                dr = self.SIMULATION_DATA.loc[self.SIMULATION_DATA.meeting_time >=t].groupby("o_name").first()
                
                for m_t, t_dest_x, t_dest_y, t_s_f_x, t_s_f_y, t_s_x, t_s_y, drn, obj in obj_list:
                    if (t >= m_t): # Target catched
                        pygame.draw.circle(self.screen, self.target_catched_color, (obj.X+3, obj.Y+3), 6)
                        drone_scores[drn].add(obj.NAME)
                        
                        # Move to center
                        if (center_x is not None) and (center_y is not None):
                            if (center_x-5<obj.X<center_x+5) and (self.HEIGHT-center_y-5<obj.Y<self.HEIGHT-center_y+5):
                                pygame.draw.circle(self.screen, self.target_catched_color, (obj.X+4, obj.Y+4), 6)
                            else:
                                obj.moveTo(t_s_f_x, t_s_f_y)
                        
                    else: # Target not catched
                        pygame.draw.circle(self.screen, self.target_color, (obj.X+3, obj.Y+3), 6)
                        obj.moveTo(t_s_x, t_s_y)
                
                for opr_name, drone in drone_list:
                    self.screen.blit(self.drone_img, (drone.X-15, drone.Y-7))
                    try:
                        drone.moveTo(dr.loc[opr_name].o_speed_x, dr.loc[opr_name].o_speed_y)
                    except:
                        pass
                    
                t += self.SPEED_RATIO
                
            else:
                for m_t, t_dest_x, t_dest_y, t_s_f_x, t_s_f_y, t_s_x, t_s_y, drn, obj in obj_list:
                    pygame.draw.circle(self.screen, self.target_catched_color, (obj.X+3, obj.Y+3), 6)
                    drone_scores[drn].add(obj.NAME)
                    
                for opr_name, drone in drone_list:
                    self.screen.blit(self.drone_img, (drone.X-15, drone.Y-7))
            
                        
            for e, (d_name, d_score) in enumerate(sorted(drone_scores.items(), key=lambda x:x[0]),1):
                score_txt = f"{d_name} : {len(d_score)}"
                text_score_of_drone = myfont.render(score_txt, False, (0, 0, 255))
                self.screen.blit(text_score_of_drone,(10, 30 + e*20))
            
            pygame.display.update()
            
#%% READ FLIGHT PLAN

operator_sheetname = "Operator"
target_sheetname = "Target"
df_results = pd.read_csv("./sonuclar/results.csv")

df_results["o_speed_x"] = df_results["o_speed"] * np.sin(np.radians(df_results["o_angle"]))
df_results["o_speed_y"] = df_results["o_speed"] * np.cos(np.radians(df_results["o_angle"]))

df_results["t_speed_x"] = df_results["t_speed"] * np.sin(np.radians(df_results["t_angle"]))
df_results["t_speed_y"] = df_results["t_speed"] * np.cos(np.radians(df_results["t_angle"]))

df_results["t_speed_final_x"] = df_results["t_speed"] * np.sin(np.radians(df_results["t_return_angle"]))
df_results["t_speed_final_y"] = df_results["t_speed"] * np.cos(np.radians(df_results["t_return_angle"]))

#%% RUN SIMULATOR

df_results_norm = df_results.copy()

cols_coor_x = ['o_start_x',  't_start_x',  'meeting_x']
cols_coor_y = ['o_start_y',  't_start_y',  'meeting_y']

if RETURN_TO_CENTER:
    cols_coor_x.append("t_final_dest_x")
    cols_coor_y.append("t_final_dest_y")

min_x = df_results.loc[:, cols_coor_x].min().min()
max_x = df_results.loc[:, cols_coor_x].max().max()
min_y = df_results.loc[:, cols_coor_y].min().min()
max_y = df_results.loc[:, cols_coor_y].max().max()

min_x_screen = SCREEN_WIDTH * 0.05
max_x_screen = SCREEN_WIDTH * 0.95

min_y_screen = SCREEN_HEIGHT * 0.05
max_y_screen = SCREEN_HEIGHT * 0.95

x_frac = (max_x_screen - min_x_screen) / (max_x - min_x)
y_frac = (max_y_screen - min_y_screen) / (max_y - min_y)


df_results_norm.loc[:, cols_coor_x] = min_x_screen + ((df_results.loc[:, cols_coor_x] - min_x) * (max_x_screen - min_x_screen)) / (max_x - min_x)
df_results_norm.loc[:, cols_coor_y] = min_y_screen + ((df_results.loc[:, cols_coor_y] - min_y) * (max_y_screen - min_y_screen)) / (max_y - min_y)

df_results_norm.loc[:, "o_speed_x"] *= x_frac
df_results_norm.loc[:, "o_speed_y"] *= y_frac

df_results_norm.loc[:, "t_speed_x"] *= x_frac
df_results_norm.loc[:, "t_speed_y"] *= y_frac

df_results_norm.loc[:, "t_speed_final_x"] *= x_frac
df_results_norm.loc[:, "t_speed_final_y"] *= y_frac


if __name__ == "__main__":
    simulation = Simulation(SCREEN_WIDTH, SCREEN_HEIGHT, simulation_data=df_results_norm, speed_ratio=0.040)
    simulation.start()
