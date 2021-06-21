import pytimber
import numpy as np
import datetime
import datascout as ds
import os
import os.path
import overview_manager

db = pytimber.LoggingDB()
output_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/'
overwrite = False

##download from date of last recorded file until today (one hour ago)
list_of_days = os.listdir(output_directory)

if list_of_days == []:
    last_hour_date = datetime.datetime(2021, 6, 7, 0) #.strftime("%Y-%m-%d %H:%M:%S")
else:
    last_day = max(list_of_days)
    list_of_files = os.listdir(output_directory + '/' + last_day)
    last_file = max(list_of_files)
    print('last_file:')
    print(last_file)
    year, month, day, hour, minute, second, microsecond, parquet = last_file.split('.')
    last_hour_date = datetime.datetime(int(year), int(month), int(day), int(hour))# - datetime.timedelta(hours=1)

previous_date = last_hour_date

datetime_now = datetime.datetime.now()

time_ranges_to_download = []
while previous_date + datetime.timedelta(hours=1) < datetime_now:
    time_ranges_to_download.append((previous_date.strftime("%Y-%m-%d %H:%M:%S"), (previous_date + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")))
    previous_date += datetime.timedelta(hours=1)
print('Downloading in time ranges:')
print(time_ranges_to_download)
###############

###download day:
#month = 6
#day = 5
#time_ranges_to_download = []
#for hour in range(0, 24):
#    date_start = datetime.datetime(2021, month, day, hour, 0, 0) - datetime.timedelta(minutes=2)
#    date_end = datetime.datetime(2021, month, day, hour, 59, 59) + datetime.timedelta(minutes=2)
#    t_start = date_start.strftime("%Y-%m-%d %H:%M:%S")
#    t_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
#    time_ranges_to_download.append( (t_start, t_end) )
################

# download specific range
# t_start = '2021-05-31 15:51:20.000'
# t_end = '2021-05-31 15:52:20.000'
# time_ranges_to_download = [(t_start, t_end)]
#####################

device = 'SPS.BCTDC.51454/Acquisition'
device_to_overview = 'SPS.BCTDC.51454'
overview_name = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/Overviews/BCT_overview.h5'
#overview_file = overview_manager.open_file(overview_name)


USERS = ['MD5', 'MD2']

variables = ['SPS.BCTDC.51454:Acquisition:totalIntensity',  
             'SPS.BCTDC.51454:Acquisition:totalIntensity_unitExponent',
             'SPS.BCTDC.51454:Acquisition:measStamp',
             'SPS.BCTDC.51454:Acquisition:measStamp_unitExponent',
             'SPS.TGM:USER']

# Temp filenames
temp_folder = 'data_nxcals/temp/'
temp_overview_name = temp_folder + '/BCT_overview.h5'
os.mkdir(temp_folder)
os.system('cp ' + overview_name + ' ' + temp_overview_name)
# Open the temp overview file
temp_overview_file = overview_manager.open_file(temp_overview_name)

curr_day = ''
for t_start, t_end in time_ranges_to_download:
    print(f'Fetching data between {t_start} and {t_end} ...')
    if curr_day != t_start[0:10]:
        curr_day = t_start[0:10]
        os.mkdir(temp_folder+'/'+curr_day)
        if not os.path.exists(output_directory+'/'+curr_day):
            os.mkdir(output_directory+'/'+curr_day)

    data = db.get(variables, t_start, t_end)
    
    cycleStamp_list = data[variables[0]][0]
    for cycle_index, cycleStamp_s in enumerate(cycleStamp_list):
        SPS_user = data['SPS.TGM:USER'][1][cycle_index]
        if SPS_user not in USERS:
            continue
        cycleStamp_ns = int(cycleStamp_s * 1.e9)
        
        cycleStamp_time = datetime.datetime.utcfromtimestamp(cycleStamp_s) + datetime.timedelta(hours=2) 
        ## Add 2 hours to go from UTC to UTC+2 (GVA time)

        filename = cycleStamp_time.strftime("%Y.%m.%d.%H.%M.%S.%f") + '.parquet'
        temp_final_path = temp_folder + curr_day + '/' + filename
    
        if os.path.exists(temp_final_path):
            if overwrite:
                print(f'{filename} exists, overwriting...')
            else:
                print(f'{filename} exists, not overwriting...')
                continue
        else:
                print(f'Creating {filename}...')
    
        full_dictionary = {}
        full_dictionary[device] = {}
        ### build header
        header = {
                  'acqStamp' : 0,
                  'cycleStamp' : cycleStamp_ns,
                  'isFirstUpdate' : False,
                  'isImmediateUpdate' : False,
                  'selector': 'SPS:USER:' + SPS_user,
                  'setStamp': 0,
                 }
        full_dictionary[device]['header'] = header
        ######################3
        
        ### build value
        totalIntensity = np.float_(data['SPS.BCTDC.51454:Acquisition:totalIntensity'][1][cycle_index])
        totalIntensity_unitExponent = data['SPS.BCTDC.51454:Acquisition:totalIntensity_unitExponent'][1][cycle_index]
        measStamp = np.float_(data['SPS.BCTDC.51454:Acquisition:measStamp'][1][cycle_index])
        measStamp_unitExponent = data['SPS.BCTDC.51454:Acquisition:measStamp_unitExponent'][1][cycle_index]
        acqTime = ''

        time_axis = measStamp * 10**measStamp_unitExponent
        intensity_axis = totalIntensity * 10**totalIntensity_unitExponent

        # define injection intensity at 25ms of BCT timestamps
        injection_intensity_index = np.argmin(abs(time_axis - 25e-3))         
        injected_intensity_protons = intensity_axis[injection_intensity_index]
        maximum_intensity_protons = np.max(intensity_axis)
        delta_time = np.diff(time_axis)[0]
        integrated_intensity_protons_seconds = np.sum(intensity_axis)*delta_time
        
        # check exponents
        value = {
                 'totalIntensity' : totalIntensity,
                 'totalIntensity_unitExponent' : totalIntensity_unitExponent,
                 'measStamp' : measStamp,
                 'measStamp_unitExponent' : measStamp_unitExponent,
                 'injectionTime_wrt_cycleStamp_s' : 1.015,
                 'acqTime' : acqTime,
                 'injected_intensity_protons' : injected_intensity_protons,
                 'maximum_intensity_protons' : maximum_intensity_protons,
                 'integrated_intensity_protons_seconds' : integrated_intensity_protons_seconds,
                }
        stamp_device = f'{int(cycleStamp_s)}/{device_to_overview}/'
        #overview_manager.write_value(injected_intensity_protons, stamp_device + 'injected_intensity_protons', overview_file)
        #overview_manager.write_value(maximum_intensity_protons, stamp_device + 'maximum_intensity_protons', overview_file)
        #overview_manager.write_value(integrated_intensity_protons_seconds, stamp_device + 'integrated_intensity_protons_seconds', overview_file)
        #overview_manager.write_value(cycleStamp_ns, stamp_device + 'cycleStamp_ns', overview_file)
        #full_dictionary[device]['value'] = value
        
        #####
        #ds.dict_to_parquet(full_dictionary, final_path)
        
        # Write the dict to temp parquet file
        ds.dict_to_parquet(full_dictionary, temp_final_path)
        # Modify the temp overview file  
        overview_manager.write_value(injected_intensity_protons, stamp_device + 'injected_intensity_protons', temp_overview_file)
        overview_manager.write_value(maximum_intensity_protons, stamp_device + 'maximum_intensity_protons', temp_overview_file)
        overview_manager.write_value(integrated_intensity_protons_seconds, stamp_device + 'integrated_intensity_protons_seconds', temp_overview_file)
        overview_manager.write_value(cycleStamp_ns, stamp_device + 'cycleStamp_ns', temp_overview_file)

# Close the overview file
overview_manager.close_file(temp_overview_file)       
# Move the temps to the proper folders
os.system('mv ' + temp_overview_name + ' ' + overview_name)
for curr_day in os.listdir(temp_folder):
    print(curr_day)
    os.system('mv ' + temp_folder + curr_day + '/*.parquet ' + output_directory+'/'+curr_day)
# Remove the temp folder
os.system('rm -r ' + temp_folder)

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

