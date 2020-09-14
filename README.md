# pamtra-icon
Set of routines and libraries to run pamtra over ICON meteogram output  
Should work on both python2 and python3 (yes pamtra works on py3 now!!)

It is assumed that you have succesfully installed pamtra https://github.com/igmk/pamtra

## forward simulation
The main file is run_pamtra.py, run
```
  python run_pamtra.py -h
```
for a list of the available options

An example on how to use it to simulate awipev Joyrad94 assuming SB06 2mom scheme
```
  python run_pamtra.py -i <full_path_to_icon_meteogram>  
                       -r <Joyrad94/joy94_passive89>
                       -df SB062mom  
                       -hy all_hydro  
                       -sp  <outputfile.nc>
                       -np 4  
                       -set '{"pyVerbose":1}' # skip this if you do not want to see the simulation progress
```
The script must be run with -r Joyrad94 option for the radar output and with -r joy94_passive89 for the passive output. It is possible to skip the passive part, if both are needed remember to save into different outputfiles

## Plotting routines
The scripts whose name begin with 'plot_' are plotting routines specifically designed to match certain colorschemes and figuresizes.  
As an example to reproduce the plots from the awipev station do
```
  python plot_rad94_awipev.py -s <full/path/figurename.png>  
                              -r <pamtra_output_radar.nc>
                              -p <pamtra_output_passive.nc>
```
All arguments are optional. The default figure name is dummy.png  
If either the radar or the passive (or both!!) files are not provided the corresponding subplots will be left empty

## Rest of the library
The other files contain libraries of options that enable the user to deal with different ICON or measurement settings
