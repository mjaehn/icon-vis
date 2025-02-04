# Vector Plot

**Description:**

The vector plot notebook plots the U, V vectors from ICON over Switzerland. Because the ICON data is at a very high resolution, fieldextra has been used via the [modules/interpolate.py](/modules/interpolate.py) module, to interpolate the data to both a regular grid a coarser ICON grid before plotting. DWD ICONtools could also be used for the interpolation. Follow the installation instruction in the main folder or activate your virtual environment before starting the jupyter notebook.

### Example plot

To create the example plots below, activate your conda environment or venv and start the vectorplot jupyter notebook.

<p float="left">
<img src=VectorPlot_Reg.png width="500"/>
<img src=VectorPlot_ICON.png width="500"/>
</p>
<p align="center">
<img src=VectorPlot_Stream.png width="550"/>
</p>
