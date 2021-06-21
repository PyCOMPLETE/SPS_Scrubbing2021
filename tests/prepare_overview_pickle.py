import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

import awkward as ak

data_folder = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/'


BCT_folder = data_folder + 'BCT/'
Pressures_folder = data_folder + 'Pressures/'

all_files = os.listdir(BCT_folder)
n_files = len(all_files)

cycleStamps_list = []
integrated_intensity_list = []
max_intensity_list = []
max_pressure_MKDVB_list = []
max_pressure_10660_list = []
max_pressure_61674_list = []

for ii, parquet_filename in enumerate(all_files):
    if ii%1000 == 0:
        print(f'{ii}/{n_files}')
    #print(parquet_filename)
    if not os.path.exists(Pressures_folder + parquet_filename):
        print(f'file does not exist {Pressures_folder + parquet_filename}')
        continue
    BCT_parquet = BCT_folder + parquet_filename
    Pressures_parquet = Pressures_folder + parquet_filename

    max_intensity = ak.from_parquet(BCT_parquet,columns=['SPS.BCTDC.51454/Acquisition'])[0, 'SPS.BCTDC.51454/Acquisition','value','maximum_intensity_protons']
    integrated_intensity = ak.from_parquet(BCT_parquet,columns=['SPS.BCTDC.51454/Acquisition'])[0, 'SPS.BCTDC.51454/Acquisition','value','integrated_intensity_protons_seconds']
    #if integrated_intensity < 0.5e13:
    #    continue

    cycleStamp_ns = ak.from_parquet(BCT_parquet,columns=['SPS.BCTDC.51454/Acquisition'])[0, 'SPS.BCTDC.51454/Acquisition','header','cycleStamp']
    max_pressure_MKDVB = ak.from_parquet(Pressures_parquet,columns=['MKDVB.51698:PRESSURE'])[0, 'MKDVB.51698:PRESSURE','value','max_pressure_mbar']

    try:
        max_pressure_10660 = ak.from_parquet(Pressures_parquet,columns=['VACCMW.VGHB_10660.PR'])[0, 'VACCMW.VGHB_10660.PR','value','max_pressure_mbar']
    except:
        max_pressure_10660 = -1

    try:
        max_pressure_61674 = ak.from_parquet(Pressures_parquet,columns=['VACCMW.VGHB_61674.PR'])[0, 'VACCMW.VGHB_61674.PR','value','max_pressure_mbar']
    except:
        max_pressure_61674 = -1

    cycleStamps_list.append(cycleStamp_ns*1e-9)
    integrated_intensity_list.append(integrated_intensity)
    max_intensity_list.append(max_intensity)
    max_pressure_MKDVB_list.append(max_pressure_MKDVB)
    max_pressure_10660_list.append(max_pressure_10660)
    max_pressure_61674_list.append(max_pressure_61674)
    # if len(cycleStamps_list) > 100:
    #     break

mydict = {}
mydict['cycleStamps'] = cycleStamps_list
mydict['integrated_intensity'] = integrated_intensity_list
mydict['max_pressure_MKDVB'] = max_pressure_MKDVB_list
mydict['max_pressure_10660'] = max_pressure_10660_list
mydict['max_pressure_61674'] = max_pressure_61674_list
mydict['max_intensity'] = max_intensity_list

pickle.dump(mydict, open('overview_thursday.pkl','wb'))

