"""
plot HDF5 proprietary data converted by ascii2hdf5.py
"""

from pathlib import Path
import xarray
import argparse
import numpy as np
from matplotlib.pyplot import subplots, show
from matplotlib.colors import LogNorm


def plot(dat: xarray.DataArray):
    if dat.ndim != 3:
        raise ValueError("Expected 3-D array")

    iel = dat.elevation.size // 2 - 1  # 0 degrees
    iaz = dat.azimuth.size // 2 - 1  # 0 degrees

    speed = dat.speed
    azr = np.radians(dat.azimuth)
    elr = np.radians(dat.elevation)

    fg, ax = subplots(nrows=1, ncols=2, subplot_kw=dict(projection="polar"))

    h = ax[0].pcolormesh(azr, speed, dat[:, :, iel].T, shading="nearest", norm=LogNorm())
    ax[0].set_thetalim(thetamin=dat.azimuth[0], thetamax=dat.azimuth[-1])
    ax[0].set_xlabel("speed [km/sec]", rotation=dat.azimuth[0].item())
    fg.colorbar(h, ax=ax[0], shrink=0.25)

    h = ax[1].pcolormesh(elr, speed, dat[iaz, :, :], shading="nearest", norm=LogNorm())
    ax[1].set_thetalim(thetamin=dat.elevation[0], thetamax=dat.elevation[-1])
    ax[1].set_xlabel("speed [km/sec]", rotation=dat.elevation[0].item())
    fg.colorbar(h, ax=ax[1], shrink=0.25)

    fg.suptitle(filename.stem)


if __name__ == "__main__":
    P = argparse.ArgumentParser()
    P.add_argument("filename")
    p = P.parse_args()

    filename = Path(p.filename).expanduser()

    dat = xarray.load_dataarray(filename)
    plot(dat)

    show()
