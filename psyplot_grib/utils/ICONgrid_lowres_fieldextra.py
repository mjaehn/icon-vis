from pathlib import Path
import subprocess

remap_snippet = """
!*********************************************************************************************
! Namelist for remapping ICON grid to regular grid
! Usage: fieldextra remap.nl
!        where fieldextra points to /project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp
!*********************************************************************************************
!!!! HEADER
! Global settings
&RunSpecification
 verbosity             = "high"
 additional_diagnostic = .true.
/
&GlobalResource
 dictionary            = "/project/s83c/fieldextra/tsa/resources/dictionary_icon.txt"
 grib_definition_path  = "/project/s83c/fieldextra/tsa/resources/eccodes_definitions_cosmo",
                         "/project/s83c/fieldextra/tsa/resources/eccodes_definitions_vendor"
 grib2_sample          = "/project/s83c/fieldextra/tsa/resources/eccodes_samples/COSMO_GRIB2_default.tmpl"
 icon_grid_description = '{grid_file}',
                         '/scratch/vcherkas/icon-vis/psyplot/psyplot_grib/tmp/fieldextra/mch_ch_coarsegrid_wind_R19B04.nc'
/
&GlobalSettings
 default_model_name            = "icon"
 default_product_category      = "determinist"
 default_out_type_stdlongitude = .true.
/
! Model specifc information
&ModelSpecification
 model_name            = "icon"
 regrid_method         = "icontools,rbf",
/
! Information associated to imported NetCDF file
&NetCDFImport
 dim_default_attribute = "ncells:long_name=unstructured_grid_cell_index value=index",
                         "alt: axis=z standard_name=height",
/
!!!! PRODUCT
&Process
  in_file='{data_file}'
  out_file='{file_out}', out_type="GRIB2",
  out_regrid_target = "icon_grid,cell,/scratch/vcherkas/icon-vis/psyplot/psyplot_grib/tmp/fieldextra/mch_ch_coarsegrid_wind_R19B04.nc"
  out_regrid_method = "default"
  in_size_vdate = {num_dates}
/
&Process in_field = "U" /
&Process in_field = "V" /
"""

filetypes = {"grib2": (2, ""), "netcdf2": (4, ".nc"), "netcdf4": (5, ".nc")}

init_remap_namelist = "NAMELIST_ICON_LOWRES_REMAP"

output_dir = Path('./tmp/fieldextra')
output_dir.mkdir(parents=True, exist_ok=True)


def create_remap_namelist(data_file, grid_file, file_out, num_dates):
    with open(output_dir / Path(init_remap_namelist), "w") as f:
        f.write(
            remap_snippet.format(data_file=data_file,
                                 grid_file=grid_file,
                                 file_out=file_out.resolve(),
                                 num_dates=num_dates
                                 #init_type=filetypes[init_type][0],
                                 ))


def remap_ICON_to_lowresICON(data_file, grid_file, num_dates):
    file_out = output_dir / (Path(data_file).stem + "_lowresgrid.grb2")
    create_remap_namelist(data_file, grid_file, file_out, num_dates)
    f = open("tmp/fieldextra/LOG_ICON_LOWRES_REMAP.txt", "w")
    subprocess.run(["/project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp",  \
                "./tmp/fieldextra/NAMELIST_ICON_LOWRES_REMAP"], \
               stdout=f )
    return file_out.resolve()
