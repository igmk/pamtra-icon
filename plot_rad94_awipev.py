# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:34:01 2017

@author: dori
"""

import netCDF4 as nc
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
#from radar_settings import radarlib, hydrodict

#############################################
# Particular colormap from Lukas
colors1 = plt.cm.cool(np.linspace(1, 0, 60))
colors2 = plt.cm.winter(np.linspace(1, 0, 30))
colors3 = plt.cm.autumn(np.linspace(1, 0, 30))
colors = np.vstack((colors1, colors2, colors3))
Vm_Colormap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
#############################################

parser =  argparse.ArgumentParser(description='do plots for QuickLookBrowser')
parser.add_argument('-r', '--radar', default=None, help='Fullpath of the radar 94GHz pamtra simulation file')
parser.add_argument('-p', '--passive', default=None, help='Fullpath of the passive 89GHz pamtra simulation file')
parser.add_argument('-s', '--save', default='dummy.png', help='Fullpath of image to save')

if not len(argv)-1:
    parser.print_help()
    exit()
args = parser.parse_args()

runFile94 = args.radar
passive89file = args.passive
savefigure = args.save
print runFile94, passive89file, savefigure

# Define Plotting Function
def plot_variable(x, y, v, axes, fig=None,
                  xlab=None, ylab=None, vlab=None, title=None,
                  vmin=None, vmax=None, xlim=None, ylim=None,
                  cmap='jet'):
    mesh = axes.pcolormesh(x, y, v, vmin=vmin, vmax=vmax, cmap=cmap)
    if title is not None:
        axes.text(0.1,0.9,title,transform=axes.transAxes,weight='black',
                  bbox=dict(facecolor='white'))
    #####################################
    box = axes.get_position()
    pad, width = 0.01, 0.02
    if fig is None:
        fig = plt.gcf()
    cax = fig.add_axes([box.xmax + pad, box.ymin, width, box.height])
    plt.colorbar(mesh, cax=cax, label=vlab)
    #plt.colorbar(mesh,label=vlab,ax=axes)
    ######################################
    if xlab is not None:
        axes.set_xlabel(xlab)
    if ylab is not None:
        axes.set_ylabel(ylab)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)

versus = -1 # Top Down
versus =  1 # Bottom Up

xfmt = md.DateFormatter('%m-%d %H')
ylim=(0, 12)
xDataLim = -1
figsize41=(12.0, 15.0) # From Lukas'script
figsize31=(18, 18)
figsize21=(18, 12)

def readPamtra_nc(ncfile):
    runDataset = Dataset(ncfile)
    runVars = runDataset.variables
    H = (runVars['height'][:,0,:])[:xDataLim,:]
    ttt = pd.to_datetime(runVars['datatime'][:,0],unit='s')
    tt = (np.tile(ttt,(H.shape[1],1)).T)[:xDataLim,:]
    print(tt.shape, H.shape)
    a = 2.0*(runVars['Attenuation_Hydrometeors'][:,0,:,0,0] + runVars['Attenuation_Atmosphere'][:,0,:,0])
    A = a[:,::versus].cumsum(axis=1)[:,::versus][:xDataLim,:]
    Ze = runVars['Ze'][:,0,:,0,0,0][:xDataLim,:]
    MDV = -runVars['Radar_MeanDopplerVel'][:,0,:,0,0,0][:xDataLim,:]
    SW = runVars['Radar_SpectrumWidth'][:,0,:,0,0,0][:xDataLim,:]
    return H, tt, A, Ze, MDV, SW

f,(ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=figsize41)

if runFile94 is not None:
    # make attenuated Z
    Hw, ttw, Aw, Zew, MDVw, SWw = readPamtra_nc(runFile94)
    Zw = Zew - Aw

    # Plots
    plot_variable(ttw, 1.0e-3*Hw, Zw, ax1, f,
              None, 'height [km]', 'dBZ',
              'W-band Z attenuated', -40, 10, ylim=ylim)
    plot_variable(ttw, 1.0e-3*Hw, MDVw, ax2, f,
              None, 'height [km]', 'm/s',
              'W-band MDV', -6, 2, ylim=ylim,
              cmap=Vm_Colormap)
    plot_variable(ttw, 1.0e-3*Hw, SWw, ax3, f,
              None, 'height [km]', 'm/s',
              'W-band SW', 0, 1.5, ylim=ylim)

if passive89file is not None:
    # Load 89GHz passive channel and plot
    pamtrafile = Dataset(passive89file)
    datavars = pamtrafile.variables
    datadims = pamtrafile.dimensions
    datetime = nc.num2date(datavars['datatime'][:],
                           datavars['datatime'].units)
    timestamp = nc.date2num(datetime, 'seconds since 1970-01-01 00:00:00')
    tb = datavars['tb'][:,0,1,31,:,0] # downwelling at 0 meters

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

    plot_one_frequency(ax4, datetime, tb[:,0], str(datavars['frequency'][0] )+'GHz')

#####################################

ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax3.xaxis.set_major_formatter(xfmt)
ax4.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
ax3.grid(color='k')
ax4.grid(color='k')

ax4.set_ylabel('Tb [K]   89 GHz')

#f.tight_layout(pad=0)
f.savefig(savefigure)
#print(savefigure)
plt.close('all')
