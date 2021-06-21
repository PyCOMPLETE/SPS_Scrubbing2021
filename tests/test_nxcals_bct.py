import pytimber
import numpy as np
import datetime
import datascout as ds
import os.path
import matplotlib.pyplot as plt

db = pytimber.LoggingDB()
output_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/'

overwrite = False

##download day:
#month = 5
#day = 31
#time_ranges_to_download = []
#for hour in range(9,10):
#    date_start = datetime.datetime(2021, month, day, hour, 0, 0) - #datetime.timedelta(minutes=2)
#    date_end = datetime.datetime(2021, month, day, hour, 59, 59) + #datetime.timedelta(minutes=2)
#    t_start = date_start.strftime("%Y-%m-%d %H:%M:%S")
#    t_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
#    time_ranges_to_download.append( (t_start, t_end) )
###############

#download specific range
t_start = '2021-06-02 16:00:00.000'
t_end = '2021-06-02 17:00:00.000'
time_ranges_to_download = [(t_start, t_end)]
#####################

device = 'SPS.BCTDC.51454/Acquisition'

user = 'MD2kostas'
fundamental_filter = 'SPS:%:' + user
header_selector = 'SPS:USER:' + user


variables = ['SPS.BCTDC.51454:Acquisition:totalIntensity',  
             'SPS.BCTDC.51454:Acquisition:totalIntensity_unitExponent',
             'SPS.BCTDC.51454:Acquisition:measStamp',
             'SPS.BCTDC.51454:Acquisition:measStamp_unitExponent',
             ]

for t_start, t_end in time_ranges_to_download:
    print(f'Fetching data between {t_start} and {t_end} ...')
    data = db.get(variables, t_start, t_end, fundamental=fundamental_filter)
    
    for ii in range(len(data['SPS.BCTDC.51454:Acquisition:totalIntensity'][0])):
        meas = data['SPS.BCTDC.51454:Acquisition:measStamp']
        intensity = data['SPS.BCTDC.51454:Acquisition:totalIntensity'][1][ii] * 10 ** data['SPS.BCTDC.51454:Acquisition:totalIntensity_unitExponent'][1][ii]
        cyclestamp = meas[0][ii]
        time_ax = meas[1][ii] * 10** data['SPS.BCTDC.51454:Acquisition:measStamp_unitExponent'][1][ii]
        plt.plot(cyclestamp+time_ax, intensity, 'r')

plt.show()
        #####
#        ds.dict_to_parquet(full_dictionary, final_path)



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

