# ascii2hdf5-examples

Examples of converting proprietary ASCII formats to HDF5 using Numpy to parse text data and write to HDF5 files with h5py.

## Install

```sh
pip install -r requirements.txt
```

## Run

This example is for specific sensor data.
You'll need to adapt the code to your text data.

```sh
python ascii2netcdf.py ~/data/myfile.txt
# creates NetCDF4 file ~/data/myfile.nc

python plot.py ~/data/myfile.nc
```
