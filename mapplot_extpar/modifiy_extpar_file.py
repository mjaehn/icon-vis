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

        # Create VPRM classes
        ds['VPRM_01'] = ds['LU_CLASS_FRACTION_05'] + \
                        ds['LU_CLASS_FRACTION_08']
        ds['VPRM_02'] = ds['LU_CLASS_FRACTION_06'] + \
                        ds['LU_CLASS_FRACTION_07'] + \
                        ds['LU_CLASS_FRACTION_09']
        ds['VPRM_03'] = ds['LU_CLASS_FRACTION_10'] + \
                        ds['LU_CLASS_FRACTION_16'] + \
                        ds['LU_CLASS_FRACTION_17']
        ds['VPRM_04'] = ds['LU_CLASS_FRACTION_11'] + \
                        ds['LU_CLASS_FRACTION_12'] + \
                        ds['LU_CLASS_FRACTION_13'] + \
                        ds['LU_CLASS_FRACTION_15'] * 0.5
        ds['VPRM_05'] = ds['LU_CLASS_FRACTION_01'] * 0
        ds['VPRM_06'] = ds['LU_CLASS_FRACTION_01'] + \
                        ds['LU_CLASS_FRACTION_02'] + \
                        ds['LU_CLASS_FRACTION_03']
        ds['VPRM_07'] = ds['LU_CLASS_FRACTION_04'] + \
                        ds['LU_CLASS_FRACTION_14'] + \
                        ds['LU_CLASS_FRACTION_18']
        ds['VPRM_08'] = ds['LU_CLASS_FRACTION_15'] * 0.5 + \
                        ds['LU_CLASS_FRACTION_19'] + \
                        ds['LU_CLASS_FRACTION_20'] + \
                        ds['LU_CLASS_FRACTION_21'] + \
                        ds['LU_CLASS_FRACTION_22']

        # Write to netCDF file
        ds.to_netcdf(path=output_file, mode='w')
