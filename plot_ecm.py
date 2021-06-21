import sys
import datascout
sys.path.append('/afs/cern.ch/work/s/spsscrub/SPS_Scrubbing2021/sps-beam-monitoring/sps_beam_monitoring')
import PlottingClassesSPS

data_directory = 'data_pyjapcscout/temporary_ecloud/'

dict_ec = datascout.parquet_to_dict(data_directory + '2021.06.09.08.00.09.390139.parquet')

ec = PlottingClassesSPS.ECLOUD(dict_ec.keys())

ec.plot(dict_ec)
