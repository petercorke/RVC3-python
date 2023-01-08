# # 4.1 Wheeled Mobile Robots
#

# ## 4.1.1 Car-Like Mobile Robots
#

%run -m lanechange -H

out

plt.plot(out.t, out.x);  # q vs time

plt.plot(out.x[:,0], out.x[:,1]);  # x vs y

# ### 4.1.1.1 Driving to a Point
#

pgoal = (5, 5);

qs = (8, 5, pi / 2);

%run -i -m drivepoint -H

q = out.x;  # configuration vs time
plt.plot(q[:, 0], q[:, 1]);

# ### 4.1.1.2 Driving Along a Line
#

L = (1, -2, 4);

qs = (8, 5, pi / 2);

%run -i -m driveline -H

# ### 4.1.1.3 Driving Along a Path
#

%run -m drivepursuit -H

# ### 4.1.1.4 Driving to a Configuration
#

qg = (5, 5, pi / 2);

qs = (9, 5, 0);

%run -i -m driveconfig -H

q = out.x;  # configuration vs time
plt.plot(q[:, 0], q[:, 1]);

# ## 4.1.2 Differentially-Steered Vehicle
#

# ## 4.1.3 Omnidirectional Vehicle
#

# # 4.2 Aerial Robots
#

%run -m quadrotor -H

t = out.t; x = out.x;
x.shape

plt.plot(t, x[:, 0], t, x[:, 1]);

# # 4.3 Advanced Topics
#

# ## 4.3.1 Nonholonomic and Underactuated Systems
#

# # 4.4 Wrapping Up
#

# ## 4.4.1 Further Reading
#

veh = Bicycle(speed_max=1, steer_max=np.deg2rad(30));
veh.q

veh.step([0.3, 0.2])
veh.q

veh.deriv(veh.q, [0.3, 0.2])

# ## 4.4.2 Exercises
#

