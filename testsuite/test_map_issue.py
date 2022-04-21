import psyplot.project as psy
import os
from pathlib import Path


def test_map_issue():
    os.popen('python data/get_data.py')
    input_file = Path(
        'data/example_data/nc/my_exp1_atm_3d_ml_20180921T000000Z.nc')
    ds = psy.open_dataset(input_file)
    pp = psy.plot.mapplot(ds,
                          name='temp',
                          t=0,
                          bounds={
                              'method': 'minmax',
                              'vmin': 260.0,
                              'vmax': 300.0
                          })
    pp.update(projection='robin')
