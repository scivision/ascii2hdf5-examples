"""
plot HDF5 proprietary data converted by ascii2hdf5.py
"""

from pathlib import Path
import argparse
import h5py
import numpy as np
from matplotlib.pyplot import subplots, show
from matplotlib.colors import LogNorm


def plot(dat: np.ndarray):
    if dat.ndim != 3:
        raise ValueError("Expected 3-D array")

    # a priori
    Naz = 20
    boundsAz = (-32.0, 32.0)
    Nspeed = 64
    boundsSpeed = (0.0, 20.0)
    Nel = 20
    boundsEl = (-32.0, 32.0)

    if dat.shape != (Naz, Nel, Nspeed):
        raise ValueError(f"Expected shape {Naz, Nel, Nspeed}")

    iel = Nel // 2 - 1  # 0 degrees
    iaz = Naz // 2 - 1  # 0 degrees

    Az = np.linspace(*boundsAz, Naz)
    El = np.linspace(*boundsEl, Nel)
    speed = np.linspace(*boundsSpeed, Nspeed)

    fg, ax = subplots(nrows=1, ncols=2, subplot_kw=dict(projection="polar"))

    h = ax[0].pcolormesh(np.radians(Az), speed, dat[iel, :, :].T, shading="nearest", norm=LogNorm())
    ax[0].set_thetalim(thetamin=boundsAz[0], thetamax=boundsAz[1])
    ax[0].set_xlabel("speed [km/sec]", rotation=boundsAz[0])
    fg.colorbar(h, ax=ax[0], shrink=0.25)

    h = ax[1].pcolormesh(np.radians(El), speed, dat[:, iaz, :].T, shading="nearest", norm=LogNorm())
    ax[1].set_thetalim(thetamin=boundsEl[0], thetamax=boundsEl[1])
    ax[1].set_xlabel("speed [km/sec]", rotation=boundsEl[0])
    fg.colorbar(h, ax=ax[1], shrink=0.25)

    fg.suptitle(filename.stem)


if __name__ == "__main__":
    P = argparse.ArgumentParser()
    P.add_argument("filename")
    p = P.parse_args()

    filename = Path(p.filename).expanduser()

    with h5py.File(filename, "r") as f:
        plot(f["/data"])

    show()
