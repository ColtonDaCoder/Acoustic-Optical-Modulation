import numpy as np
import json
import math
import jcmwave,time,imp,shutil,os 

aoi = 20
wvl = 200

output_file = "20AOI.json"

jcmwave.set_num_threads(10)
        
keys = {
    'AOI': aoi,
    'vacuum_wavelength': wvl*1e-9,
    'uol': 1e-9,
    'display_triangulation' : 'no',
    'boundary' : 'Periodic',
    'info_level' : -1,
    'fem_degree' : 3,
    'n_refinement_steps' : 0, # Currently we get non-physical results if this is >0
    }
 
#print('Wavelength : %3.2f nm' % (keys['vacuum_wavelength']*1e9))
for i in range(30):
    air_id = "n_"+str(i)
    val = 1
    keys[air_id] = val

keys['sm_filename'] = '"'+'project_results/sm.jcm"'
jcmwave.jcmt2jcm('boundary_conditions.jcmt', keys)
jcmwave.jcmt2jcm('materials.jcmt', keys)
jcmwave.jcmt2jcm('project.jcmpt', keys)
jcmwave.jcmt2jcm('sources.jcmt', keys)
jcmwave.jcmt2jcm('layout.jcmt', keys)
jcmwave.solve('project.jcmp')

# Gather Reflected Fourier Modes (Z)
filename_fourierModes_r = './project_results/fourier_modes_r.jcm';
fourierModes_r = jcmwave.loadtable(filename_fourierModes_r,format='named')
powerFlux_r = jcmwave.convert2powerflux(fourierModes_r)

reflection_list = []
total_P_s_r = np.real(powerFlux_r['PowerFluxDensity'][0][:,2])
total_P_p_r = np.real(powerFlux_r['PowerFluxDensity'][1][:,2])

# Reflected flux in normal direction
for order in range(len(powerFlux_r['PowerFluxDensity'][0])):
    orders_list = [str(fourierModes_r['N1'][order]), str(fourierModes_r['N2'][order])]
    P_s_r = total_P_s_r[order]
    P_p_r = total_P_s_r[order]
    reflection_list.append([orders_list, [P_s_r, P_p_r]])

with open('saved.json','w') as f:
    json.dump(reflection_list, f)

	    

