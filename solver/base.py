# ...   Imports

# standard
import logging
from abc import ABC, abstractmethod

# misc
import numpy as np
import scipy


logger = logging.getLogger(__name__)


class ABCSolver(ABC):
    """ Abstract base class for all MMB solvers

    Implements basic functionality like storing and preparing all relevant
    data, calculating an initial metamer, etc.
    """
    def __init__(self, cm_phi, cm_psi):
        # store input
        self.cm_phi = cm_phi
        self.cm_psi = cm_psi
        self.phi0 = None
        self.psi0 = None

        # construct unified color mechanism by stacking
        self.cm_U = np.vstack([cm_phi, cm_psi])

        if len(cm_phi.shape) == 1:
            self.dim_phi = 1
        else:
            self.dim_psi = cm_psi.shape[0]

        if len(cm_phi.shape) == 1:
            self.dim_psi = cm_psi.shape[0]
        else:
            self.dim_phi = cm_phi.shape[0]

        self.dims, self.nsamples = self.cm_U.shape

        self._set_defaults()

    def find_initial_metamer(self):
        """ Locate initial metamer

        This is just a rather naive brute force approach: starting with a
        reflectance r(lambda) = 0.5, optimize the reflectance to match the
        observed color signal. Subsequently, calculate the color signal of the
        second observer.
        """

        logger.info("\t   Searching for an initial metamer ... ")

        bnds = ((0, 1) for n in range(self.nsamples))
        r0 = [0.5] * self.nsamples
        result = scipy.optimize.minimize(self.signal_formation, r0,
                                         method='TNC', bounds=bnds,
                                         options={'disp': False})
        self.psi0 = self.cm_psi @ result.x

        logger.info(f"\t - Initial metamer: {self.psi0} ")

        # construct a "center" inside the metamer mismatch body
        self.p0 = np.hstack([self.phi0, self.psi0])      # inhomogneous coordinates
        self.p0h = np.hstack([self.phi0, self.psi0, 1])  # homogeneous coordinates

    def signal_formation(self, r):
        """ Converts a spectral object reflectance to the associated color
        signal of the first observer/illuminant pair.

        :param r: spectral object reflectance

        :return: color signal
        """
        color_signal = self.cm_phi @ r

        difference = color_signal - self.phi0
        return np.linalg.norm(difference)

    def _pre_solve(self):
        """ Use this to implement functionality that is required prior to
        solving the MMB.
        """
        pass

    @abstractmethod
    def _solve(self):
        """ Use this to implement the main solver.
        """
        pass

    def _post_solve(self):
        """ Use this to implement potential post processing
        """
        pass

    def _custom_init(self):
        """ Overwrite if you require basic initialization
        """
        pass

    def _set_defaults(self):
        """ Use this function of you want to add some default settings to your
        solver

        :return:
        """
        pass

    def _parse_options(self, options):
        """ Use this function to implement custom config parsing.

        :return:
        """
        pass

    def solve(self, phi0):
        """ Calculates the MMB.
        """

        self.phi0 = phi0

        # log basic info
        logger.info("First color mechanism: ")
        logger.info(f"\t - Dimensionality: {self.cm_phi.shape[0]} ")
        logger.info(f"\t - Observed color signal: {self.phi0} ")
        logger.info("Second color mechanism: ")
        logger.info(f"\t - Dimensionality: {self.cm_psi.shape[0]} ")

        self.find_initial_metamer()

        self._pre_solve()
        self._solve()
        self._post_solve()

    def configure(self, options):
        self._parse_options(options)
        self._custom_init()

    def project_generators(self, n):
        """ Accumulate all spectral weights in the respective half-spaces.

        :param n: normal vector defining a hyperplane through the origin.
        """
        n_proj = n @ self.cm_U

        d_p = np.where(n_proj > 0, n_proj, 0).sum()
        d_n = np.where(n_proj < 0, n_proj, 0).sum()

        return d_p, d_n

    def construct_tangents(self, n: np.array, d_p: float, d_n: float):
        """

        :param n: normal vector of the tangent hyperplane
        :param d_p: positive projection of spectral weights
        :param d_n: negative projection of spectral weights
        """
        h_p = np.append(n, -d_p)
        h_n = np.append(n, -d_n)

        return h_p, h_n
