from __future__ import print_function
import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
plt.close('all')
import matplotlib.dates as md
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from glob import glob
import os
import argparse
from sys import argv

parser =  argparse.ArgumentParser(description='do plots for QuickLookBrowser')
parser.add_argument('-i', '--icon', default=None, help='Fullpath of the icon meteogram simulation file')
parser.add_argument('-p', '--passive', default=None, help='Fullpath of the passive 89GHz pamtra simulation file')
parser.add_argument('-s', '--save', default='dummy.png', help='Fullpath of image to save')

if not len(argv)-1:
    parser.print_help()
    exit()
args = parser.parse_args()

ICON = args.icon
passiveFile = args.passive
savefigure = args.save
print(ICON, passiveFile, savefigure)

xfmt = md.DateFormatter('%H')
plt.close('all')

iconfile = netCDF4.Dataset(ICON)
iconvars = iconfile.variables
QV = iconvars['QV_S'][:]
P = iconvars['P_SFC'][:]
T2 = iconvars['T2M'][:]
T2D = iconvars['TD2M'][:]
icon_times = netCDF4.num2date(iconvars["time"][:],iconvars["time"].units) # datetime autoconversion

pamtrafile = netCDF4.Dataset(passiveFile)
datavars = pamtrafile.variables
datadims = pamtrafile.dimensions
datetime = netCDF4.num2date(datavars['datatime'][:],
                            datavars['datatime'].units)
timestamp = netCDF4.date2num(datetime, 'seconds since 1970-01-01 00:00:00')
tb = datavars['tb'][:,0,1,31,:,0] # downwelling at 0 meters

print(timestamp.shape, tb.shape)

def plot_one_frequency(ax, time, tb, frequency, noxtick=True, mean=True, color='k', ylim=None):
    ax.plot(time, tb,'k')
    ax.plot(time, tb.mean()*np.ones(time.shape), 'k', ls=':')
    if mean:
	    ax.text(0.9, 0.8, str(tb.mean())+' K' ,
	                  horizontalalignment='center',
	                  verticalalignment='center',
	                  color='red',
	                  transform=ax.transAxes)
    ax.text(0.1, 0.8, frequency,
                  horizontalalignment='center',
                  verticalalignment='center',
                  color='red',
                  transform=ax.transAxes)
    ax.set_xlim([min(time), max(time)])
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.xaxis.set_major_formatter(xfmt)
    if noxtick:
        ax.set_xticklabels([])

def Td2RH(Td,T):
	L = 2.501e6
	Rw = 461.5
	return 100.0*np.exp(-L*(T-Td)/(Rw*T*Td))

f, axs = plt.subplots(8, 2, sharex=False, figsize=(9,7),
                      gridspec_kw = {'hspace':0.1})
plot_one_frequency(axs[0,0], icon_times, Td2RH(T2D, T2), 'RH   [%]', False, False, ylim=[0,100])
plot_one_frequency(axs[0,1], icon_times, T2, '             Temperature   [K]', False, False)

plot_one_frequency(axs[1,0], datetime, tb[:,0], str(datavars['frequency'][0] )+'GHz')
plot_one_frequency(axs[2,0], datetime, tb[:,1], str(datavars['frequency'][1] )+'GHz')
plot_one_frequency(axs[3,0], datetime, tb[:,2], str(datavars['frequency'][2] )+'GHz')
plot_one_frequency(axs[4,0], datetime, tb[:,3], str(datavars['frequency'][3] )+'GHz')
plot_one_frequency(axs[5,0], datetime, tb[:,4], str(datavars['frequency'][4] )+'GHz')
plot_one_frequency(axs[6,0], datetime, tb[:,5], str(datavars['frequency'][5] )+'GHz')
plot_one_frequency(axs[7,0], datetime, tb[:,6], str(datavars['frequency'][6] )+'GHz',False)
plot_one_frequency(axs[1,1], datetime, tb[:,7], str(datavars['frequency'][7] )+'GHz')
plot_one_frequency(axs[2,1], datetime, tb[:,8], str(datavars['frequency'][8] )+'GHz')
plot_one_frequency(axs[3,1], datetime, tb[:,9], str(datavars['frequency'][9] )+'GHz')
plot_one_frequency(axs[4,1], datetime, tb[:,10],str(datavars['frequency'][10])+'GHz')
plot_one_frequency(axs[5,1], datetime, tb[:,11],str(datavars['frequency'][11])+'GHz')
plot_one_frequency(axs[6,1], datetime, tb[:,12],str(datavars['frequency'][12])+'GHz')
plot_one_frequency(axs[7,1], datetime, tb[:,13],str(datavars['frequency'][13])+'GHz',False)
#f.tight_layout(pad=0)
f.savefig(savefigure, dpi=200, bbox_inches='tight')
plt.close('all')
