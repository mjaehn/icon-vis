# Load required python packages
import sys
import numpy as np
import xarray as xr
import argparse
from pathlib import Path

if __name__ == "__main__":

    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', dest = 'input_file',\
                            help = 'name of input file',\
                            default='/store/c2sm/c2sme/VPRM/setup_C2SM/input/grid/extpar_file.nc')
    parser.add_argument('--outfile', '-o', dest = 'output_file',\
                            help = 'name of output file',\
                            default = '/store/c2sm/c2sme/VPRM/setup_C2SM/input/grid/extpar_file_modified.nc')
    args = parser.parse_args()

    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.is_file():
        sys.exit(args.input_file + " is not a valid file name")
    output_file = args.output_file

    # Read input file
    with xr.open_dataset(input_file) as ds:
        print(ds.keys())
        # Read and modifiy output file
        print(ds['time'].values) 
        times = [21110111., 11110211., 11110311., 11110411., 11110511., 11110611.,
                 11110711., 11110811., 11110911., 11111011., 11111111., 11111211.]
        ds = ds.assign_coords(time=ds.time + 1e7) 
        print(ds['time'].values)
        ds.to_netcdf(path=output_file, mode='w')

