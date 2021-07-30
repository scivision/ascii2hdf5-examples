#!/usr/bin/env python3
"""
loads text data and converts to HDF5
assumes data is unsigned integer 8bit (uint8)

Michael Hirsch

Python >= 3.8

ASCII data is ~60kB as this is inefficient way to store data.
HDF5 file is 27.6kB uncompressed--a little fixed overhead due to HDF5 internal structure.

Expected raw data size would be 20 * 20 * 64 * 1 bytes = 25.6 kB
"""

import argparse
from pathlib import Path
import re
import numpy as np
import h5py


def read_text(filename: Path) -> np.ndarray:
    """
    read ASCII data from file
    """

    # a priori
    Nel = 20
    Naz = 20
    Nbin = 64

    filename = Path(filename).expanduser()

    dat = np.empty((Naz, Nel, Nbin), dtype=np.uint8)

    bpat = re.compile(r"(?<=azimuth_bin\=)\d+")
    dpat = re.compile(r"(?<=\[)((\d+\s*){20})(?=])")

    iaz = 0
    i = 0
    with open(filename) as f:
        for line in f:
            if m := bpat.search(line):
                iaz = int(m.group(0))
            elif dpat.search(line):
                for i in range(Nbin):
                    d = list(map(float, line[1:-2].split()))
                    if len(d) == 0:
                        raise ValueError(f"empty data line at {iaz}, {i}")
                    if len(d) < Nel:
                        # data fragmented onto next line, join together
                        line = f.readline()
                        d2 = list(map(float, line[:-2].split()))
                        d.extend(d2)
                    if len(d) != Nel:
                        raise ValueError(f"incorrect data line(s) near {iaz}, {i}")

                    dat[iaz, :, i] = d

                    if i < Nbin - 1:
                        line = f.readline()
            else:
                raise ValueError(f"unexpected raw data:\n{line}")

    return dat


def write_hdf5(data: np.ndarray, filename: Path):
    """
    write data to HDF5 file
    """

    with h5py.File(filename, "w") as f:
        f["/data"] = data


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
                if file.suffix == ".txt" and not file_in.with_suffix(".h5").is_file()
            ]
        )
        if not files:
            raise FileNotFoundError(file_in)
        for file in files:
            file_out = file.with_suffix(".h5")
            print(f"{file} => {file_out}")
            data = read_text(file)
            write_hdf5(data, file_out)
    elif file_in.is_file():
        write_hdf5(read_text(file_in), file_in.with_suffix(".h5"))
    else:
        raise FileNotFoundError(file_in)
