"""
plot HDF5 proprietary data converted by ascii2hdf5.py
"""

from pathlib import Path
import h5py
import numpy as np
from matplotlib.pyplot import figure, show
import argparse


def plot(dat: np.ndarray):
    if dat.ndim != 3:
        raise ValueError("Expected 3-D array")

    # a priori
    Naz = 20
    Nspeed = 64
    Nel = 20

    if dat.shape != (Naz, Nel, Nspeed):
        raise ValueError(f"Expected shape {Naz, Nel, Nspeed}")

    iel = Nel // 2 - 1  # 0 degrees
    iaz = Naz // 2 - 1  # 0 degrees

    Az = np.linspace(-32, 32, Naz)
    El = np.linspace(-32, 32, Nel)
    speed = np.linspace(0, 20, Nspeed)

    # fg = figure(subplot_kw={'projection': 'polar'})
    fg = figure()
    ax = fg.subplots(nrows=1, ncols=2)
    ax[0].pcolormesh(speed, Az, dat[:, iel, :], shading="nearest")
    ax[1].pcolormesh(speed, El, dat[iaz, :, :], shading="nearest")


if __name__ == "__main__":
    P = argparse.ArgumentParser()
    P.add_argument("filename")
    p = P.parse_args()

    filename = Path(p.filename).expanduser()

    with h5py.File(filename, "r") as f:
        plot(f["/data"])

    show()
