#!/bin/bash

source /work/dori/pamtraenv/bin/activate
export OPENBLAS_NUM_THREADS=1
export PAMTRA_DATADIR=/work/dori/pamtra-data

NP=24

ICON_PATH=/data/mod/icon_local/nyalesund/
ROOT_PATH=/data/mod/icon_local/nyalesund/pamtra_runs/
DATA_PATH=${ROOT_PATH}data/
PLOT_PATH=${ROOT_PATH}plots/
CODE_PATH=/work/dori/pamtra-icon/
TMP_PATH=${CODE_PATH}tmp/

cd ${CODE_PATH}

#FIRST_DAY='20240201'
TODAY=`date +%Y%m%d`
FIRST_DAY='20240731'

declare -a hydro_combo=("all_hydro") # "no_snow" "only_snow" "only_liquid" "only_ice" "only_graupel_hail")
declare -a radar_names=("Joyrad94" "NyRAD35" "GRaWAC167" "GRaWAC175") # "Joyrad10" "Joyrad35" "Grarad94"

newdata=0
DAY=$FIRST_DAY
echo $DAY $TODAY
until [[ ${DAY} > ${TODAY} ]]; do
    year=$(date -d "$DAY + 1 day" +%Y)
    mon=$(date -d "$DAY + 1 day" +%m)
    # Check if there is ICON output
    ICON_file=${ICON_PATH}/${year}/${mon}/${DAY}_r600m_f2km/METEOGRAM_patch001_${DAY}_awipev.nc
    if [ -f ${ICON_file} ]; then
        echo ${DAY}
        passiveFile=${DATA_PATH}radiometer/${DAY}_r600_f2km_joy94_passive89.nc
        if [ -f $passiveFile ]; then
            echo "passive "${DAY}" already done"
        else
            python3 ${CODE_PATH}run_pamtra.py -i ${ICON_file} -sp ${passiveFile} -hy all_hydro -r joy94_passive89 -np ${NP} > ${TMP_PATH}pamtra${DAY}_passive.out
	    newdata=1
        fi
        for hydro in "${hydro_combo[@]}"; do
            for radar in "${radar_names[@]}"; do
                radarFile=${DATA_PATH}radar/${hydro}/${DAY}_r600_f2km_${hydro}_mom_${radar}.nc
                if [ -f ${radarFile}  ]; then
                    echo "Already processed " ${DAY} ${hydro} ${radar}
                else
                    echo "Running "${DAY} ${hydro} ${radar}
                    python3 ${CODE_PATH}run_pamtra.py -i ${ICON_file} -sp ${radarFile} -hy ${hydro} -r ${radar} -np ${NP} > ${TMP_PATH}pamtra${DAY}_${hydro}_${radar}.out
                    newdata=1
                fi
            done
            if [ "$newdata" -eq "1" ]; then
                plotFile=${PLOT_PATH}/${hydro}/${DAY}${hydro}pamtra94nya.png
                echo "Newdata ... plotting"
                #changed python2 to python3
                python3 plot_rad94_awipev.py -s ${plotFile} -r ${radarFile} -p ${passiveFile}
                newdata=0
            fi
        done
    else
        echo "no ICON data for "${DAY} ${ICON_file}
    fi
    DAY=$(date -d "$DAY + 1 day" +%Y%m%d)
done

