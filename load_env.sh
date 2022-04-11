#!/bin/bash

PROJECT_FOLDER=/project/g110/pyvis_dev

if [[ $HOST == *'tsa'* ]]; then
    VENV_PATH=${PROJECT_FOLDER}/venv_tsa_test
elif [[ $HOST == *'daint'* ]]; then
    VENV_PATH=${PROJECT_FOLDER}/venv_daint_test
fi

# ---- required for cf-grib engine ------

if [[ $HOST == *'tsa'* ]]; then
    echo 'Loading modules for cf-grib engine'
    source ~osm/.opr_setup_dir
    export PATH=$OPR_SETUP_DIR/bin:$PATH
    export MODULEPATH=$MODULEPATH\:$OPR_SETUP_DIR/modules/modulefiles
    
    module load PrgEnv-gnu/19.2
    module load eccodes/2.19.0-gnu-8.3.0-nocuda-noomp
    module load eccodes_cosmo_resources/2.19.0.5

    export GRIB_DEFINITION_PATH=/project/g110/spack-install/tsa/cosmo-eccodes-definitions/2.19.0.7/gcc/zcuyy4uduizdpxfzqmxg6bc74p2skdfp/cosmoDefinitions/definitions/:/project/g110/spack-install/tsa/eccodes/2.19.0/gcc/viigacbsqxbbcid22hjvijrrcihebyeh/share/eccodes/definitions/
    export GRIB_SAMPLES_PATH=/project/g110/spack-install/tsa/cosmo-eccodes-definitions/2.19.0.7/gcc/zcuyy4uduizdpxfzqmxg6bc74p2skdfp/cosmoDefinitions/samples/:/project/g110/spack-install/tsa/eccodes/2.19.0/gcc/viigacbsqxbbcid22hjvijrrcihebyeh/share/eccodes/samples/
    
    module load python
    source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh
    eccodes=`spack location -i eccodes@2.19.0%gcc@8.3.0`
    export ECCODES_DIR=${eccodes}

fi

if [[ $HOST == *'tsa'* ]]; then
    echo 'Setting FIELDEXTRA_PATH for tsa'
    export FIELDEXTRA_PATH=/project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp
elif [[ $HOST == *'daint'* ]]; then
    echo 'Setting FIELDEXTRA_PATH for daint'
    export FIELDEXTRA_PATH=/project/s83c/fieldextra/daint/bin/fieldextra_gnu_opt_omp
fi

echo 'Activating virtual env'
if [[ $HOST == *'tsa'* ]]; then
	module use /apps/common/UES/sandbox/kraushm/tsa-PROJ/modules/all
	module load PrgEnv-gnu proj/8.0.0-fosscuda-2019b geos
    #module load eccodes
elif [[ $HOST == *'daint'* ]]; then
    export EASYBUILD_PREFIX=/project/g110/pyvis
    module load daint-gpu EasyBuild-custom PROJ GEOS cray-python ecCodes/2.23.0-CrayGNU-21.09
fi

source ${VENV_PATH}/bin/activate