#!/bin/bash

old_num=00

# Map index to land-use class description
declare -a classes=('irrigated croplands'
                    'rainfed croplands'
                    'mosaic cropland (50-70 pct) - vegetation (20-50 pct)'
                    'mosaic vegetation (50-70 pct) - cropland (20-50 pct)'
                    'closed broadleaved evergreen forest'
                    'closed broadleaved deciduous forest'
                    'open broadleaved deciduous forest'
                    'closed needleleaved evergreen forest'
                    'open needleleaved evergreen or deciduous forest'
                    'mixed broadleaved and needleleaved forest'
                    'mosaic shrubland (50-70 pct) - grassland (20-50 pct)'
                    'mosaic grassland (50-70 pct) - shrubland (20-50 pct)'
                    'closed to open shrubland'
                    'closed to open herbaceous vegetation'
                    'sparse vegetation'
                    'closed to open forest regulary flooded'
                    'closed forest or shrubland permanently flooded'
                    'closed to open grassland regularly flooded'
                    'artificial surfaces'
                    'bare areas'
                    'water bodies'
                    'permanent snow and ice'
                    'undefined'
                   )

idx=0
configfile=config_mapplot.ini
for i in {01..23}
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
    python mapplot.py  --config ${configfile} --infile /home/mjaehn/extpar/extpar_file_modified.nc --outfile extpar_lu_class_${i}.png
    old_num=${i}
    idx="$((idx+1))"
done
sed -i "s/${old_num}/00/g" ${configfile}
sed -i "s/${classes[22]}/<placeholder>/g" ${configfile}


