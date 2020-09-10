#!/bin/bash

source /home/dori/.bashrc
export OPENBLAS_NUM_THREADS=1

NP=4

ICON_PATH=/data/inscape/icon/experiments/juelich/testbed/
ROOT_PATH=/data/optimice/pamtra_runs/tripex2/
DATA_PATH=${ROOT_PATH}data/
PLOT_PATH=${ROOT_PATH}plots/
CODE_PATH=/net/ora/develop/pamtra-icon/

FIRST_DAY='20151111'
TODAY='20160106' ##`date +%Y%m%d`

declare -a hydro_combo=("all_hydro" "no_snow" "only_snow" "only_liquid" "only_ice" "only_graupel_hail")
declare -a radar_names=("Joyrad94" "KiXPol" "Joyrad35")

newdata=0
newpassive=0
DAY=$FIRST_DAY
echo $DAY $TODAY
until [[ ${DAY} > ${TODAY} ]]; do
	# Check if there is ICON output
	ICON_file=${ICON_PATH}testbed_${DAY}/METEOGRAM_patch001_${DAY}_joyce.nc
	if [ -f ${ICON_file} ]; then
		echo ${DAY}
		passiveFile=${DATA_PATH}${DAY}hatpro.nc
		plotFile=${PLOT_PATH}${DAY}hatpro.png
		if [ -f $passiveFile ]; then
			echo "passive "${DAY}" already done"
		else
			python3 ${CODE_PATH}run_pamtra.py -i ${ICON_file} -sp ${passiveFile} -hy all_hydro -r hatpro -np ${NP} > ${CODE_PATH}pamtra${DAY}_hatpro.out
			newpassive=1
		fi
		if [ "$newpassive" -eq "1" ]; then
			python ${CODE_PATH}plot_hatpro.py -s ${plotFile} -p ${passiveFile} -i ${ICON_file}
		fi
		for hydro in "${hydro_combo[@]}"; do
			mkdir -p ${DATA_PATH}/${hydro}
			mkdir -p ${PLOT_PATH}/${hydro}
			for radar in "${radar_names[@]}"; do
				radarFile=${DATA_PATH}${hydro}/${DAY}${hydro}_mom_${radar}.nc
				if [ -f ${radarFile}  ]; then
					echo "Already processed " ${DAY} ${hydro} ${radar}
				else
					echo "Running "${DAY} ${hydro} ${radar}
					python3 ${CODE_PATH}run_pamtra.py -i ${ICON_file} -sp ${radarFile} -hy ${hydro} -r ${radar} -np ${NP} > ${CODE_PATH}pamtra${DAY}_${hydro}_${radar}.out
					newdata=1
				fi
			done
			if [ "$newdata" -eq "1" ]; then
				plotFile=${PLOT_PATH}/${hydro}/${DAY}${hydro} # plotfilename is completed by the python script, several plots are done
				echo "Newdata ... plotting"
				radarX=${DATA_PATH}${hydro}/${DAY}${hydro}_mom_KiXPol.nc
				radarK=${DATA_PATH}${hydro}/${DAY}${hydro}_mom_Joyrad35.nc
				radarW=${DATA_PATH}${hydro}/${DAY}${hydro}_mom_Joyrad94.nc
				python ${CODE_PATH}plot_tripex_radars.py -s ${plotFile} -rx ${radarX} -rk ${radarK} -rw ${radarW}
				newdata=0
			fi
		done
	else
		echo "no ICON data for "${DAY}
	fi
	DAY=$(date -d "$DAY + 1 day" +%Y%m%d)
done
