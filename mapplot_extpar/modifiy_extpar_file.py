# Load required python packages
import sys
import numpy as np
import xarray as xr
xr.set_options(display_max_rows=44)
import argparse
from pathlib import Path

if __name__ == "__main__":

    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', dest = 'input_file',\
                            help = 'name of input file',\
                            default='/home/mjaehn/extpar/extpar_file.nc')
    parser.add_argument('--outfile', '-o', dest = 'output_file',\
                            help = 'name of output file',\
                            default = '/home/mjaehn/extpar/extpar_file_modified.nc')
    args = parser.parse_args()

    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.is_file():
        sys.exit(args.input_file + " is not a valid file name")
    output_file = args.output_file

    # Read input file
    with xr.open_dataset(input_file) as ds:
        # Change times
        ds = ds.assign_coords(time=ds.time + 1e7)
        # Split up LU_CLASS_FRACTION
        print(ds['LU_CLASS_FRACTION']['nclass_lu'])
        for i in ds['LU_CLASS_FRACTION']['nclass_lu'].values:
            print(i)
            print(ds['LU_CLASS_FRACTION'][i].values)
            print(np.mean(ds['LU_CLASS_FRACTION'][i].values))
            idx = i + 1
            varname = f'LU_CLASS_FRACTION_{idx:02d}'
            print(varname)
            ds[varname] = ds['LU_CLASS_FRACTION'][i]

        print(ds)

        # Write to netCDF file        
        ds.to_netcdf(path=output_file, mode='w')
