# ...   Imports

# standard
import logging
import data

# misc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# custom
import solver
from utils import construct_ocs_2d


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # ...   1.) construct some color mechanisms (simple example of illuminant induced metamer mismatching)
    wls = data.wls

    cm_phi = data.cmf[1,:] * data.il_A
    cm_psi = data.cmf[1,:] * data.il_D65

    cm_phi = cm_phi / np.sum(cm_phi) * 100
    cm_psi = cm_psi / np.sum(cm_psi) * 100

    # ...   2.) Calculate MMB

    phi0 = 50

    solver_MMB_ot = solver.OptimizeTangent(cm_phi=cm_phi, cm_psi=cm_psi)

    # use this setting to increase or decrease the amount of boundary points you want to compute. A frequency of 10
    # corresponds to approximately 1000 points
    sample_grid = np.asarray([1, -1]) # there are only two directions we can search in
    options = {
        "search_directions": sample_grid,
    }
    solver_MMB_ot.configure(options)
    solver_MMB_ot.solve(phi0=phi0)

    # ...    3.) Draw results
    ocs_boundary = construct_ocs_2d(solver_MMB_ot.cm_U, 400)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # ocs
    ax.plot(ocs_boundary[0, :], ocs_boundary[1, :], zorder=2)
    # draw search line
    ax.plot([phi0, phi0], [200, -200], 'k', zorder=0)
    # MMB boundary
    boundary = np.asarray(solver_MMB_ot.mmb_boundary_points)
    ax.scatter(boundary[:,0], boundary[:,1])

    ax.grid(visible=True)
    ax.set(xlim=[-10, 110], ylim=[-10, 110], xlabel='Y under CIE A', ylabel=r'Y under CIE D65',)

    plt.show()



