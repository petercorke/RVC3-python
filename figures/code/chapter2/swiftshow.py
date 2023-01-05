#! /usr/bin/env python3
from spatialmath import SE3
from roboticstoolbox.backends.swift import Swift
from spatialgeometry import Mesh

m = Mesh('/Users/corkep/Dropbox/code/RVC3-python/chapter2/fig2_4.dae')

env = Swift()
env.launch()
env.add(m)
env.hold()