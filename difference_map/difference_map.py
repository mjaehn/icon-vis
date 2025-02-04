# load required python packages
import argparse
import sys
from pathlib import Path

import cmcrameri.cm as cmc
import icon_vis.modules as iconvis  # import icon-vis self-written modules
import matplotlib.pyplot as plt
import numpy as np
import psyplot.project as psy
import xarray as xr
from matplotlib.lines import Line2D

if __name__ == "__main__":

    ####################

    # A) Parsing arguments

    ####################

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", "-c", dest="config_path", help="path to config file"
    )
    parser.add_argument(
        "--infile1", "-i1", dest="input_file1", help="path to input file 1", default=""
    )
    parser.add_argument(
        "--infile2", "-i2", dest="input_file2", help="path to input file 2", default=""
    )
    parser.add_argument(
        "--outdir", "-d", dest="output_dir", help="output directory", default=Path.cwd()
    )
    parser.add_argument(
        "--outfile",
        "-o",
        dest="output_file",
        help="name of output file",
        default="difference_map_output.png",
    )
    parser.add_argument("-co", action="store_true", help="get config options")

    args = parser.parse_args()

    #####################

    # B) Read config file or show available options

    #####################

    # Show options for config file
    if args.co:
        print(
            "var, name (req): name of the variable as in the nc file\n"
            + "var, varlim (opt): lower and upper limit of color scale\n"
            + "var, grid_file (req if file is missing grid-information): path to grid file\n"
            + "var, height (opt): index of dimension height from variable (default 0)\n"
            + "map, lonmin/lonmax/latmin/latmax (opt): values for map extension\n"
            + "map, projection (opt): projection to draw on (e.g., robin)\n"
            + "map, add_grid (opt): set false to remove grid with lat and lon labels\n"
            + "map, title (opt): title of plot\n"
            + "map, cmap (opt): name of colorbar\n"
            + "map, diff (opt): relative difference with input diff=rel, else absolute difference\n"
            + "map, sig (opt): marks significant (sig=1) or insignificant (sig=2) data points\n"
            + "map, sig_leg (opt): add legend for significant markers\n"
            + "map, leg_loc (opt): location of legend for significant markers\n"
            + "map, alpha (opt): significance level (default 0.05)\n"
            + "map, col (opt): color of markers for sig/insig data points\n"
            + "map, marker (opt): marker for sig/insig data points\n"
            + "map, markersize (opt): marker size of markers for sig/insig data points\n"
            + "map, clabel (opt): label of colorbar\n"
            + "coord, name (opt): add markers at certain locations (several inputs possible)\n"
            + "coord, lon/lat (opt): lon and lat of the locations\n"
            + "coord, marker (opt): marker specifications for all locations\n"
            + "coord, marker_size (opt): marker sizes for all locations\n"
            + "coord, col (opt): colors of all markers for all locations"
        )
        sys.exit()

    # read config file
    var, map_c, coord, _ = iconvis.read_config(args.config_path)

    #############

    # C) Load data

    #############

    # Check if input files exists
    input_file1 = Path(args.input_file1)
    if not input_file1.is_file():
        sys.exit(args.input_file1 + " is not a valid file name")
    input_file2 = Path(args.input_file2)
    if not input_file2.is_file():
        sys.exit(args.input_file2 + " is not a valid file name")

    # load data
    if iconvis.check_grid_information(input_file1):
        data1 = psy.open_dataset(input_file1)
    elif "grid_file" in var.keys():
        data1 = iconvis.combine_grid_information(input_file1, var["grid_file"])
    else:
        sys.exit(
            "The file "
            + str(input_file1)
            + " is missing the grid information. Please provide a grid file in the config."
        )
    if iconvis.check_grid_information(input_file2):
        data2 = psy.open_dataset(input_file2)
    elif "grid_file" in var.keys():
        data2 = iconvis.combine_grid_information(input_file2, var["grid_file"])
    else:
        sys.exit(
            "The file "
            + str(input_file2)
            + " is missing the grid information. Please provide a grid file in the config."
        )

    # variable and related things
    var_field1 = getattr(data1, var["name"])
    var_dims1 = var_field1.dims
    values1 = var_field1.values

    # variable and related things
    var_field2 = getattr(data2, var["name"])
    var_dims2 = var_field2.dims
    values2 = var_field2.values

    # Check if height dimension exists
    height_ind = [i for i, s in enumerate(var_dims1) if "height" in s]
    if height_ind:
        values_red1 = values1[:, var["height"], :].squeeze()
    height_ind = [i for i, s in enumerate(var_dims2) if "height" in s]
    if height_ind:
        values_red2 = values2[:, var["height"], :].squeeze()

    # Calculate mean, difference and p-values
    var1_mean, _, var_diff, pvals = iconvis.get_stats(values_red1, values_red2)

    if map_c["diff"] == "rel":
        nonan = np.argwhere((~np.isnan(var_diff)) & (var1_mean != 0) & (var_diff != 0))
        var_diff[nonan] = 100 * (var_diff[nonan] / var1_mean[nonan])

    # Create new dataset, which contains the mean var_diff values
    data3 = xr.Dataset(
        data_vars=dict(var_diff=(["ncells"], var_diff)),
        coords=dict(
            clon=(["ncells"], data1.clon.values[:]),
            clon_bnds=(["ncells", "vertices"], data1.clon_bnds.values[:]),
            clat=(["ncells"], data1.clat.values[:]),
            clat_bnds=(["ncells", "vertices"], data1.clat_bnds.values[:]),
        ),
    )
    data3["clon"].attrs["bounds"] = "clon_bnds"
    data3["clat"].attrs["bounds"] = "clat_bnds"
    data3["clon"].attrs["units"] = "radian"
    data3["clat"].attrs["units"] = "radian"
    data3.var_diff.encoding["coordinates"] = "clat clon"

    #############

    # D) Plot data

    #############

    # Get map extension
    if "lonmin" not in map_c.keys():
        map_c["lonmin"] = min(np.rad2deg(data3.clon.values[:]))
    if "lonmax" not in map_c.keys():
        map_c["lonmax"] = max(np.rad2deg(data3.clon.values[:]))
    if "latmin" not in map_c.keys():
        map_c["latmin"] = min(np.rad2deg(data3.clat.values[:]))
    if "latmax" not in map_c.keys():
        map_c["latmax"] = max(np.rad2deg(data3.clat.values[:]))

    pp = data3.psy.plot.mapplot(name="var_diff")
    pp.update(
        map_extent=[map_c["lonmin"], map_c["lonmax"], map_c["latmin"], map_c["latmax"]]
    )
    if "projection" in map_c.keys():
        pp.update(projection=map_c["projection"])
    if "varlim" in var.keys():
        pp.update(
            bounds={
                "method": "minmax",
                "vmin": var["varlim"][0],
                "vmax": var["varlim"][1],
            }
        )
    if "add_grid" in map_c.keys():
        pp.update(xgrid=map_c["add_grid"], ygrid=map_c["add_grid"])
    if "title" in map_c.keys():
        pp.update(title=map_c["title"])
    if "cmap" in map_c.keys():
        pp.update(cmap=map_c["cmap"])
    else:
        pp.update(cmap=cmc.vik)
    if "clabel" in map_c.keys():
        pp.update(clabel=map_c["clabel"])
    pp.update(borders=True, lakes=True, rivers=False)

    fig = plt.gcf()
    if coord:
        # go to matplotlib level
        llon = map_c["lonmax"] - map_c["lonmin"]
        llat = map_c["latmax"] - map_c["latmin"]
        for i in range(0, len(coord["lon"])):
            pos_lon, pos_lat = iconvis.add_coordinates(
                coord["lon"][i],
                coord["lat"][i],
                map_c["lonmin"],
                map_c["lonmax"],
                map_c["latmin"],
                map_c["latmax"],
            )
            fig.axes[0].plot(
                pos_lon,
                pos_lat,
                coord["col"][i],
                marker=coord["marker"][i],
                markersize=coord["marker_size"][i],
                transform=fig.axes[0].transAxes,
            )
            if "name" in coord.keys():
                fig.axes[0].text(
                    pos_lon + llon * 0.003,
                    pos_lat + llat * 0.003,
                    coord["name"][i],
                    transform=fig.axes[0].transAxes,
                )

    # Add dots for significant/insignificant datapoints
    if map_c["sig"]:
        pfdr = iconvis.wilks(pvals, map_c["alpha"])
        if map_c["sig"] == 1:
            sig = np.argwhere(pvals < pfdr)
            sig_leg = "Significant differences"
        elif map_c["sig"] == 2:
            sig = np.argwhere((np.isnan(pvals)) | (pvals > pfdr))
            sig_leg = "Insignificant differences"
        else:
            sys.exit("Invalid number for map,sig")
        for i in sig:
            pos_lon, pos_lat = iconvis.add_coordinates(
                np.rad2deg(data3.clon.values[i]),
                np.rad2deg(data3.clat.values[i]),
                map_c["lonmin"],
                map_c["lonmax"],
                map_c["latmin"],
                map_c["latmax"],
            )
            fig.axes[0].plot(
                pos_lon,
                pos_lat,
                map_c["col"],
                marker=map_c["marker"],
                markersize=map_c["markersize"],
                transform=fig.axes[0].transAxes,
            )
        if map_c["sig_leg"]:
            leg_el = [
                Line2D(
                    [0],
                    [0],
                    marker=map_c["marker"],
                    color="None",
                    label=sig_leg,
                    markerfacecolor=map_c["col"],
                    markersize=map_c["markersize"],
                )
            ]
            fig.axes[0].legend(handles=leg_el, loc=map_c["leg_loc"])

    #############

    # E) Save figure

    #############

    output_dir = Path(args.output_dir)
    output_file = Path(output_dir, args.output_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
