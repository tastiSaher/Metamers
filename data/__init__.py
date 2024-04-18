""" Helper subpackage to provide various spectral functions

The visible wavelenth range from 380nm to 780nm in 1nm steps is considered.
Available are

Color matching functions:
    cmf     - CIE 1964 10 degree observer (https://cie.co.at/datatable/cie-1964-colour-matching-functions-10-degree-observer)

Spectral power distributions:
    il_A    -  CIE D65 (https://cie.co.at/datatable/cie-standard-illuminant-d65)
    il_D65  -  CIE A (https://cie.co.at/datatable/cie-standard-illuminant-1-nm)

"""

# ...   Imports

# standard
from pathlib import Path

# misc
import numpy as np


def load_cie_csv(fpath: Path) -> np.ndarray:
    data = np.genfromtxt(fpath, delimiter=',')
    data = np.nan_to_num(data)
    idx_start = np.where(data[:, 0] == wl_start)[0][0]
    idx_end = np.where(data[:, 0] == wl_end)[0][0] + 1
    return data[idx_start:idx_end, 1:].T.squeeze()

# ...   settings
wl_start = 380
wl_end = 780
wl_count = wl_end - wl_start + 1
wls = np.linspace(wl_start, wl_end, wl_count)

# ...   load and provide some defaults

# color matching functions of human standard observer
cmf = load_cie_csv(Path(__file__).parent / Path("CIE_xyz_1964_10deg.csv"))

# some illuminants
il_A = load_cie_csv(Path(__file__).parent / Path("CIE_std_illum_A_1nm.csv"))
il_D65 = load_cie_csv(Path(__file__).parent / Path("CIE_std_illum_D65.csv"))

