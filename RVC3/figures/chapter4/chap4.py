#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## Initial Setup
format compact
close all
clear
clc

## Section 4.1.1 - Car-Like Mobile Robots
sl_lanechange
sim("sl_lanechange")
out
t = out.get("t") q = out.get("y")
stackedplot(t, q, ...
    "DisplayLabels", ["x", "y", "theta", "psi"], ...
    "GridVisible", 1, "XLabel", "Time")
plot(q(:,1), q(:,2))

## Section 4.1.1.1 - Moving to a Point

sl_drivepoint

xg = [5 5]

x0 = [8 5 pi/2]

r = sim("sl_drivepoint")

q = r.find("y")

plot(q(:,1), q(:,2))

## Section 4.1.1.2 - Following a Line

sl_driveline

L = [1 -2 4]

x0 = [8 5 pi/2]

r = sim('sl_driveline')

## 4.1.1.3

sl_pursuit

r = sim('sl_pursuit')


## 4.1.1.4 move to pose

sl_drivepose

xg = [5 5 pi/2]

x0 = [9 5 0]

r = sim('sl_drivepose')

q = r.find('y')
plot(q(:,1), q(:,2))

## 4.1.2 diff steer

## 4.2 flying robots

sl_quadrotor

mdl_quadrotor

sim('sl_quadrotor')


about result

plot(result(:,1), result(:,2:3))

