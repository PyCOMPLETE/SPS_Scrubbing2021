import datetime
import os
out_directory = '/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/data_nxcals/BCT/'
list_of_files = os.listdir(out_directory)

if list_of_files == []:
    last_hour_date = datetime.datetime(2021, 5, 31, 0) #.strftime("%Y-%m-%d %H:%M:%S")
else:
    last_file = max(list_of_files)
    year, month, day, hour, minute, second, microsecond, parquet = last_file.split('.')
    last_hour_date = datetime.datetime(int(year), int(month), int(day), int(hour)) - datetime.timedelta(hours=1)

previous_date = last_hour_date

datetime_now = datetime.datetime.now()

time_ranges = []
while previous_date + datetime.timedelta(hours=1) < datetime_now:
    time_ranges.append((previous_date.strftime("%Y-%m-%d %H:%M:%S"), (previous_date + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")))
    previous_date += datetime.timedelta(hours=1)
    

print(time_ranges)
