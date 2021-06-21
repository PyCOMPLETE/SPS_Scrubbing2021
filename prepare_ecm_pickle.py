import sys
import datascout
import pickle
import os
from tqdm import tqdm

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
    fileslist = os.listdir('data_pyjapcscout/temporary_ecloud/ecloud/' + user + '/')
    # loop over all the parquets
    for filename in tqdm(fileslist):
        try:
            dict_ec = datascout.parquet_to_dict('data_pyjapcscout/temporary_ecloud/ecloud/' + user + '/' + filename)
        except:
            print(f"couldn't open file {filename}")
            continue

        for device in device_list:
            tot_dict[device]['header']['cycleStamp'].append(dict_ec[device]['header']['cycleStamp'])
            if dict_ec[device]['value'] == '':
                for i, key in enumerate(tot_dict[device]['value'].keys()):
                    tot_dict[device]['value'][key].append('')
                continue

            for i, key in enumerate(tot_dict[device]['value'].keys()):
                values = dict_ec[device]['value'][key]
                tot_dict[device]['value'][key].append(dict_ec[device]['value'][key])

    pickle.dump(tot_dict, open('overview_pickles/overview_ecm_'+user+'.pkl', 'wb'))

#ec = PlottingClassesSPS.ECLOUD(dict_ec.keys())

#ec.plot(dict_ec)
