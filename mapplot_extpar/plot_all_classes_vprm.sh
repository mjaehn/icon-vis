#!/bin/bash

old_num=00

# Map index to land-use class description
declare -a classes=('evergreen'
                    'deciduous'
                    'mixed forest'
                    'shrubland'
                    'savanna'
                    'cropland'
                    'grassland'
                    'urban area'
                   )

idx=0
configfile=config_mapplot_vprm.ini
for i in {01..08}
do
    echo "Index ${i} is ${classes[$idx]}"
    sed -i "s/${old_num}/${i}/g" ${configfile}
    if [[ i -eq 01 ]]
    then 
        sed -i "s/<placeholder>/${classes[$idx]}/g" ${configfile}
    else
        last_idx="$((idx-1))"
        sed -i "s/${classes[$last_idx]}/${classes[$idx]}/g" ${configfile}
    fi
    python mapplot.py  --config ${configfile} --infile /home/mjaehn/extpar/extpar_file_modified.nc --outfile vprm_lu_class_${i}.png
    old_num=${i}
    idx="$((idx+1))"
done
sed -i "s/${old_num}/00/g" ${configfile}
sed -i "s/${classes[22]}/<placeholder>/g" ${configfile}


