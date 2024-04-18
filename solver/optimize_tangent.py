# ...   Imports

# standard
import logging
from abc import ABC, abstractmethod

# misc
import numpy as np
import scipy
from tqdm import tqdm

# custom
from .base import ABCSolver
from utils import spherical2cartesian, cartesian2spherical


logger = logging.getLogger(__name__)


class OptimizeTangent(ABCSolver):

    def _custom_init(self):
        """
        """

        # construct initial search grid across n-dimensional spherical
        # coordinates.
        logger.info("Initializing hyperplane search grid for initialization ...")
        grid_pi = np.linspace(0, np.pi, self.sample_per_angle)
        grid_2pi = np.linspace(0, 2*np.pi, self.sample_per_angle*2)

        grid = [grid_pi] * (self.dims-2)
        grid.append(grid_2pi)

        out = np.meshgrid(*grid)
        final_grid = np.array(out)
        final_grid = final_grid.reshape(self.dims-1, -1).T.reshape(-1, self.dims-1)

        base_tangents = []
        for s in tqdm(final_grid):
            n = spherical2cartesian(radius=1, angles=s)

            d_p, d_n = self.project_generators(n)
            h_p, h_n = self.construct_tangents(n, d_p, d_n)

            base_tangents.append(h_p)
        self.base_tangents = np.asarray(base_tangents)
        self.alphas_init = final_grid

        logger.info("Search grid:")
        logger.info(f"\t - sample_per_angle (option): {self.sample_per_angle}")
        logger.info(f"\t - resulting hyperplane count: {self.base_tangents.shape[0]}")

    def _set_defaults(self):
        self.directions = []
        self.sample_per_angle = 5

    def _parse_options(self, options):
        if "search_directions" in options:
            self.directions = options["search_directions"]
        if "samples_per_angle" in options:
            self.sample_per_angle = options["samples_per_angle"]

    def _solve(self):
        logger.info("Sampling metamer mismatch body boundary ... ")
        self.alpha_opt = []
        self.mmb_boundary_points = []
        for direction in tqdm(self.directions):
            d = np.hstack([np.array([0] * self.dim_phi), direction])

            alpha_opt, p_opt = self.boundary_in_direction(d)

            if alpha_opt is not None:
                self.alpha_opt.append(alpha_opt)
                self.mmb_boundary_points.append(p_opt)

    def _post_solve(self):
        """ Rerun failed optimizations.
        """
        logger.info("Detecting and fixing failed optimizations ... ")

        base_tangents = []
        for s in tqdm(self.alpha_opt):
            n = spherical2cartesian(radius=1, angles=s)

            d_p, d_n = self.project_generators(n)
            h_p, h_n = self.construct_tangents(n, d_p, d_n)

            base_tangents.append(h_p)

        self.base_tangents = np.asarray(base_tangents)
        self.alphas_init = np.array(self.alpha_opt)

        self.alpha_opt = []
        self.mmb_boundary_points = []
        for direction in tqdm(self.directions):
            d = np.hstack([np.array([0] * self.dim_phi), direction])

            alpha_opt, p_opt = self.boundary_in_direction(d)

            if alpha_opt is not None:
                self.alpha_opt.append(alpha_opt)
                self.mmb_boundary_points.append(p_opt)

    def boundary_in_direction(self, direction):
        self.angles = []
        self.p_p = []
        self.dir_cur = direction

        # get initial angular coordinates
        dist_p = -(self.base_tangents @ self.p0h) / (self.base_tangents[:, :-1] @ direction)
        idx_opt = np.where(dist_p > 0, dist_p, np.inf).argmin()
        a0 = self.alphas_init[idx_opt, :]

        # find boundary hyperplane

        # search direction
        tol = 1e-9
        last_result = 999999999
        for i in range(20):
            res = scipy.optimize.minimize(self.error_fun, a0,
                                          method='Nelder-Mead', tol=1e-6,
                                          options={'disp': False,
                                                   'maxiter': 5000})  # , callback=self.callback)
            # print(f"result at iteration {i+1}: {res.fun}")
            if (last_result - res.fun) < tol:
                break

            last_result = res.fun
            a0 = res.x

        if not res.success:
            print(
                "should not happen, consider fixing the optimizer settings")

        alpha_opt = res.x
        p_opt = self.p0 + self.error_fun(alpha_opt) * direction

        return alpha_opt, p_opt

    def construct_boundary_point(self, angles):
        n = spherical2cartesian(radius=1, angles=angles)

        d_p, d_n = self.project_generators(n)
        h_p, h_n = self.construct_tangents(n, d_p, d_n)

        dist_p = -(h_p @ self.p0h) / (h_p[:-1] @ self.dir_cur)
        dist_n = -(h_n @ self.p0h) / (h_n[:-1] @ self.dir_cur)

        n_proj = n @ self.cm_U

        if dist_p > 0 and dist_n < 0:
            return np.where(n_proj > 0, self.cm_U, 0).sum(1)
        elif dist_n > 0 and dist_p < 0:
            return np.where(n_proj < 0, self.cm_U, 0).sum(1)
        else:
            raise ValueError(
                "Central point of MMB is not located within the MMB!")

    def error_fun(self, alpha):
        n = spherical2cartesian(radius=1, angles=alpha)

        d_p, d_n = self.project_generators(n)
        h_p, h_n = self.construct_tangents(n, d_p, d_n)

        dist_p = -(h_p @ self.p0h) / (h_p[:-1] @ self.dir_cur)
        dist_n = -(h_n @ self.p0h) / (h_n[:-1] @ self.dir_cur)

        return max(dist_p, dist_n)

    def callback(self, angles):
        self.angles.append(angles)
        self.p_p.append(self.p0 + self.error_fun(angles) * self.dir_cur)
