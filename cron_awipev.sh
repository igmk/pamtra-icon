#!/bin/bash

source /home/dori/.bashrc
export OPENBLAS_NUM_THREADS=1

NP=4

ICON_PATH=/data/inscape/icon/experiments/nyalesund/testbed/
ROOT_PATH=/data/optimice/pamtra_runs/awipev/
DATA_PATH=${ROOT_PATH}data/
PLOT_PATH=${ROOT_PATH}plots/
CODE_PATH=/net/ora/develop/pamtra-icon/

FIRST_DAY='20200615'
TODAY=`date +%Y%m%d`

declare -a hydro_combo=("all_hydro") # "no_snow" "only_snow" "only_liquid" "only_ice" "only_graupel_hail")
declare -a radar_names=("Joyrad94") # "Joyrad10" "Joyrad35" "Grarad94"

#python plot_rad94_awipev.py -s ${PLOT_PATH}/all_hydro/${DAY}all_hydropamtra94nya.png -r 
#${DATA_PATH}/all_hydro/${DAY}_r600_f2km_all_hydro_mom_Joyrad94.nc 
#-p ${DATA_PATH}${DAY}_r600_f2km_joy94_passive89.nc

#python run_pamtra.py -i ${ICON_PATH}${DAY}_r600m_f2km/METEOGRAM_patch001_${DAY}_awipev.nc -r Joyrad94 -df SB062mom -hy all_hydro -np 4 -sp 
#${DATA_PATH}all_hydro/${DAY}_r600_f2km_all_hydro_mom_Joyrad94.nc



newdata=1
DAY=$FIRST_DAY
echo $DAY $TODAY
until [[ ${DAY} > ${TODAY} ]]; do
	# Check if there is ICON output
	ICON_file=${ICON_PATH}${DAY}_r600m_f2km/METEOGRAM_patch001_${DAY}_awipev.nc
	if [ -f ${ICON_file} ]; then
		echo ${DAY}
		passiveFile=${DATA_PATH}${DAY}_r600_f2km_joy94_passive89.nc
		if [ -f $passiveFile ]; then
			echo "passive "${DAY}" already done"
		else
			python3 ${CODE_PATH}run_pamtra.py -i ${ICON_file} -sp ${passiveFile} -hy all_hydro -r joy94_passive89 -np ${NP} > ${CODE_PATH}pamtra${DAY}_passive.out
			newdata=1
		fi
		for hydro in "${hydro_combo[@]}"; do
			for radar in "${radar_names[@]}"; do
				radarFile=${DATA_PATH}${hydro}/${DAY}_r600_f2km_all_hydro_mom_${radar}.nc
				if [ -f ${radarFile}  ]; then
					echo "Already processed " ${DAY} ${hydro} ${radar}
				else
					echo "Running "${DAY} ${hydro} ${radar}
					python3 ${CODE_PATH}run_pamtra.py -i ${ICON_file} -sp ${radarFile} -hy ${hydro} -r ${radar} -np ${NP} > ${CODE_PATH}pamtra${DAY}_${hydro}_${radar}.out
					newdata=1
				fi
			done
			if [ "$newdata" -eq "1" ]; then
				plotFile=${PLOT_PATH}/all_hydro/${DAY}all_hydropamtra94nya.png
				echo "Newdata ... plotting"
				python2 plot_rad94_awipev.py -s ${plotFile} -r ${radarFile} -p ${passiveFile}
				newdata=0
			fi
		done
	else
		echo "no ICON data for "${DAY}
	fi
	DAY=$(date -d "$DAY + 1 day" +%Y%m%d)
done
