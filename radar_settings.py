# DEFINE LIBRARY OF RADAR PROPRTIES
KiXPolnml = {'radar_fwhr_beamwidth_deg':1.3,
             'radar_integration_time':1.0,
             'radar_k2':0.93,
             'radar_max_v':9.0,
             'radar_min_v':-9.0,
             'radar_nfft':1200,
             'radar_no_ave':1,
             'radar_pnoise0':-29.7,
             'radar_peak_min_snr': 3,
             'frequency':9.4}

Joyrad94nml = {'radar_fwhr_beamwidth_deg':0.5,
               'radar_integration_time':1.0,
               'radar_k2':0.93,
               'radar_max_v':6.8,
               'radar_min_v':-6.8,
               'radar_nfft':512,
               'radar_no_ave':17,
               'radar_pnoise0':-54, # -29.5
               'radar_peak_min_snr': -15,
               'frequency':94.0}

Joyrad10nml = {'radar_fwhr_beamwidth_deg':1.0,
               'radar_integration_time':2.0,
               'radar_k2':0.93,
               'radar_max_v':78.07291,
               'radar_min_v':-78.07291,
               'radar_nfft':4096,
               'radar_no_ave':10,
               'radar_pnoise0':-11.9,#-48.0,
               'frequency':9.6}

Joyrad35nml = {'radar_fwhr_beamwidth_deg':0.6,
               'radar_integration_time':2.0,
               'radar_k2':0.93,
               'radar_max_v':10.56824,
               'radar_min_v':-10.56824,
               'radar_nfft':512,
               'radar_pnoise0':-38.4,#-64.0,
               'radar_no_ave':20,
               'radar_peak_min_snr':-10,
               'frequency':35.5}

Grarad94nml = {'radar_fwhr_beamwidth_deg':0.5,
               'radar_integration_time':1.0,
               'radar_k2':0.93,
               'radar_max_v':6.8,
               'radar_min_v':-6.8,
               'radar_nfft':512,
               'radar_no_ave':17,
               'radar_pnoise0':-35.0,#-54.0, !-17.3!
#               'radar_peak_min_snr': 10,
               'frequency':94.0}

Default = {}

radarlib = {'Joyrad10':Joyrad10nml, 'Joyrad35':Joyrad35nml, \
            'Grarad94':Grarad94nml, 'KiXPol':KiXPolnml, \
            'Joyrad94':Joyrad94nml, 'Default':Default, \
            'hatpro':Default, 'joy94_passive89':Default}

# DEFINE DICTIONARY OF HYDROMETOR CONTENT COMBINATIONS
hydrodict = {'all_hydro'        :[1.,1.,1.,1.,1.,1.],
             'no_snow'          :[1.,1.,1.,0.,1.,1.],
             'only_snow'        :[0.,0.,0.,1.,0.,0.],
             'only_ice'         :[0.,1.,0.,0.,0.,0.],
             'only_liquid'      :[1.,0.,1.,0.,0.,0.],
             'only_graupel_hail':[0.,0.,0.,0.,1.,1.]}
