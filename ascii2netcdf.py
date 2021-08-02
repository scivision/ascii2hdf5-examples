#!/usr/bin/env python3
"""
loads text data and converts to NetCDF4
assumes data is unsigned integer 8bit (uint8)

Michael Hirsch

Python >= 3.8

ASCII data is ~60kB as this is inefficient way to store data.
HDF5 file is 27.6kB uncompressed--overhead due to HDF5 internal structure.
NetCDF4 file is ~ 35kB uncompressed due to additional overhead of NetCDF4 axes and metadata.

Expected raw data size would be 20 * 20 * 64 * 1 bytes = 25.6 kB
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import numpy as np
import xarray


def read_text(filename: Path) -> xarray.DataArray:
    """
    read ASCII data from file
    """

    # a priori
    Nel = 20
    Naz = 20
    Nspeed = 64
    boundsAz = (-32.0, 32.0)
    boundsSpeed = (0.0, 20.0)
    boundsEl = (-32.0, 32.0)

    filename = Path(filename).expanduser()

    dat = xarray.DataArray(
        coords={
            "azimuth": np.linspace(*boundsAz, Naz, dtype=np.float32),
            "speed": np.linspace(*boundsSpeed, Nspeed, dtype=np.float32),
            "elevation": np.linspace(*boundsEl, Nel, dtype=np.float32),
        },
        dims=["azimuth", "speed", "elevation"],
    ).astype(np.uint8)

    bpat = re.compile(r"(?<=azimuth_bin\=)\d+")
    dpat = re.compile(r"(?<=\[)((\d+\s*){20})(?=])")

    iaz = 0
    i = 0
    with open(filename) as f:
        for line in f:
            if m := bpat.search(line):
                iaz = int(m.group(0))
            elif dpat.search(line):
                for i in range(Nspeed):
                    d = text2list(line)
                    if len(d) == 0:
                        raise ValueError(f"empty data line at {iaz}, {i}")
                    if len(d) < Nel:
                        # data fragmented onto next line, join together
                        # assumes that data isn't broken over more than 2 lines
                        line = f.readline()
                        d.extend(text2list(line))
                    if len(d) != Nel:
                        raise ValueError(f"incorrect data line(s) near {iaz}, {i}\n{line}")
                    # data line length is now correct
                    dat[iaz, i, :] = np.array(d).astype(np.uint8)
                    # this azimuth "page", this speed, Nel elevations

                    if i < Nspeed - 1:
                        line = f.readline()
            else:
                raise ValueError(f"unexpected raw data:\n{line}")

    return dat


def drop_brackets(s: str) -> str:
    return s.replace("[", "").replace("]", "")


def text2list(line: str) -> list[float]:

    return list(map(float, drop_brackets(line).split()))


if __name__ == "__main__":
    P = argparse.ArgumentParser(description="Load instrument text data and convert to HDF5")
    P.add_argument("path", help="path (or directory to iterate) to ASCII data file")
    p = P.parse_args()

    file_in = Path(p.path).expanduser()
    if file_in.is_dir():
        files = sorted(
            [
                file
                for file in file_in.iterdir()
                if file.suffix == ".txt" and not file_in.with_suffix(".nc").is_file()
            ]
        )
        if not files:
            raise FileNotFoundError(file_in)
        for file in files:
            file_out = file.with_suffix(".nc")
            print(f"{file} => {file_out}")
            read_text(file).to_netcdf(file_out, mode="w", format="NETCDF4")
    elif file_in.is_file():
        read_text(file_in).to_netcdf(file_in.with_suffix(".nc"), mode="w", format="NETCDF4")
    else:
        raise FileNotFoundError(file_in)
