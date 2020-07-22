from __future__ import division
from sys import argv

#################################################
# temporary workaround issue #24
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
#################################################

import pyPamtra
import numpy as np
import argparse
from radar_settings import radarlib
from radar_settings import hydrodict
from descriptorFilesICON import descFilesLib

parser =  argparse.ArgumentParser(description='do plots for QuickLookBrowser')

parser.add_argument('-i','--icon',
	                help='gimme the full path to ICON meteogram file')

parser.add_argument('-r','--radarset', default='Joyrad10',
	                help='gimme radar name I will look in my library to setup the paramenters',
	                choices=radarlib.keys())

parser.add_argument('-df','--descriptorfile', default='SB062mom',
				    help='gimme the name of the descriptorfile, I will infer if it is 1 or 2 moment from the name',
				    choices=descFilesLib.keys())

parser.add_argument('-hy','--hydroset', default='all_hydro',
	                help='gimme hydrosettings I will look into my library to switch on and off hydrometeor content accordingly',
	                choices=hydrodict.keys())

parser.add_argument('-sp','--savepath', default='./',
	                help='gimme fulldatapath for saving output')

parser.add_argument('-np', '--numproc', type=int, default=2,
					help='gimme the number of processors I can use default = 2')

parser.add_argument('-ti', '--timeidx', type=str, default='None',
				    help='python string to be evaluated into range of time indexces to slice the input')

parser.add_argument('-nml', '--pam_nmlSet', type=str, default='None',
				    help='python dictionary to be evaluated to overwrite pam.nmlSet')

parser.add_argument('-set', '--pam_set', type=str, default='None',
				    help='python dictionary to be evaluated to overwrite pam.set')

parser.add_argument('-p', '--pam_p', type=str, default='None',
				    help='python dictionary to be evaluated to overwrite pam.p')


def overwrite_pam(pam, p, Set, nmlSet):
	if p is not None:
		for k in p.keys():
			pam.p[k] = p[k]
	if Set is not None:
		for k in Set.keys():
			pam.set[k] = Set[k]
	if nmlSet is not None:
		for k in nmlSet.keys():
			pam.nmlSet[k] = nmlSet[k]
	return pam


if not len(argv)-1:
	parser.print_help()
	exit()
args = parser.parse_args()

timeidx = eval(args.timeidx)
forceP = eval(args.pam_p)
forceSet = eval(args.pam_set)
forceNmlSet = eval(args.pam_nmlSet)

radarstr = args.radarset
hydrostr = args.hydroset

cores = args.numproc
descFile = descFilesLib[args.descriptorfile]

print args

if '1mom' in args.descriptorfile:
	pam = pyPamtra.importer.readIcon1momMeteogram(args.icon,
												  descFile,
												  timeidx=timeidx,
												  hydro_content=hydrodict[hydrostr][:5])
else:
	pam = pyPamtra.importer.readIcon2momMeteogram(args.icon,
												  descFile,
												  timeidx=timeidx,
												  hydro_content=hydrodict[hydrostr])

# SETTINGS
pam.nmlSet["radar_mode"] = 'moments'
pam.set['verbose'] = 0 # set verbosity levels
pam.set['pyVerbose'] = 1 # change to 0 if you do not want to see job progress number
pam.p['turb_edr'][:] = 1.0e-4
pam.nmlSet['radar_airmotion'] = True
pam.nmlSet['radar_airmotion_vmin'] = 0.0 # workaround to potential bug in radar_spectrum
pam.nmlSet['radar_airmotion_model'] = 'constant'

def set_radar_properties(pam, radarlib, radar):
	pam.nmlSet['active'] = True
	pam.nmlSet['passive'] = False
	radarbook = radarlib[radar]
	for k in radarbook.keys():
		print k
		if 'radar' in k: # avoid to set frequency in the nmlSet
			print k, radarbook[k]
			pam.nmlSet[k] = radarbook[k]
	return pam, radarbook['frequency']

def run_radar_simulation(pam, radarname, hydroconf):
	pam, frequency = set_radar_properties(pam, radarlib, radarname)
	pam = overwrite_pam(pam, forceP, forceSet, forceNmlSet)
	pam.runParallelPamtra(np.array([frequency]), pp_deltaX=1, pp_deltaY=1, pp_deltaF=1, pp_local_workers=cores)
	pam.writeResultsToNetCDF(args.savepath+hydroconf+'_'+pam.nmlSet["radar_mode"][:3]+'_'+radarname+'.nc')
	return pam

def runPassive89(pam):
		# SETTINGS
		pam.nmlSet['active'] = False
		pam.nmlSet['passive'] = True # Passive is time consuming
		pam = overwrite_pam(pam, forceP, forceSet, forceNmlSet)
		frequencies = [89.0]
		pam.runParallelPamtra(np.array(frequencies), pp_deltaX=1, pp_deltaY=1, pp_deltaF=1, pp_local_workers=cores)
		pam.writeResultsToNetCDF(args.savepath+'joy94_passive89.nc') # SAVE OUTPUT
		return pam

# RUN PAMTRA
if (radarstr == 'joy94_passive89'):
	pam = runPassive89(pam)
else:
	pam = run_radar_simulation(pam, radarstr, hydrostr)
