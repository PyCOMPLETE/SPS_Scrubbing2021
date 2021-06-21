import pytimber
import numpy as np
import datetime
import datascout as ds
import os.path

db = pytimber.LoggingDB()
bct_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/'
output_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/Pressures/'
overwrite = True

# list_of_gauges = [
# 'VACCMW.VGHB_10660.PR', 'VACCMW.VGHB_10740.PR', 'VACCMW.VGHB_11540.PR', 'VACCMW.VGHB_11931.PR',   
# 'VACCMW.VGHB_11936.PR', 'VACCMW.VGHB_11959.PR', 'VACCMW.VGHB_11993.PR', 'VACCMW.VGHB_12060.PR',
# 'VACCMW.VGHB_12940.PR', 'VACCMW.VGHB_13160.PR', 'VACCMW.VGHB_20060.PR', 'VACCMW.VGHB_20380.PR',
# 'VACCMW.VGHB_20660.PR', 'VACCMW.VGHB_21540.PR', 'VACCMW.VGHB_21974.PR', 'VACCMW.VGHB_22060.PR', 
# 'VACCMW.VGHB_22940.PR', 'VACCMW.VGHB_23160.PR', 'VACCMW.VGHB_30060.PR', 'VACCMW.VGHB_30660.PR',
# 'VACCMW.VGHB_30740.PR', 'VACCMW.VGHB_31380.PR', 'VACCMW.VGHB_32280.PR', 'VACCMW.VGHB_32940.PR',
# 'VACCMW.VGHB_33160.PR', 'VACCMW.VGHB_40060.PR', 'VACCMW.VGHB_40660.PR', 'VACCMW.VGHB_40740.PR', 
# 'VACCMW.VGHB_41540.PR', 'VACCMW.VGHB_42040.PR', 'VACCMW.VGHB_42940.PR', 'VACCMW.VGHB_43160.PR', 
# 'VACCMW.VGHB_50060.PR', 'VACCMW.VGHB_50660.PR', 'VACCMW.VGHB_50740.PR', 'VACCMW.VGHB_51080.PR', 
# 'VACCMW.VGHB_51140.PR', 'VACCMW.VGHB_51280.PR', 'VACCMW.VGHB_51340.PR', 'VACCMW.VGHB_51480.PR', 
# 'VACCMW.VGHB_51540.PR', 'VACCMW.VGHB_52060.PR', 'VACCMW.VGHB_52260.PR', 'VACCMW.VGHB_52940.PR', 
# 'VACCMW.VGHB_53160.PR', 'VACCMW.VGHB_60060.PR', 
# 'VACCMW.VGHB_51698.PR',
# 'MKDVB.51698:PRESSURE'
# ]

list_of_gauges = ['VACCMW.VGHB_10660.PR',
                  'MKDVB.51698:PRESSURE',
                  'VACCMW.VGHB_61674.PR'
                 ]

year = 2021
month = 6
day = 3

for hour in range(10,11):# range(24):
    date_start = datetime.datetime(2021, month, day, hour, 0, 0) - datetime.timedelta(minutes=2)
    date_end = datetime.datetime(2021, month, day, hour, 59, 59) + datetime.timedelta(minutes=2)
    t_start = date_start.strftime("%Y-%m-%d %H:%M:%S")
    t_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
    print(f'Fetching data between {t_start} and {t_end} ...')
    data = db.get(list_of_gauges, t_start, t_end)
    resampled_data = {}
    for device in data.keys():
       old_time = data[device][0]
       old_pressure = data[device][1]
       min_time = old_time[0]
       max_time = old_time[-1] + 0.5
       new_time = np.arange(min_time, max_time)
       new_pressure = np.zeros_like(new_time)

       ii = 0
       for kk in range(len(old_time)-1):
           while old_time[kk+1] - 0.5 > new_time[ii]:
               new_pressure[ii] = old_pressure[kk]
               ii += 1
       new_pressure[-1] = old_pressure[-1]
       resampled_data[device] = (new_time, new_pressure)
    # list_of_bct_files = [this_file for this_file in os.listdir(bct_directory) if f'{year}.{month:02d}.{day:02d}.{hour:02d}' in this_file]
    # for bct_file in list_of_bct_files: 
    # 
    #     #infile = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/2021.05.31.20.27.10.935000.parquet'
    #     input_file = bct_directory + bct_file
    #     
    #     bct = ds.parquet_to_dict(input_file)
    #     
    #     cycleStamp_ns = bct['SPS.BCTDC.51454/Acquisition']['header']['cycleStamp']
    #     cycleStamp_s = cycleStamp_ns * 1.e-9
    #     
    #     cycleStamp_time = datetime.datetime.utcfromtimestamp(cycleStamp_s) + datetime.timedelta(hours=2) 
    #     ## Add 2 hours to go from UTC to UTC+2 (GVA time)
    #     
    #     filename = cycleStamp_time.strftime("%Y.%m.%d.%H.%M.%S.%f") + '.parquet'
    #     final_path = output_directory + filename
    #     
    #     if os.path.exists(final_path):
    #         if overwrite:
    #             print(f'{filename} exists, overwriting...')
    #         else:
    #             print(f'{filename} exists, not overwriting...')
    #             continue
    #     else:
    #             print(f'Creating {filename}...')
    #     
    #     t_start = cycleStamp_s
    #     t_end = cycleStamp_s + 8.2 # 7.2 for the length of the cycle, plus 1 second
    #     
    #     
    #     #variables = list_of_gauges
    #     #data = db.get(variables, t_start, t_end)
    #     
    #     user = 'MD2'
    #     fundamental_filter = 'SPS:%:' + user
    #     header_selector = 'SPS:USER:' + user
    #     
    #     full_dictionary = {}
    #     for device in list_of_gauges:
    #         full_dictionary[device] = {}
    #     
    #         ### build header
    #         header = {
    #                   'acqStamp' : 0,
    #                   'cycleStamp' : cycleStamp_ns,
    #                   'isFirstUpdate' : False,
    #                   'isImmediateUpdate' : False,
    #                   'selector': header_selector,
    #                   'setStamp': 0,
    #                  }
    #         full_dictionary[device]['header'] = header
    #         ######################3
    #         
    #         
    #         ### build value
    #         mask = np.logical_and(t_start < data[device][0], data[device][0] < t_end)
    #         time_axis = data[device][0][mask] - cycleStamp_s # [s]
    #         pressure_axis = data[device][1][mask] # mbar

    #        if len(pressure_axis) == 0:
    #            print(f'device {device} is empty')
    #            max_pressure_mbar = -1
    #        else:
    #            max_pressure_mbar = np.max(pressure_axis)
    #        
    #        # check exponents
    #        value = {
    #                 'time_s': time_axis,
    #                 'pressure_mbar' : pressure_axis,
    #                 'max_pressure_mbar' : max_pressure_mbar,
    #                }
    #        full_dictionary[device]['value'] = value
    #        ##############
    #    
    #    ds.dict_to_parquet(full_dictionary, final_path)



#intensity_at_25ms (protons)
#integrated intensity over cycle (protons*second)
#max intensity (protons)
# 1015ms (injection time wrt to cyclestamp?)
#
# max intensity in cycle   beams[SPSuser]['bct_max_vect'] = np.array([])
# not needed               beams[SPSuser]['SC_numb_vect'] = np.array([])
# cyclestamp beams[SPSuser]['timestamp_float'] = np.array([])
#  beams[SPSuser]['bct_integrated'] = np.array([])
#  beams[SPSuser]['bct_1st_inj'] = np.array([])
#  beams[SPSuser]['acqusition_time_length'] = np.array([])
#  beams[SPSuser]['bct_5th_inj'] = np.array([])




#
#for plotting class
#
# total intensity and exponent
# sampling time
# header
# plot_overview.py in sps-beam-monitoring in hannes space (spsop/Hannes/2021/sps-beam-monitoring/sps-beam_monitorin/plot_overview.py)

####
#length of cycle is 7.2, look for at least 8.2 after cyclestamp, find the peak (pressure?)

###### save per gauge
# pressure vs time in cycle
# max pressure
#

## final plot:
# max_pressure/integrated_intensity vs cyclestamp
# injected intensity vs cyclestamp

