# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:34:01 2017

@author: dori
"""
from __future__ import print_function
from netCDF4 import Dataset
import matplotlib.pyplot as plt
plt.close('all')
import matplotlib.dates as md
import numpy as np
import pandas as pd
from glob import glob
import os
import argparse
from sys import argv
from radar_settings import radarlib, hydrodict

parser =  argparse.ArgumentParser(description='do plots for QuickLookBrowser')
parser.add_argument('-rx', '--radarX',
                    help='gimme full path for X-band radar')
parser.add_argument('-rk', '--radarK',
                    help='gimme full path for Ka-band radar')
parser.add_argument('-rw', '--radarW',
                    help='gimme full path for W-band radar')
parser.add_argument('-s', '--save',
                    help='gimme full path for saving output root')
#parser.add_argument('-m1', '--moment1', nargs=1, help='tell me the modifier to data and plot folders')
#parser.add_argument('-p', '--patch', nargs=1, help='tell me the 3 padded patch number like 001')
if not len(argv)-1:
    parser.print_help()
    exit()

args = parser.parse_args()
#datestr = args.date[0]
#hydrostr = args.hydroset[0]
#print(datestr, hydrostr)

plt.close('all')

#rootpath = '/data/optimice/pamtra_runs/tripex-pol/'
#if args.rootpath is not None:
#    rootpath = args.rootpath[0]
#mod=''
#if args.moment1 is not None:
#    mod =  args.moment1[0]

#patch = ''
#if args.patch is not None:
#    patch = args.patch[0]

#runFld = rootpath + 'data' + mod + '/'
#plotFld = rootpath + 'plots' + mod + '/'

#runs = ['all_hydro', 'no_snow', 'only_ice', 'only_liquid', 'only_snow', 'only_graupel_hail']
#titles = ['all Hydrometeors', 'No Snow', 'Only Ice', 'Only liquid (cloud drops and rain)', 'only Snow', 'only Graupel and Hail']
#runTitles=dict(zip(runs,titles))

# Define Plotting Function
def plot_variable(x,y,v,axes,
                  xlab=None,ylab=None,vlab=None,title=None,
                  vmin=None,vmax=None,xlim=None,ylim=None,
                  cmap='jet'):
    mesh = axes.pcolormesh(x,y,v,vmin=vmin,vmax=vmax,cmap=cmap)
    if title is not None:
        axes.text(0.1,0.9,title,transform=axes.transAxes,weight='black',
                  bbox=dict(facecolor='white'))
    plt.colorbar(mesh,label=vlab,ax=axes)
    if xlab is not None:
        axes.set_xlabel(xlab)
    if ylab is not None:
        axes.set_ylabel(ylab)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)

versus = -1 # Top Down
versus =  1 # Bottom Up

xfmt = md.DateFormatter('%m-%d %H')
ylim=(0,12000)
xDataLim = -1
figsize31=(18,18)
figsize21=(18,12)

# Open the netcdf results file
runFile10 = args.radarX#runFld + hydrostr + '/' + datestr + hydrostr + patch + '_mom_'+'Joyrad10.nc'
runFile35 = args.radarK#runFld + hydrostr + '/' + datestr + hydrostr + patch + '_mom_'+'Joyrad35.nc'
runFile94 = args.radarW#runFld + hydrostr + '/' + datestr + hydrostr + patch + '_mom_'+'Grarad94.nc'

#if int(datestr) < 20180930:
#    runFile10 = runFld + hydrostr + '/' + datestr + hydrostr + '_mom_'+'KiXPol.nc'
#    runFile35 = runFld + hydrostr + '/' + datestr + hydrostr + '_mom_'+'Joyrad35.nc'
#    runFile94 = runFld + hydrostr + '/' + datestr + hydrostr + '_mom_'+'Joyrad94.nc'


print(runFile10)
print(runFile35)
print(runFile94)

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

from os import path
if path.exists(runFile10):
  print('exists '+ runFile10)
else:
  print('Noooooooooooooooooooooooooo')

Hx, ttx, Ax, Zex, MDVx, SWx = readPamtra_nc(runFile10)
Ha, tta, Aa, Zea, MDVa, SWa = readPamtra_nc(runFile35)
Hw, ttw, Aw, Zew, MDVw, SWw = readPamtra_nc(runFile94)

# Plot Attenuation   
f,((ax1,ax2,ax3)) = plt.subplots(3, 1, sharex=False, figsize=figsize31)
plot_variable(ttx,Hx,Ax,ax1,None,'height [km]','dB','X-band 2-way Attenuation',0,1,ylim=ylim)
plot_variable(tta,Ha,Aa,ax2,None,'height [km]','dB','Ka-band 2-way Attenuation',0,5,ylim=ylim)
plot_variable(ttw,Hw,Aw,ax3,'time','height [km]','dB', 'W-band 2-way Attenuation',0,15,ylim=ylim)
#f.suptitle(runTitles[hydrostr], weight='black',bbox=dict(facecolor='white'))
ax1.set_title('X-band')
ax2.set_title('Ka-band')
ax3.set_title('W-band')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax3.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
ax3.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_attenuation'+'.png', dpi=200, bbox_inches='tight')

# Plot Ze
f,((ax1,ax2,ax3)) = plt.subplots(3,1,sharex=False,figsize=figsize31)
plot_variable(ttx,Hx,Zex,ax1,None,'height [km]','dBZ','X-band Ze',-35,25,ylim=ylim)
plot_variable(tta,Ha,Zea,ax2,None,'height [km]','dBZ', 'Ka-band Ze',-35,25,ylim=ylim)
plot_variable(ttw,Hw,Zew,ax3,'time','height [km]','dBZ', 'W-band Ze',-35,25,ylim=ylim)
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax3.xaxis.set_major_formatter(xfmt)
ax1.set_title('X-band')
ax2.set_title('Ka-band')
ax3.set_title('W-band')
ax1.grid(color='k')
ax2.grid(color='k')
ax3.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_Ze'+'.png', dpi=200, bbox_inches='tight')

# make DWRs and plot
DWRxa = Zex-Zea
DWRaw = Zea-Zew
f,((ax1,ax2)) = plt.subplots(2,1,sharex=False,figsize=figsize21)
plot_variable(ttx,Hx,DWRxa,ax1,None,'height [km]','dB','DWR$_{X Ka}$',-5,20, ylim=ylim,cmap='nipy_spectral')
plot_variable(ttx,Hx,DWRaw,ax2,'time','height [km]','dB','DWR$_{Ka W}$',-5,20, ylim=ylim,cmap='nipy_spectral')
#f.suptitle(runTitles[hydrostr], weight='black',bbox=dict(facecolor='white'))
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax1.set_title('X-Ka')
ax2.set_title('Ka-W')
ax1.grid(color='k')
ax2.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_DWRe'+'.png', dpi=200, bbox_inches='tight')

# make attenuated Z and DWRs and respective plots
Zx = Zex-Ax
Za = Zea-Aa
Zw = Zew-Aw
f,((ax1,ax2,ax3)) = plt.subplots(3,1,sharex=False,figsize=figsize31)
plot_variable(ttx,Hx,Zx,ax1,None,'height [km]','dBZ','X-band Z attenuated',-35,25,ylim=ylim)
plot_variable(tta,Ha,Za,ax2,None,'height [km]','dBZ','Ka-band Z attenuated',-35,25,ylim=ylim)
plot_variable(ttw,Hw,Zw,ax3,'time','height [km]','dBZ', 'W-band Z attenuated',-35,25,ylim=ylim)
ax1.set_title('X-band')
ax2.set_title('Ka-band')
ax3.set_title('W-band')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax3.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
ax3.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_Zattenuated'+'.png', dpi=200, bbox_inches='tight')

DWRxa = Zx-Za
DWRaw = Za-Zw
f,((ax1,ax2)) = plt.subplots(2,1,sharex=False,figsize=figsize21)
plot_variable(ttx,Hx,DWRxa,ax1,None,'height [km]','dB','DWR$_{X Ka}$ attenuated',-5,20,ylim=ylim,cmap='nipy_spectral')    
plot_variable(ttx,Hx,DWRaw,ax2,'time','height [km]','dB','DWR$_{Ka W}$ attenuated',-5,20,ylim=ylim,cmap='nipy_spectral')
ax1.set_title('X-Ka')
ax2.set_title('Ka-W')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_DWRattenuated'+'.png', dpi=200, bbox_inches='tight')

# Plot mean doppler velocity
f,((ax1,ax2,ax3)) = plt.subplots(3,1,sharex=False,figsize=figsize31)
plot_variable(ttx,Hx,MDVx,ax1,None,  'height [km]','m/s',' X-band MDV',-3,0,ylim=ylim)
plot_variable(tta,Ha,MDVa,ax2,None,  'height [km]','m/s','Ka-band MDV',-3,0,ylim=ylim)
plot_variable(ttw,Hw,MDVw,ax3,'time','height [km]','m/s', 'W-band MDV',-3,0,ylim=ylim)
ax1.set_title('X-band')
ax2.set_title('Ka-band')
ax3.set_title('W-band')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax3.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
ax3.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_MDV'+'.png', dpi=200, bbox_inches='tight')

f,((ax1,ax2,ax3)) = plt.subplots(3,1,sharex=False,figsize=figsize31)
plot_variable(ttx,Hx,SWx,ax1,None,  'height [km]','m/s','Ku-band SW',0,1,ylim=ylim)
plot_variable(tta,Ha,SWa,ax2,None,  'height [km]','m/s','Ka-band SW',0,1,ylim=ylim)
plot_variable(ttw,Hw,SWw,ax3,'time','height [km]','m/s', 'W-band SW',0,1,ylim=ylim)
ax1.set_title('X-band')
ax2.set_title('Ka-band')
ax3.set_title('W-band')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax3.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
ax3.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_SW'+'.png', dpi=200, bbox_inches='tight')

# Plot dual doppler velocity
DDWxa = MDVx-MDVa
DDWaw = MDVa-MDVw
f,((ax1,ax2)) = plt.subplots(2,1,sharex=False,figsize=figsize21)
plot_variable(ttx,Hx,DDWxa,ax1,None,'height [km]','m/s','DDV$_{X Ka}$',-0.3,0.3,ylim=ylim,cmap='nipy_spectral')
plot_variable(ttx,Hx,DDWaw,ax2,'time','height [km]','m/s','DDV$_{Ka W}$',-0.3,0.3,ylim=ylim,cmap='nipy_spectral')
ax1.set_title('X-Ka')
ax2.set_title('Ka-W')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
ax1.grid(color='k')
ax2.grid(color='k')
f.tight_layout(pad=0)
f.savefig(args.save+'_DDV'+'.png', dpi=200, bbox_inches='tight')

# Plot dual spectral width
DSWxa = SWx-SWa
DSWaw = SWa-SWw
f,((ax1,ax2)) = plt.subplots(2,1,sharex=False,figsize=figsize21)
plot_variable(ttx,Hx,DSWxa,ax1,None,'height [km]','m/s','DSW$_{X Ka}$',-0.3,0.3,ylim=ylim,cmap='nipy_spectral')
plot_variable(ttx,Hx,DSWaw,ax2,'time','height [km]','m/s','DSW$_{Ka W}$',-0.3,0.3,ylim=ylim,cmap='nipy_spectral')
ax1.set_title('X-Ka')
ax2.set_title('Ka-W')
ax1.grid(color='k')
ax2.grid(color='k')
ax1.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_formatter(xfmt)
f.tight_layout(pad=0)
f.savefig(args.save+'_DSW'+'.png', dpi=200, bbox_inches='tight')

plt.close('all')
