import pytimber
print('imported PyTimber')
import numpy as np
import datetime
import datascout as ds
import os.path
import overview_manager
import sys

db = pytimber.LoggingDB()
bct_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/'
output_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/Pressures/'
overwrite = True
#overview_name = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/Overviews/Pressures_overview.h5'

#gauge = 'VACCMW.VGHB_10660.PR'
#gauge = 'VACCMW.VGHB_51796.PR'
#gauge = 'VACCMW.VGHB_51860.PR'
#gauge = 'VACCMW.VGHB_52060.PR'
# gauge = 'MKDVB.51698:PRESSURE'
#gauge = 'VACCMW.VGHB_61674.PR'

gauge_type = input('VACCMW.VGHB enter: "V" or MKDVB enter: "M"')
while(gauge_type != 'V' and gauge_type != 'M'):
    gauge_type = input('Please enter "V" or "M"')

if(gauge_type == 'V'):
    gauge_nbr = input('enter gauge number: ')
    gauge = 'VACCMW.VGHB_' + gauge_nbr + '.PR'
elif(gauge_type == 'M'):
    gauge = 'MKDVB.51698:PRESSURE'

print(f'downloading data from gauge {gauge}')

output_directory = output_directory + gauge + '/'
overview_name = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/Overviews/Pressures/' + gauge + '_overview.h5'

# Temp filenames
temp_parent = 'data_nxcals/temps_pressure/'
temp_folder = temp_parent + gauge + '/'
temp_overview_name = temp_folder + gauge + '_overview.h5'

if not os.path.exists(temp_parent):
    os.mkdir(temp_parent)

os.mkdir(temp_folder)
os.system('cp ' + overview_name + ' ' + temp_overview_name)
# Open the temp overview file
temp_overview_file = overview_manager.open_file(temp_overview_name)
        

# list_of_gauges = [
#  'VACCMW.VGHB_10660.PR', 'VACCMW.VGHB_10740.PR', 'VACCMW.VGHB_11540.PR', 'VACCMW.VGHB_11931.PR',   
#  'VACCMW.VGHB_11936.PR', 'VACCMW.VGHB_11959.PR', 'VACCMW.VGHB_11993.PR', 'VACCMW.VGHB_12060.PR',
#  'VACCMW.VGHB_12940.PR', 'VACCMW.VGHB_13160.PR', 'VACCMW.VGHB_20060.PR', 'VACCMW.VGHB_20380.PR',
#  'VACCMW.VGHB_20660.PR', 'VACCMW.VGHB_21540.PR', 'VACCMW.VGHB_21974.PR', 'VACCMW.VGHB_22060.PR', 
#  'VACCMW.VGHB_22940.PR', 'VACCMW.VGHB_23160.PR', 'VACCMW.VGHB_30060.PR', 'VACCMW.VGHB_30660.PR',
#  'VACCMW.VGHB_30740.PR', 'VACCMW.VGHB_31380.PR', 'VACCMW.VGHB_32280.PR', 'VACCMW.VGHB_32940.PR',
#  'VACCMW.VGHB_33160.PR', 'VACCMW.VGHB_40060.PR', 'VACCMW.VGHB_40660.PR', 'VACCMW.VGHB_40740.PR', 
#  'VACCMW.VGHB_41540.PR', 'VACCMW.VGHB_42040.PR', 'VACCMW.VGHB_42940.PR', 'VACCMW.VGHB_43160.PR', 
#  'VACCMW.VGHB_50060.PR', 'VACCMW.VGHB_50660.PR', 'VACCMW.VGHB_50740.PR', 'VACCMW.VGHB_51080.PR', 
#  'VACCMW.VGHB_51140.PR', 'VACCMW.VGHB_51280.PR', 'VACCMW.VGHB_51340.PR', 'VACCMW.VGHB_51480.PR', 
#  'VACCMW.VGHB_51540.PR', 'VACCMW.VGHB_52060.PR', 'VACCMW.VGHB_52260.PR', 'VACCMW.VGHB_52940.PR', 
#  'VACCMW.VGHB_53160.PR', 'VACCMW.VGHB_60060.PR', 
#  'VACCMW.VGHB_51698.PR',
#  'MKDVB.51698:PRESSURE',
#  'VACCMW.VGHB_60740.PR', 'VACCMW.VGHB_61340.PR', 'VACCMW.VGHB_61540.PR', 'VACCMW.VGHB_61631.PR',
#  'VACCMW.VGHB_61634.PR', 'VACCMW.VGHB_61637.PR', 'VACCMW.VGHB_61674.PR', 'VACCMW.VGHB_61693.PR',
#  'VACCMW.VGHB_61731.PR', 'VACCMW.VGHB_61756.PR', 'VACCMW.VGHB_62060.PR', 'VACCMW.VGHB_62260.PR',
#  'VACCMW.VGHB_62940.PR', 'VACCMW.VGHB_63160.PR',
#  ]


list_of_gauges = [ gauge ] #don't put more gauges here!!!!!!!!!!!!!!!!!!!

for device in list_of_gauges:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

##download from date of last recorded file until today (one hour ago)
list_of_days = os.listdir(output_directory)

if list_of_days == []:
    last_hour_date = datetime.datetime(2021, 5, 31, 0) #.strftime("%Y-%m-%d %H:%M:%S")
else:
    last_day = max(list_of_days)
    list_of_files = os.listdir(output_directory + '/' + last_day)
    print(f'last day = {last_day}')
    last_file = max(list_of_files)
    year, month, day, hour, minute, second, microsecond, parquet = last_file.split('.')
    last_hour_date = datetime.datetime(int(year), int(month), int(day), int(hour)) - datetime.timedelta(hours=1)

previous_date = last_hour_date

datetime_now = datetime.datetime.now()

two_minutes = datetime.timedelta(minutes=2)

time_ranges_to_download_datetime = []
while previous_date + datetime.timedelta(hours=1) < datetime_now:
    time_ranges_to_download_datetime.append(( (previous_date - two_minutes), 
                                              (previous_date + datetime.timedelta(hours=1) + two_minutes) ))
#    time_ranges_to_download.append(((previous_date - two_minutes).strftime("%Y-%m-%d %H:%M:%S"), 
#                                   ((previous_date + datetime.timedelta(hours=1) + two_minutes).strftime("%Y-%m-%d %H:%M:%S")))
    previous_date += datetime.timedelta(hours=1)
print('Downloading in time ranges:')
for time_range in time_ranges_to_download_datetime:
    print((time_range[0].strftime("%Y-%m-%d %H:%M:%S"), time_range[1].strftime("%Y-%m-%d %H:%M:%S")))
###############

#year = 2021
#month = 5
#day = 31

for t_start_datetime, t_end_datetime in time_ranges_to_download_datetime:
#for hour in range(24):# range(24):
    #overview_file = overview_manager.open_file(overview_name)
    t_start = t_start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    t_end = t_end_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # date_start = datetime.datetime(2021, month, day, hour, 0, 0) - datetime.timedelta(minutes=2)
    # date_end = datetime.datetime(2021, month, day, hour, 59, 59) + datetime.timedelta(minutes=2)
    # t_start = date_start.strftime("%Y-%m-%d %H:%M:%S")
    # t_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
    print(f'Fetching data between {t_start} and {t_end} ...')
    nxcals_data = db.get(list_of_gauges, t_start, t_end)
    
    ### resample data to every second.
    data = {}
    valid_device = {}
    for device in nxcals_data.keys():
       old_time = nxcals_data[device][0]
       old_pressure = nxcals_data[device][1]
       
       if len(old_time) < 2:
           valid_device[device] = False
           continue
       else:
           valid_device[device] = True

       new_time = np.arange(old_time[0], old_time[-1] + 0.5)
       new_pressure = np.zeros_like(new_time)

       ii = 0
       for kk in range(len(old_time)-1):
           while old_time[kk+1] - 0.5 > new_time[ii]:
               new_pressure[ii] = old_pressure[kk]
               ii += 1
       new_pressure[-1] = old_pressure[-1]

       data[device] = (new_time, new_pressure)

    list_bct_day_dirs = os.listdir(bct_directory)
    list_of_all_bct_files = []
    for bct_day_directory in list_bct_day_dirs:
        for bct_file in os.listdir(bct_directory + '/' + bct_day_directory):
            list_of_all_bct_files.append(bct_file)

    list_of_bct_files = []
    for bct_file in list_of_all_bct_files:
        year, month, day, hour, minute, second, microsecond, parquet = bct_file.split('.')
        file_date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        if file_date > t_start_datetime and file_date < t_end_datetime:
            list_of_bct_files.append(bct_file)
    #list_of_bct_files = [this_file for this_file in os.listdir(bct_directory) if f'{year}.{month:02d}.{day:02d}.{hour:02d}' in this_file]
    curr_day_dots = ''
    for bct_file in list_of_bct_files: 
    
        #infile = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/2021.05.31.20.27.10.935000.parquet'
        if bct_file[0:10] != curr_day_dots:
            curr_day_dots = bct_file[0:10]
            curr_day = bct_file[0:10].replace('.', '-')
            if not os.path.exists(temp_folder + curr_day):
                os.mkdir(temp_folder + curr_day)
        
        input_file = bct_directory + curr_day + '/' + bct_file
        
        bct = ds.parquet_to_dict(input_file)
        
        cycleStamp_ns = bct['SPS.BCTDC.51454/Acquisition']['header']['cycleStamp']
        cycleStamp_s = cycleStamp_ns * 1.e-9
        
        cycleStamp_time = datetime.datetime.utcfromtimestamp(cycleStamp_s) + datetime.timedelta(hours=2) 
        ## Add 2 hours to go from UTC to UTC+2 (GVA time)
        
        filename = cycleStamp_time.strftime("%Y.%m.%d.%H.%M.%S.%f") + '.parquet'
        #final_path = output_directory + '/' + filename
        temp_final_path = temp_folder + curr_day + '/' + filename 
        if os.path.exists(temp_final_path):
            if overwrite:
                print(f'{filename} exists, overwriting...')
            else:
                print(f'{filename} exists, not overwriting...')
                continue
        else:
                print(f'Creating {filename}...')
        
        t_start = cycleStamp_s
        t_end = cycleStamp_s + 8.2 # 7.2 for the length of the cycle, plus 1 second
        
        
        #variables = list_of_gauges
        #data = db.get(variables, t_start, t_end)
        
        user = 'MD5'
        fundamental_filter = 'SPS:%:' + user
        header_selector = 'SPS:USER:' + user
        
        full_dictionary = {}
        for device in list_of_gauges:
            if not valid_device[device]:
                continue
            full_dictionary[device] = {}
        
            ### build header
            header = {
                      'acqStamp' : 0,
                      'cycleStamp' : cycleStamp_ns,
                      'isFirstUpdate' : False,
                      'isImmediateUpdate' : False,
                      'selector': header_selector,
                      'setStamp': 0,
                     }
            full_dictionary[device]['header'] = header
            ######################3
            
            ### build value
            mask = np.logical_and(t_start < data[device][0], data[device][0] < t_end)
            time_axis = data[device][0][mask] - cycleStamp_s # [s]
            pressure_axis = data[device][1][mask] # mbar

            if len(pressure_axis) == 0:
                print(f'device {device} is empty')
                max_pressure_mbar = -1
            else:
                max_pressure_mbar = np.max(pressure_axis)
            
            # check exponents
            value = {
                     'time_s': time_axis,
                     'pressure_mbar' : pressure_axis,
                     'max_pressure_mbar' : max_pressure_mbar,
                    }
            stamp_device = f'{int(cycleStamp_s)}/{device}/'
            overview_manager.write_value(max_pressure_mbar, stamp_device + 'max_pressure_mbar', temp_overview_file)

            full_dictionary[device]['value'] = value
            ##############
        
        ds.dict_to_parquet(full_dictionary, temp_final_path)

# Close the overview file
overview_manager.close_file(temp_overview_file)
# Move the temps to the proper folders
os.system('mv ' + temp_overview_name + ' ' + overview_name)
for day_folder in os.listdir(temp_folder):
    if not os.path.exists(output_directory + day_folder):
                os.mkdir(output_directory + day_folder)
    os.system('mv ' + temp_folder + day_folder + '/* ' + output_directory + day_folder)
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

