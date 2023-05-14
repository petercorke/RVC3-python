#! /usr/bin/env python

"""
Creates Fig 9.28
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import numpy as np
import bdsim


def SEA(obstacle_pos=0.8, block=False, graphics=False):
    sim = bdsim.BDSim(name="SEA", graphics=graphics)

    bd = sim.blockdiagram()

    m1 = 0.5
    m2 = 1
    LQR = np.c_[169.9563, 62.9010, -19.9563, 71.1092].T
    print(LQR)
    Ks = 5
    force_lim = 2

    # define the blocks
    step = bd.STEP(1)
    inputgain = bd.GAIN(np.r_[1, 0, 1, 0])
    sum1 = bd.SUM("+-")
    lqr = bd.GAIN(LQR)
    limit = bd.CLIP(min=-force_lim, max=force_lim, name="torquelimit")

    motor_sum = bd.SUM("+-")
    motor_accel = bd.GAIN(1 / m1)
    motor_vel = bd.INTEGRATOR(x0=0)
    motor_pos = bd.INTEGRATOR(x0=0)

    spring_sum = bd.SUM("+-")
    spring_force = bd.GAIN(Ks)

    load_accel = bd.GAIN(1 / m2)
    load_vel = bd.INTEGRATOR(x0=0)
    load_pos = bd.INTEGRATOR(x0=0)
    obstacle = bd.FUNCTION(lambda x: 0 if x >= obstacle_pos else 1)
    load_prod = bd.PROD("**")

    spring_scope = bd.SCOPE(name="spring scope")
    state_scope = bd.SCOPE(
        vector=4,
        labels=["$x_m$", r"$\dot{x}_m$", "$x_l$", r"$\dot{x}_l$"],
        name="state scope",
    )

    fig_scope = bd.SCOPE(nin=3, labels=["$x_l$", "$u$", "$F_s$"], name="figure scope")
    mux = bd.MUX(4)

    # connect the blocks

    # controller
    bd.connect(step, inputgain)
    bd.connect(inputgain, sum1[0])
    bd.connect(mux, sum1[1])
    bd.connect(sum1, lqr)
    bd.connect(lqr, limit)

    # motor block
    bd.connect(limit, motor_sum[0], fig_scope[1])
    bd.connect(motor_sum, motor_accel)
    bd.connect(motor_accel, motor_vel)
    bd.connect(motor_vel, motor_pos, mux[1])
    bd.connect(motor_pos, spring_sum[0], mux[0])

    # load block
    bd.connect(load_pos, spring_sum[1], obstacle, mux[2], fig_scope[0])
    bd.connect(load_accel, load_vel)
    bd.connect(load_vel, load_prod[0])
    bd.connect(obstacle, load_prod[1])
    bd.connect(load_prod, load_pos, mux[3])

    # spring block
    bd.connect(spring_sum, spring_force)
    bd.connect(spring_force, motor_sum[1], load_accel, spring_scope, fig_scope[2])

    bd.connect(mux, state_scope)

    bd.compile()  # check the diagram

    sim.report(bd)
    out = sim.run(bd, 5, dt=5e-3, watch=[limit, spring_force])
    # out = vloop.run(2, checkstep=1e-6)  # simulate for 5s
    # # vloop.dotfile('bd1.dot')  # output a graphviz dot file
    # # vloop.savefig('pdf')      # save all figures as pdf

    return out


if __name__ == "__main__":
    SEA(block=True, graphics=True)
