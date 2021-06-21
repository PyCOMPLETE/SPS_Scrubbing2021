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
t_start = '2021-06-03 16:00:00.000'
t_end = '2021-06-03 20:00:00.000'
time_ranges_to_download = [(t_start, t_end)]
#####################

device = 'SPS.BCTDC.51454/Acquisition'

user = 'MD2'
fundamental_filter = 'SPS:%:' + user
header_selector = 'SPS:USER:' + user

#SPS.TGM:USER
#SPS.BCTDC.51454
variables = ['SPS.BCTDC.51454:Acquisition:totalIntensity',  
             'SPS.BCTDC.51454:Acquisition:totalIntensity_unitExponent',
             'SPS.BCTDC.51454:Acquisition:measStamp',
             'SPS.BCTDC.51454:Acquisition:measStamp_unitExponent',
             'SPS.TGM:USER'
             ]

for t_start, t_end in time_ranges_to_download:
    print(f'Fetching data between {t_start} and {t_end} ...')
    data = db.get(variables, t_start, t_end, fundamental=fundamental_filter)
    
    for ii in range(len(data['SPS.BCTDC.51454:Acquisition:totalIntensity'][0])):
        meas = data['SPS.BCTDC.51454:Acquisition:measStamp']
        intensity = data['SPS.BCTDC.51454:Acquisition:totalIntensity'][1][ii] * 10 ** data['SPS.BCTDC.51454:Acquisition:totalIntensity_unitExponent'][1][ii]
        cyclestamp = meas[0][ii]
        time_ax = meas[1][ii] * 10** data['SPS.BCTDC.51454:Acquisition:measStamp_unitExponent'][1][ii]
        plt.plot(cyclestamp+time_ax, intensity, 'b')

plt.show()
