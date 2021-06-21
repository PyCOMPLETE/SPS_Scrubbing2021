import pyarrow
import os
import datascout as ds
import awkward as ak
import matplotlib.pyplot as plt

#input_file = 'data_nxcals/BCT/2021.06.01.04.32.06.135000.parquet'

time_axis = []
y_axis = []
for input_file in os.listdir('data_nxcals/BCT/'):
    
    #data = ds.parquet_to_dict('data_nxcals/BCT/' + input_file)
    #timestamp = data['SPS.BCTDC.51454/Acquisition']['header']['cycleStamp']
    #max_int = data['SPS.BCTDC.51454/Acquisition']['value']['maximum_intensity_protons']

    timestamp = ak.from_parquet('data_nxcals/BCT/' + input_file,columns=['SPS.BCTDC.51454/Acquisition'])[0,'SPS.BCTDC.51454/Acquisition','header','cycleStamp']
    max_int = ak.from_parquet('data_nxcals/BCT/' + input_file,columns=['SPS.BCTDC.51454/Acquisition'])[0,'SPS.BCTDC.51454/Acquisition','value','maximum_intensity_protons']

    time_axis.append(timestamp)
    y_axis.append(max_int)

# plt.plot(time_axis, y_axis)
# plt.show()
