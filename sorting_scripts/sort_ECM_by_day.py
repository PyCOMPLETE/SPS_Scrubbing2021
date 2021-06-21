import os
import datetime
from tqdm import tqdm

#A script that sorts all parquet files in the BCT folder in new separate folder for each day.

output_directory = '/afs/cern.ch/project/spsecloud/SPS_Scrubbing2021_data1/ECM/SPS.USER.MD5/'

list_of_files = os.listdir(output_directory)
print(f'length of list_of_files is {len(list_of_files)}')

# download specific range
# t_start = '2021-05-31 15:51:20.000'
# t_end = '2021-05-31 15:52:20.000'
# time_ranges_to_download

#overview_file = overview_manager.open_file(overview_name)

curr_day = ''
N_files = len(list_of_files)
#list_of_files = list_of_files[5:1000] #for testing
#for t_start, t_end in time_ranges_to_move:
for fileName in tqdm(list_of_files):
    #print(f'fileName = {fileName}')
    #if os.path.isdir(fileName): #does not recognize parquet files as files
    if len(fileName)<11:
        #print('above is a directory')
        continue
    
    day = fileName[0:10].replace('.','-')
    #print(f'boolean = {curr_day != day}')
    if curr_day != day:
        print(f'day = {day}')
        curr_day = day
        #os.mkdir(output_directory+'/'+curr_day)
        if not os.path.exists(output_directory+'/'+curr_day):
            os.mkdir(output_directory+'/'+curr_day)
    full_Name = output_directory + fileName
    full_Name_out = output_directory + curr_day + '/'
    os.system('mv ' + full_Name + ' ' + full_Name_out )
    #os.rm(full_Name)
    
     
