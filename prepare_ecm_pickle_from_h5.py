import sys
import datascout
import pickle
import os
from tqdm import tqdm
import h5py
import numpy as np
import matplotlib.pyplot as plt
import datetime

data_folder = '/afs/cern.ch/project/spsecloud/SPS_Scrubbing2021_data1/ECM/Overviews/'
data_folder_BCT = '/afs/cern.ch/project/spsecloud/SPS_Scrubbing2021_data1/data_nxcals/Overviews/'

def get_var(cycleStamp_list_str, h5_file, value_path):
    var = []
    for cycleStamp in cycleStamp_list_str:
       if value_path in h5_file:
           vv = h5_file[value_path][()]
       else:
           vv = -1 
       vv.append(var) 
    return
BCT_h5 = h5py.File(data_folder_BCT + 'BCT_overview.h5', 'r')

cycleStamps_list_str_BCT = list(BCT_h5.keys())

max_intensity_list = [BCT_h5[cycleStamp]['SPS.BCTDC.51454/maximum_intensity_protons'][()] for cycleStamp in cycleStamps_list_str_BCT]
integrated_intensity_list = [BCT_h5[cycleStamp]['SPS.BCTDC.51454/integrated_intensity_protons_seconds'][()] for cycleStamp in cycleStamps_list_str_BCT]

#ECM/Overviews/USER.MDX/Overview_ecm.h5 (One folder for each user)
# structure of h5 file: file[cycleStamp][device][headerName][()] where headerName is one of: measStamp, totalGain, sem2DRaw
def sem2DRaw_list(ECM_h5, device_name, cycleStamps_list_str_p):
#function that exctacts all data of ECM from the already existing h5 file 
    sem2DRaw_list = []
    #ECM_h5 = h5py.File(h5_file, 'r')

    for cycleStamp in cycleStamps_list_str_p:
        try:
            print(f'cycleStamp in nanoseconds: {cycleStamp}')
            print(datetime.datetime.utcfromtimestamp(int(float(cycleStamp)/10**9)))
#            breakpoint()
            sem2DRaw_list.append(ECM_h5[cycleStamp][device_name]['sem2DRaw'][()])
        except:
            breakpoint()
            sem2DRaw_list.append(-1)
            print(f"Data unavailable in sem2DRaw, adding a -1 \n cykleStamp = {cycleStamp}")       

    return sem2DRaw_list

def measStamp_list(ECM_5, device_name, cycleStamps_list_str_p):
#function that exctacts all data of ECM from the already existing h5 file
    measStamp_list = []
    #ECM_h5 = h5py.File(h5_file, 'r')

    for cycleStamp in cycleStamps_list_str_p:

        try:
            measStamp_list.append(ECM_h5[cycleStamp][device_name]['measStamp'][()])
        except:
            measStamp_list.append(-1)
            print(f'{datetime.datetime.utcfromtimestamp(int(cycleStamp))} /n Data unavailable in measStamp, adding -1')       

    return measStamp_list

def totalGain_list(ECM_5, device_name, cycleStamps_list_str_p):
#function that exctacts all data of ECM from the already existing h5 file
    totalGain_list = []
    #ECM_h5 = h5py.File(h5_file, 'r')

    for cycleStamp in cycleStamps_list_str_p:
        try:
#            breakpoint()
            totalGain_list.append(ECM_h5[cycleStamp][device_name]['totalGain'][()])
        except:
            totalGain_list.append(-1)
            print(f'{datetime.datetime.utcfromtimestamp(int(cycleStamp))} /n Data unavailable in totalGain, adding -1')       

    return totalGain_list


cycleStamps_list_BCT = list(map(int, cycleStamps_list_str_BCT))

#sys.path.append('/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/sps-beam-monitoring/sps_beam_monitoring')
#import PlottingClassesSPS

################ user input ###################
user = input('Which user (MD2/MD5)? ')
while user != 'MD2' and user != 'MD5':
    user = input('wrong user input, choose "MD2" or "MD5": ')
###############################################

user_name = f'SPS.USER.{user}'

data_directory = 'ECM/'

tot_dict = {}
tot_dict['cycleStamps_BCT'] = cycleStamps_list_BCT
tot_dict['integrated_intensity'] = integrated_intensity_list
tot_dict['max_intensity'] = max_intensity_list

device_list = ['BESCLD-VECM11733', 'BESCLD-VECM11737', 'BESCLD-VECM11738', 'BESCLD-VECM11754']

# initialize empty dictionaries for all the devices
for device in device_list:
#    h5_name = f'{data_folder}{user_name}/overview_ecm.h5'
    h5_name = f'{data_folder}{user_name}/overview_ecm_three_days.h5'
    ECM_h5 = h5py.File(h5_name, 'r')
    cycleStamps_list_str = list(ECM_h5.keys()) #will be in nanoseconds
    cycleStamps_list_str = cycleStamps_list_str[1:-1]
#    print(f'for device {device} cycleStamps_list_str is {cycleStamps_list_str}')
#    cycleStamps_list = list(map(int, cycleStamps_list_str[:-1]))
    cycleStamps_list = list(map(int, cycleStamps_list_str[1:-1]))
#    tot_dict[device] = {}
#    tot_dict[device]['header'] = {'cycleStamp': []} #don't want to save this again
#    tot_dict[device]['value']
    tot_dict[device] = {'cycleStamp_ECM': cycleStamps_list,
                        'sem2DRaw': sem2DRaw_list(ECM_h5, device, cycleStamps_list_str), 
                        'totalGain': totalGain_list(ECM_h5, device, cycleStamps_list_str),
                        'measStamp': measStamp_list(ECM_h5, device, cycleStamps_list_str)}

pickle.dump(tot_dict, open('overview_pickles/overview_ecm_' + user + '_from_h5' + '_three_days' +'.pkl', 'wb'))

#ec = PlottingClassesSPS.ECLOUD(dict_ec.keys())

#ec.plot(dict_ec)
