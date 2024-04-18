# ...   Imports

# standard
import logging

# misc
import numpy as np
import matplotlib.pyplot as plt
from icosphere import icosphere

# custom
import solver
import data
from utils import construct_ocs_3d


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # ...   1.) construct some color mechanisms (simple example of illuminant induced metamer mismatching)
    wls = data.wls

    cm_phi = data.cmf * data.il_A
    cm_psi = data.cmf * data.il_D65

    # normalize brightness to 100
    cm_phi = cm_phi / np.sum(cm_phi[1,:]) * 100
    cm_psi = cm_psi / np.sum(cm_psi[1,:]) * 100

    logging.info("Close the plot to continue ...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))
    ax1.plot(wls, cm_psi.T)
    ax2.plot(wls, cm_phi.T)
    ax1.set(xlim=[data.wl_start, data.wl_end], xlabel='wavelength [nm]',
            ylabel=r'spectral weights $\sigma_i(\lambda)$', title="1964 standard observer under CIE A")
    ax2.set(xlim=[data.wl_start, data.wl_end], xlabel='wavelength [nm]',
            ylabel=r'spectral weights $\sigma_i(\lambda)$', title="1964 standard observer under CIE D65")
    plt.show()

    # simulate a color signal
    n_samples = len(wls)
    r0 = np.array([0.5] * n_samples)
    phi0 = cm_phi @ r0

    # ...   2.) Calculate MMB

    # configure solver
    solver_MMB_ot = solver.OptimizeTangent(cm_phi=cm_phi, cm_psi=cm_psi)

    # use this setting to increase or decrease the amount of boundary points you want to compute. A frequency of 10
    # corresponds to approximately 1000 points
    subd_frequency = 10
    sample_grid, faces = icosphere(subd_frequency)
    options = {
        "search_directions": sample_grid,
    }
    solver_MMB_ot.configure(options)
    solver_MMB_ot.solve(phi0=phi0)

    # ...    3.) Draw results

    # get OCS boundary
    ocs_bounds = construct_ocs_3d(cm_psi, subd=5)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    # plot mmb
    tphi = np.asarray(solver_MMB_ot.mmb_boundary_points)[:,:3]
    tpsi = np.asarray(solver_MMB_ot.mmb_boundary_points)[:,3:]
    ax.scatter(tpsi[:, 0], tpsi[:, 1], tpsi[:, 2])

    plt.show()
