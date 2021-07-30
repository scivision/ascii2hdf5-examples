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

from pathlib import Path
import re
import numpy as np
import h5py

# a priori
Nel = 20
Naz = 20
Nbin = 64

fn = Path("C_N_in72920.0_T_in6898.9_U_in7871.1_Nratio0.0.txt")
fnout = fn.with_suffix(".h5")

dat = np.empty((Naz, Nel, Nbin), dtype=np.uint8)

bpat = re.compile(r"(?<=azimuth_bin\=)\d+")
dpat = re.compile(r"(?<=\[)((\d+\s*){20})(?=])")

iaz = 0
i = 0
with open(fn) as f:
    for line in f:
        if m := bpat.search(line):
            iaz = int(m.group(0))
        elif dpat.search(line):
            for i in range(Nbin):
                try:
                    dat[iaz, :, i] = list(map(float, line[1:-2].split()))
                except ValueError:
                    print(iaz, i)
                    print(line)
                    raise
                if i < Nbin - 1:
                    line = f.readline()
        else:
            raise ValueError(f"unexpected raw data\n{line}")

with h5py.File(fnout, "w") as f:
    f["/data"] = dat
