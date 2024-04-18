# ...   Imports

# standard
import math

# misc
import numpy as np

# custom
from icosphere import icosphere


def cartesian2spherical(vector):
    """ Converts n-dimensional cartesian coordinates to spherical coordinates

    :param vector:
    :return:
    """

    n = len(vector)
    angles = []
    r = np.linalg.norm(vector)

    for i in range(0, n - 1):
        rc = np.linalg.norm(vector[i+1:])
        angles.append(math.atan2(rc, vector[i]))

    return r, np.asarray(angles)


def spherical2cartesian(radius, angles):
    """ Converts n-dimensional spherical coordinates to cartesian coordinates

    :param radius: the radial coordinate
    :param angles: n-1 angular coordinates
    :return:
    """
    n = len(angles)
    r = radius
    multi_sin = 1
    eucl_vec = []

    for i in range(0, n-1):
        eucl_vec.append( r * multi_sin * math.cos(angles[i]) )
        multi_sin *= math.sin(angles[i])

    eucl_vec.append( r * multi_sin * math.cos(angles[-1]) )
    eucl_vec.append( r * math.sin(angles[-1]) )

    eucl_vec = np.asarray(eucl_vec)
    eucl_vec = eucl_vec / np.linalg.norm(eucl_vec)

    return eucl_vec


def construct_ocs_2d(sw: np.array, T:int=400) -> np.array:
    ocs_boundary = []

    for idx in range(T):
        angle = idx / T * 2 * np.pi - np.pi / 2

        n = np.array([np.sin(angle), np.cos(angle)])
        n_proj = n @ sw
        ocs_boundary.append(np.where(n_proj > 0, sw, 0).sum(1))

    return np.asarray(ocs_boundary).T

def construct_ocs_3d(sw, subd=5):
    """ Constructs a set of boundary points on the ocs based on spherical
    sampling

    :param sw: the spectral weights
    :param subd: subdivision frequency of the icosahedron
    """

    subd_frequency = 20
    samples, faces = icosphere(subd_frequency)

    ocs_boundary = []

    for n in samples:
        n_proj = n @ sw
        ocs_boundary.append(np.where(n_proj > 0, sw, 0).sum(1))

    return np.asarray(ocs_boundary)