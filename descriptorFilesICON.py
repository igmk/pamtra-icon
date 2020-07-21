import numpy as np

descriptorFile2mom = np.array([
      # ['hydro_name' 'as_ratio' 'liq_ice' 'rho_ms' 'a_ms' 'b_ms' 'alpha_as' 'beta_as' 'moment_in' 'nbin' 'dist_name' 'p_1' 'p_2' 'p_3' 'p_4' 'd_1' 'd_2' 'scat_name' 'vel_size_mod' 'canting']
       ('cwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 13, 100, 'mgamma', -99.0, -99.0,   2.0,    1.0,   2.0e-6,   8.0e-5, 'mie-sphere',                     'corPowerLaw_24388657.6_2.0', -99.0),
       ('iwc_q', 1.0, -1, -99.0, 1.58783,  2.56,  0.684,   2.0, 13, 100, 'mgamma', -99.0, -99.0, 1.564, 0.8547, 1.744e-5, 9.369e-3, 'ssrg-rt3_0.18_0.89_2.06_0.08',   'corPowerLaw_30.606_0.5533',  -99.0),
       #('rwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 13, 100, 'mgamma', -99.0, -99.0,   2.0,    1.0,  0.00012,   8.2e-3, 'mie-sphere',                     'corAtlas_9.292_9.623_622.2',  -99.0),
	   ('rwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 13, 100, 'mgamma', -99.0, -99.0,   2.0,    1.0,  0.00012,   8.2e-3, 'mie-sphere',                     'corAtlas_9.292_9.292_622.2',  -99.0),
       ('swc_q', 0.6, -1, -99.0,   0.038,   2.0, 0.3971,  1.88, 13, 100, 'mgamma', -99.0, -99.0,   1.0,    1.0,  5.13e-5, 2.294e-2, 'ssrg-rt3_0.25_1.00_1.66_0.04',   'corPowerLaw_5.511054_0.25',  -99.0),
       ('gwc_q', 1.0, -1, -99.0,  500.86,  3.18,  -99.0, -99.0, 13, 100, 'mgamma', -99.0, -99.0,  5.37,   1.06,  2.11e-4,   1.3e-2, 'mie-sphere',                     'corPowerLaw_406.67_0.85',    -99.0), 
       ('hwc_q', 1.0, -1, -99.0,  392.33,   3.0,  -99.0, -99.0, 13, 100, 'mgamma', -99.0, -99.0,   5.0,    1.0,  1.87e-4,   1.1e-2, 'mie-sphere',                     'corPowerLaw_106.33_0.5',     -99.0)],
      dtype=[('hydro_name', 'S15'), ('as_ratio', '<f8'), ('liq_ice', '<i8'), ('rho_ms', '<f8'), ('a_ms', '<f8'), ('b_ms', '<f8'), ('alpha_as', '<f8'), ('beta_as', '<f8'), ('moment_in', '<i8'), ('nbin', '<i8'), ('dist_name', 'S15'), ('p_1', '<f8'), ('p_2', '<f8'), ('p_3', '<f8'), ('p_4', '<f8'), ('d_1', '<f8'), ('d_2', '<f8'), ('scat_name', 'S30'), ('vel_size_mod', 'S30'), ('canting', '<f8')]
      )

descriptorFile1mom = np.array([ # TODO to be reviewed, coefficients for m-D and v-D are changing
  #['hydro_name' 'as_ratio' 'liq_ice' 'rho_ms' 'a_ms' 'b_ms' 'alpha_as' 'beta_as' 'moment_in' 'nbin' 'dist_name' 'p_1' 'p_2' 'p_3' 'p_4' 'd_1' 'd_2' 'scat_name' 'vel_size_mod' 'canting']
   ('cwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0,  3,  1,   'mono',           -99.0, -99.0, -99.0, -99.0,  2.0e-5,  -99.0, 'mie-sphere', 'corPowerLaw_24388657.6_2.0', -99.0),
   ('iwc_q', 0.2, -1, -99.0,   130.0,   3.0,  0.684,   2.0,  3,  1,   'mono_cosmo_ice', -99.0, -99.0, -99.0, -99.0,   -99.0,  -99.0, 'ssrg-rt3_0.18_0.89_2.06_0.08', 'corPowerLaw_30.606_0.5533', -99.0),
   ('rwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0,  3,  100, 'exp',            -99.0, -99.0, 8.0e6, -99.0,  1.2e-4, 6.0e-3, 'mie-sphere', 'corPowerLaw_130.0_0.5', -99.0),
   ('swc_q', 0.6, -1, -99.0,   0.038,   2.0, 0.3971,  1.88,  3,  100, 'exp_cosmo_snow', -99.0, -99.0, -99.0, -99.0, 5.1e-11, 1.0e-2, 'ssrg-rt3_0.25_1.00_1.66_0.04', 'corPowerLaw_4.9_0.25', -99.0),
   ('gwc_q', 1.0, -1, -99.0,   169.6,   3.1,  -99.0, -99.0,  3,  100, 'exp',            -99.0, -99.0, 4.0e6, -99.0, 1.0e-10, 1.0e-2, 'mie-sphere', 'corPowerLaw_406.67_0.85', -99.0)],
  dtype=[('hydro_name', 'S15'), ('as_ratio', '<f8'), ('liq_ice', '<i8'), ('rho_ms', '<f8'), ('a_ms', '<f8'), ('b_ms', '<f8'), ('alpha_as', '<f8'), ('beta_as', '<f8'), ('moment_in', '<i8'), ('nbin', '<i8'), ('dist_name', 'S15'), ('p_1', '<f8'), ('p_2', '<f8'), ('p_3', '<f8'), ('p_4', '<f8'), ('d_1', '<f8'), ('d_2', '<f8'), ('scat_name', 'S20'), ('vel_size_mod', 'S30'), ('canting', '<f8')]
  )

descFilesLib = { 'SB061mom':descriptorFile1mom,
			     'SB062mom':descriptorFile2mom}
