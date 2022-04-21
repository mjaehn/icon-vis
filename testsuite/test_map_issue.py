import psyplot.project as psy
import os


def test_map_issue():
    cmd = 'python data/get_data.py'
    os.popen(cmd)
    ds = psy.open_dataset('data/example_data/nc/my_exp1_atm_3d_ml_20180921T000000Z.nc')
    pp = psy.plot.mapplot(ds, name='temp', t=0, bounds={'method': 'minmax', 'vmin': 260.0, 'vmax': 300.0})
    pp.update(projection='robin')
