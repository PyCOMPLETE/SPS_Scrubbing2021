# With this script we create one h5 Overview file per user from the parquet 
# files in ECM/{user}/.
#
# The h5 file fields can be accessed as follows:
# 
# file = overview_manager.open_file('overview_ecm.h5')
# quantity = file['cyclestamp']['device']['quantity'][()]
# 
# where quantity can be one of the following:
#   - sem2DRaw: ecm signal. Dimesnions: number of channels x number of measurements
#   - measStamp: timeStamp associated to a measurement
#   - totalGain: the gain of the ecm. the sem2DRaw data have to be normalized by this number

import sys
import datascout
import pickle
import os
from tqdm import tqdm
import overview_manager
import datetime
import numpy as np

sys.path.append('/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/sps-beam-monitoring/sps_beam_monitoring')
import PlottingClassesSPS

data_directory = 'data_pyjapcscout/temporary_ecloud/ecloud/'

tot_dict = {}
device_list = ['BESCLD-VECM11733/Acquisition', 'BESCLD-VECM11737/Acquisition', 'BESCLD-VECM11738/Acquisition', 'BESCLD-VECM11754/Acquisition']

# initialize empty dictionaries for all the devices
for device in device_list:
    tot_dict[device] = {}
    tot_dict[device]['header'] = {'cycleStamp': []}
    tot_dict[device]['value'] = {'sem2DRaw': [], 
                                 'totalGain': [],
                                 'measStamp': []}

#users_list = ['SPS.USER.MD2', 'SPS.USER.MD5']
users_list = ['SPS.USER.MD5']
for user in users_list:
    overview_name = 'ECM/Overviews/'+ user + '/overview_ecm.h5' 
    overview_file = overview_manager.open_file(overview_name)
    if len(overview_file.keys())>0:
        #if we find already an overview file we identify the first file to start from
        last_filename = overview_file['last_filename'][()].decode().split('.')
        yy = int(last_filename[0])
        mm = int(last_filename[1])
        dd = int(last_filename[2])
        hh = int(last_filename[3])
        mn = int(last_filename[4])
        ss = int(last_filename[5])
        ms = int(last_filename[6])
        
        last_datetime = datetime.datetime(yy,mm,dd,hh,mn,ss,ms)
        last_day_stamp = datetime.datetime.timestamp(datetime.datetime(yy,mm,dd))
        last_time_stamp = datetime.datetime.timestamp(last_datetime)
    else:
        last_day_stamp = last_time_stamp = datetime.datetime.timestamp(datetime.datetime(2021,5,31))
    
    print('last time:')
    print(last_time_stamp)

    # find the days to be processed in the days list, i.e. the days s.t. date>last_date
    daylist = np.array(os.listdir(f'ECM/{user}/'))
    timestamps_list = np.zeros(len(daylist))

    for i, day in enumerate(daylist[0:5]):
        yy, mm, dd = day.split('-')
        # we have to add a day to find the last incomplete day
        datetime_day = datetime.datetime(int(yy), int(mm), int(dd))+datetime.timedelta(hours=24)
        timestamps_list[i] = datetime.datetime.timestamp(datetime_day)
    
    mask = timestamps_list >= last_day_stamp
    #loop over all days
    for day in daylist[mask]:
    # loop over all the parquets
        print(day)
        fileslist = np.array(os.listdir(f'ECM/{user}/{day}/'))
        timestamps_list_files = np.zeros(len(fileslist))
        for i, day in enumerate(fileslist):
            yy, mm, dd, hh, mn, ss, mus = day.split('.')[:-1]
            datetime_day_file = datetime.datetime(int(yy), int(mm), int(dd), int(hh), int(mn), int(ss), int(mus))
            timestamps_list_files[i] = datetime.datetime.timestamp(datetime_day_file)

        mask_files = timestamps_list_files > last_time_stamp
        for filename in tqdm(fileslist):
            filename_split = filename.split('.')
            yy = int(filename_split[0])
            mm = int(filename_split[1])
            dd = int(filename_split[2])
            hh = int(filename_split[3])
            mn = int(filename_split[4])
            ss = int(filename_split[5])
            ms = int(filename_split[6])
    
            this_datetime = datetime.datetime(yy,mm,dd,hh,mn,ss,ms)
            this_time_stamp = datetime.datetime.timestamp(this_datetime)
            
            #print(cycleStamp)
            if this_time_stamp <= last_time_stamp:
                continue

            #print(filename)
            try:
                dict_ec = datascout.parquet_to_dict('data_pyjapcscout/temporary_ecloud/ecloud/' + user + '/' + filename)
            except:
                print(f"couldn't open file {filename}")
                continue

            for device in device_list:

                #print(filename)
                cycleStamp = dict_ec[device]['header']['cycleStamp']
                device_short = device.split('/')[0]
                stamp_device = f'{int(cycleStamp)}/{device_short}/'
                if not dict_ec[device]['value'] == '':
                    try:
                        sem2DRaw = dict_ec[device]['value']['sem2DRaw']
                        totalGain = dict_ec[device]['value']['totalGain']
                        measStamp = dict_ec[device]['value']['measStamp']
                    except:
                        print(f'something went wrong with file: {filename}')
                        sem2dRaw = -1
                        totalGain = -1
                        measStamp = -1  
                else:
                    print('Empty cycle')
                    sem2dRaw = -1
                    totalGain = -1
                    measStamp = -1                

                overview_manager.write_value(sem2DRaw, stamp_device + 'sem2DRaw', overview_file)
                overview_manager.write_value(totalGain, stamp_device + 'totalGain', overview_file)
                overview_manager.write_value(measStamp, stamp_device + 'measStamp', overview_file)

    if not 'last_filename' in overview_file.keys():    
        overview_file['last_filename'] = filename.encode()
    else:
        overview_file['last_filename'][()] = filename.encode()
    overview_manager.close_file(overview_file)

