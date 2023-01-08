# # 5.1 Introduction to Reactive Navigation
#

# ## 5.1.1 Braitenberg Vehicles
#

def sensorfield(x, y):
  xc, yc = (60, 90)
  return 200 / ((x - xc) ** 2 + (y - yc) ** 2 + 200)

%run -m braitenberg -H

# ## 5.1.2 Simple Automata
#

house = rtb_load_matfile("data/house.mat");

floorplan = house["floorplan"];
floorplan.shape

places = house["places"];
places.keys()

places.br3

bug = Bug2(occgrid=floorplan);

bug.plot();

bug.run(start=places.br3, goal=places.kitchen, animate=True);

path = bug.run(start=places.br3, goal=places.kitchen);
path.shape

# # 5.2 Introduction to Map-Based Navigation
#

# # 5.3 Planning with a Graph-Based Map
#

data = rtb_load_jsonfile("data/queensland.json");

for name, info in data["places"].items():
  plot_point(info["utm"], text=name)

data["routes"][0]

import pgraph
g = pgraph.UGraph()  # create empty undirected graph
for name, info in data["places"].items():
  g.add_vertex(name=name, coord=info["utm"])  # add a place
for route in data["routes"]:
  g.add_edge(route["start"], route["end"], 
             cost=route["distance"])  # add a route

g.plot()

g.n
g.ne

g["Brisbane"]

g["Brisbane"].neighbors() 

g["Brisbane"].degree

g.average_degree()

g.nc

edges = g["Brisbane"].edges()

edges[0].endpoints

path, length = g.path_BFS("Hughenden", "Brisbane")
length
", ".join([p.name for p in path])
g.plot()
g.highlight_path(path)



path, length, parents = g.path_UCS("Hughenden", "Brisbane")
length
", ".join([p.name for p in path])

parents["Winton"]

tree = pgraph.DGraph.Dict(parents);

tree.showgraph()

g.path_UCS("Hughenden", "Brisbane", verbose=True)


g["Bedourie"].edgeto(g["Birdsville"]).cost


path, length, parents = g.path_Astar("Hughenden", "Brisbane", summary=True)
length
", ".join([p.name for p in path])

# find the unique vertex names
visited = set(list(parents.keys()) + list(parents.values()));
g.plot()
g.highlight_vertex(visited, color="yellow")

g.path_Astar("Hughenden", "Brisbane", verbose=True)

# ## 5.3.1 Minimum-Time Path Planning
#

g = pgraph.UGraph()
for name, info in data["places"].items():
  g.add_vertex(name=name, coord=info["utm"])
for route in data["routes"]:
  g.add_edge(route["start"], route["end"], 
             cost=route["distance"] / route["speed"])

g.heuristic = lambda x: np.linalg.norm(x) / 100

path, time, _ = g.path_Astar("Hughenden", "Brisbane")
time
", ".join([p.name for p in path])

# ## 5.3.2 Wrapping Up
#

# # 5.4 Planning with an Occupancy-Grid Map
#

# ## 5.4.1 Distance Transform
#

map = np.zeros((100, 100));

map[40:50, 20:80] = 1;  # set to occupied

map.ravel()[np.random.choice(map.size, 100, replace=False)] = 1;

simplegrid = np.zeros((6, 6));
simplegrid[2:5, 3:5] = 1
simplegrid[3:5, 2] = 1

dx = DistanceTransformPlanner(occgrid=simplegrid);

dx.plan(goal=(1, 1))

dx.plot(labelvalues=True);

dx = DistanceTransformPlanner(occgrid=simplegrid, distance="manhattan");
dx.plan(goal=(1, 1))
dx.plot(labelvalues=True);

dx.plot_3d();

path = dx.query(start=(5, 4))

dx.plot(path);

dx.query(start=(5, 4), animate=True);

house = rtb_load_matfile("data/house.mat");
floorplan = house["floorplan"];
places = house["places"];

dx = DistanceTransformPlanner(occgrid=floorplan);
dx.plan(goal=places.kitchen)
dx.plot();

path = dx.query(start=places.br3);
path.shape

dx.plot(path);

dx.plan(places.kitchen, summary=True);

dx.plan(places.kitchen, animate=True);

dx = DistanceTransformPlanner(occgrid=floorplan, inflate=5);
dx.plan(places.kitchen);
p = dx.query(places.br3);
dx.plot(p);

# ## 5.4.2 D*
#

dstar = DstarPlanner(occgrid=floorplan);

c = dstar.costmap;

dstar.plan(goal=places.kitchen);

nexpand0 = dstar.nexpand

path = dstar.query(start=places.br3);

def sensorfunc(pos):
   if pos[0] == 300:  # near the door?
       changes = []
       for x in range(300, 325):
           for y in range(115,125):
               changes.append((x, y, np.inf))
       return changes

dstar.query(start=places.br3, sensor=sensorfunc);

dstar.nexpand - nexpand0

# # 5.5 Planning with Roadmaps
#

occgrid = floorplan.copy();

occgrid[0, :] = 1
occgrid[-1, :] = 1
occgrid[:, 0] = 1
occgrid[:, -1] = 1

freespace = Image(occgrid == 0)
freespace.disp();

skeleton = freespace.thin().disp();

sites = np.random.uniform(size=(2,9));
from scipy.spatial import Voronoi
vor = Voronoi(sites.T);

prm = PRMPlanner(occgrid=floorplan, seed=0);

prm.plan(npoints=50)

prm

prm.plot();

prm.plan(npoints=300)
prm.plot();
prm

np.random.rand(5)  # seeded by NumPy (not repeatable)
np.random.seed(42)
np.random.rand(5)  # with seed of 42
np.random.seed(42)
np.random.rand(5)  # with seed of 42

path = prm.query(start=places.br3, goal=places.kitchen);
prm.plot(path)

path = prm.query(start=places.br2, goal=places.kitchen);
path.shape

# # 5.6 Planning Driveable Paths
#

qs = (0, 0, pi/2);
qg = (1, 0, pi/2);

# ## 5.6.1 Dubins Path Planner
#

dubins = DubinsPlanner(curvature=1)

path, status = dubins.query(qs, qg)
path.shape

dubins.plot(path);

status

dubins.plot(path, configspace=True);

# ## 5.6.2 Reeds-Shepp Path Planner
#

rs = ReedsSheppPlanner(curvature=1)
path, status = rs.query(qs, qg)
path.shape
status

rs.plot(path, direction=status.direction);

rs.plot(path, configspace=True);

# ## 5.6.3 Lattice Planner
#

lp = LatticePlanner();
lp.plan(iterations=1, summary=True)
lp.plot()

lp.plan(iterations=2, summary=True)
lp.plot()

lp.plot(configspace=True)

lp.plan(iterations=8, summary=True)
lp.plot()

path, status = lp.query(qs, qg);
path.shape

lp.plot(path)

status

lattice = LatticePlanner(costs=[1, 10, 1])  # S, L, R
lp.plan(iterations=8)
path, status = lp.query(qs, qg)

og = BinaryOccupancyGrid(workspace=[-5, 5, -5, 5], value=False)

og.set([-2, 0, -2, -1], True)
og.set([2, 3, 0, 4], True)
og.set([0, 2, -2, -2], True)

lattice = LatticePlanner(occgrid=og)
lattice.plan(iterations=None)

path, status = lattice.query(qs, qg)
lattice.plot(path)

# ## 5.6.4 Curvature Polynomials
#

cpoly = CurvaturePolyPlanner()
path, status = cpoly.query(qs, qg)
status
                poly=array([ 3.059, 3.095, 2.234, -4.865]))
cpoly.plot(path);

# ## 5.6.5 Planning in Configuration Space
#

map = PolygonMap(workspace=[0, 10]);
map.add([(5, 50), (5, 6), (6, 6), (6, 50)])
map.add([(5, 4), (5, -50), (6, -50), (6, 4)])

map.plot()

qs = (2, 8, -pi/2);
qg = (8, 2, -pi/2);

piano = VehicleIcon("piano", scale=3)
piano.plot(qs);
piano.plot(qg);

l, w = 3, 1.5;
vpolygon = Polygon2([(-l/2, w/2), (-l/2, -w/2),
                     (l/2, -w/2), (l/2, w/2)]);

q = (2, 4, 0);

map.iscollision(vpolygon.transformed(SE2(q)))

vehicle = Bicycle(steer_max=1, L=2, polygon=vpolygon);

vehicle.curvature_max

rrt = RRTPlanner(map=map, vehicle=vehicle, npoints=50, showsamples=True, seed=0)

q = rrt.qrandom()
rrt.iscollision(q)

rrt.plan(goal=qg, animate=True)

path, status = rrt.query(start=qs);

rrt.g.plot()

rrt.g.highlight_path(status.vertices, color="red")

rrt.plot(path);

status.initial_d

# # 5.7 Advanced Topics
#

# ## 5.7.1 A* vs Dijkstra Search
#

# ## 5.7.2 Converting Grid Maps to Graphs
#

# ## 5.7.3 Converting between Graphs and Matrices
#

import pgraph
g = pgraph.UGraph()
for i in range(4):  # add 4 vertices
  g.add_vertex()
g[0].connect(g[1], cost=1);  # 0 -- 1
g[0].connect(g[3], cost=2);  # 0 -- 3
g[1].connect(g[2], cost=3);  # 1 -- 2
g.distance()

# ## 5.7.4 Local and Global Planning
#

# # 5.8 Wrapping Up
#

# ## 5.8.1 Resources
#

# ## 5.8.2 Exercises
#

