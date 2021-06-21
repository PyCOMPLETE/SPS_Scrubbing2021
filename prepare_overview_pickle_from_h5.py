import h5py
import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime
import sys

data_folder = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/Overviews/'

def get_var(cycleStamp_list_str, h5_file, value_path):
    var = []
    for cycleStamp in cycleStamp_list_str:
       if value_path in h5_file:
           vv = h5_file[value_path][()]
       else:
           vv = -1 
       vv.append(var) 
    return
BCT_h5 = h5py.File(data_folder + 'BCT_overview.h5', 'r')
# MKDV1_h5 = h5py.File(data_folder + 'Pressures/MKDVB.51698:PRESSURE_overview.h5', 'r')
#VGHB_10660_h5 = h5py.File(data_folder + 'Pressures/VACCMW.VGHB_10660.PR_overview.h5', 'r')
#VGHB_51860_h5 = h5py.File(data_folder + 'Pressures/VACCMW.VGHB_51860.PR_overview.h5', 'r')

cycleStamps_list_str = list(BCT_h5.keys())

max_intensity_list = [BCT_h5[cycleStamp]['SPS.BCTDC.51454/maximum_intensity_protons'][()] for cycleStamp in cycleStamps_list_str]
integrated_intensity_list = [BCT_h5[cycleStamp]['SPS.BCTDC.51454/integrated_intensity_protons_seconds'][()] for cycleStamp in cycleStamps_list_str]
# max_pressure_MKDV1_list =  [MKDV1_h5[cycleStamp]['MKDVB.51698:PRESSURE/max_pressure_mbar'][()] for cycleStamp in cycleStamps_list_str]
#max_pressure_10660_list =  [VGHB_10660_h5[cycleStamp]['VACCMW.VGHB_10660.PR/max_pressure_mbar'][()] for cycleStamp in cycleStamps_list_str]
#max_pressure_51860_list =  [VGHB_51860_h5[cycleStamp]['VACCMW.VGHB_51860.PR/max_pressure_mbar'][()] for cycleStamp in cycleStamps_list_str]
#max_pressure_51860_list = []
#for cycleStamp in cycleStamps_list_str:
#    print(datetime.datetime.utcfromtimestamp(int(cycleStamp)))
#    max_pressure_51860_list.append(VGHB_51860_h5[cycleStamp]['VACCMW.VGHB_51860.PR/#max_pressure_mbar'][()])

def max_pressure_list(gauge_name, cycleStamps_list_str_p):
    max_list = []
    VGHB_h5 = h5py.File(data_folder + 'Pressures/'+ gauge_name + '_overview.h5', 'r')

    for cycleStamp in cycleStamps_list_str_p:
        try:
            print(datetime.datetime.utcfromtimestamp(int(cycleStamp)))
            max_list.append(VGHB_h5[cycleStamp][gauge_name + '/max_pressure_mbar'][()])
        except:
            max_list.append(-1)
            print("Data unavailable, adding a -1")

    return max_list

    
cycleStamps_list = list(map(int, cycleStamps_list_str))

#######################################################################
# selecet gauge to plot
#gauge_name = 'VGHB_51860.PR'
#gauge_nbr = '51860'
gauge_type = input('VACCMW.VGHB enter: "V" or MKDVB enter: "M"')
while(gauge_type != 'V' and gauge_type != 'M'):
    gauge_type = input('Please enter "V" or "M"')

if(gauge_type == 'V'):
    gauge_nbr = input('enter gauge number: ')
    gauge = 'VACCMW.VGHB_' + gauge_nbr + '.PR'
    gauge_name = gauge_nbr
elif(gauge_type == 'M'):
    gauge = 'MKDVB.51698:PRESSURE'
    gauge_name = 'MKDVB' ## is this correct

#gauge_name = sys.argv[1] #just the five numbers
print(f'gauge_name = {gauge_name}')
# VGHB_51860.PR
#######################################################################

mydict = {}
mydict['cycleStamps'] = cycleStamps_list
mydict['integrated_intensity'] = integrated_intensity_list
# mydict['max_pressure_MKDV1'] = max_pressure_MKDV1_list
#mydict['max_pressure_10660'] = max_pressure_10660_list
if(gauge_type == 'V'):
    mydict['max_pressure_' + gauge_name] = max_pressure_list('VACCMW.VGHB_' + gauge_name + '.PR', cycleStamps_list_str)
elif(gauge_type == 'M'):
    mydict['max_pressure_' + gauge_name] = max_pressure_list('MKDVB.51698:PRESSURE', cycleStamps_list_str)

#mydict['max_pressure_51860'] = max_pressure_51860_list
# mydict['max_pressure_61674'] = max_pressure_61674_list
mydict['max_intensity'] = max_intensity_list
pickle.dump(mydict, open('overview_pickles/overview_from_h5_' + gauge_name + '.pkl', 'wb'))
 
#plt.plot(cycleStamps_list, max_intensity_list)
#plt.show()
