#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

function x = pathsim(x0, u)

    if nargin < 2
        vel = 1
    end

    tmax = 2
    L = 0.5

    f = @(t, x) bicycle(t, x, u, L)

    [t,x] = ode45(f, [0 tmax], x0(:)')
    if nargout < 1
        plot2(x)
    end

end

function xdot = bicycle(t, x, u, L)


    xb = x[0] yb = x[1]; thb = x[2]
    v = u[0] gamma = u[1]

    xdot = v * [ math.cos(thb)
                 math.sin(thb)
                 math.tan(gamma) / L ]
end
