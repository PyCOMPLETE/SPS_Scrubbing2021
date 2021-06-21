import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pickle
import datetime
import sys

# plot from pkl file w structure
# pkl files are in the folders "ECM/SPS.USER.MD2 or MD5"
# called overview_ecm_**username**_from_h5.pkl
# the stucture in the file is as follows:
# tot_dict['cycleStamps'] = cycleStamps_list
# tot_dict['integrated_intensity'] = integrated_intensity_list
# tot_dict['max_intensity'] = max_intensity_list
# tot_dict[device] = {'sem2DRaw': sem2DRaw_list(h5_name, device, cycleStamp_list_str), 
#                     'totalGain': totalGain_list(h5_name, device, cycleStamp_list_str),
#                     'measStamp': measStamp_list(h5_name, device, cycleStamp_list_str)}

##TO DO
#choose device
#choose user

# example name of ecm monitor BESCLD-VECM11733
#ecm_monior = sys.argv[1]    ######### TO DO ########## choose ecm monitor
ecm_monitor = 11733
print(f'plotting for ecm monitor BESCLD-VECM{ecm_monitor}')
save = input('save figure or show figure? (save/show)')

ecm_title = f'BESCLD-VECM{ecm_monitor}'
plot_color = 'b' 
#include BCT things in the pickle of the ecm but just plot it like this now
pickle_fileBCT = 'overview_pickles/overview_from_h5_' + str(51860) + '.pkl'
pickle_file = 'overview_pickles/overview_ecm_SPS.USER.MD2.pkl'  ##### TO DO ###### make it possible to choose user

today = datetime.date.today().isoformat()
print(today)

ms = 3
overviewBCT = pickle.load(open(pickle_fileBCT, 'rb'))
overview = pickle.load(open(pickle_file,'rb'))

cycleStampsBCT = np.array(overviewBCT['cyckleStamps'])

cycleStamps = np.array(overview[f'{ecm_title}/Aquisition']['header']['cycleStamps'])
totalGain = np.array(overview[f'{ecm_title}/Aquisition']['value']['totalGain'])
measStamp = np.array(overview[f'{ecm_title}/Aquisition']['value']['measStamp'])

print(f'len(totalGain) = {len(totalGain)} and len(measStamp) = {len(measStamp)}')
 

# #mask = gauge_to_plot > 0
# mask = max_int > 1e11
# mask = np.logical_and(mask, gauge_to_plot > 0)

# cycleStamps = cycleStamps[mask]
# max_int = max_int[mask]
# integrated_intensity = integrated_intensity[mask]
# gauge_to_plot = gauge_to_plot[mask]

utc_dates = list(map(datetime.datetime.utcfromtimestamp, cycleStamps)) 

gva_dates = [date + datetime.timedelta(hours=2) for date in utc_dates]
        
dates = matplotlib.dates.date2num(gva_dates)
# plot_style = plot_color + '.'
# fig1 = plt.figure(1, figsize=[6.4*1.2, 4.8*1.3])
# ax1 = fig1.add_subplot(414)
# ax1.plot_date(dates, gauge_to_plot/integrated_intensity, plot_style, label = gauge, ms=ms)
# ax1.set_ylabel('Normalized pressure\n[mbar/p/s]')
# #ax1.set_ylim(0,0.8e-18)
# #ax1.set_xlabel('Date')
# plt.xticks(rotation=40)
# ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
# ax1.set_yscale('log')
# plt.grid('on')
# #ax1.set_xlabel('Date')
# #fig1.subplots_adjust(bottom=0.2)
# #plt.title('MKDVB')
# #plt.legend(loc='upper left')

# ax2 = fig1.add_subplot(413, sharex=ax1)
# ax2.plot_date(dates, gauge_to_plot, plot_style , label=gauge, ms=ms)
# #ax2.plot_date(dates, np.array(vghb_10660)/np.array(integrated_intensity), 'b.', label='VGHB_10660', ms=ms)
# ax2.set_ylabel('Pressure [mbar]')
# #ax2.set_ylim(0,0.5e-6)
# #ax2.set_xlabel('Date')
# vplt.xticks(rotation=40)
# ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
# plt.setp(ax2.get_xticklabels(), visible=False)
# plt.grid('on')
# #ax2.set_xticklabels([])
# #plt.title('VGHB_10660')
# #plt.legend(loc='upper left')

# ax3 = fig1.add_subplot(412, sharex=ax1, yscale='log')
# ax3.plot_date(dates, np.array(integrated_intensity), plot_style, label = gauge, ms=ms)
# ax3.set_ylabel('Integrated \n intensity\n[p*s]')
# plt.xticks(rotation=40)
# ax3.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
# #ax3.set_ylim(0, 1.6e12)
# #ax3.set_xticklabels([])
# plt.grid('on')
# plt.setp(ax3.get_xticklabels(), visible=False)
# #plt.title('MKDV1')

# #fig1.subplots_adjust(bottom=0.15)
# #fig1.savefig('pressure_MKDV1.png', dpi=200)

# ax4 = fig1.add_subplot(411, sharex=ax1)
# ax4.plot_date(dates, np.array(max_int), plot_style, label = gauge, ms=ms)
# ax4.set_ylabel('Maximum intensity\n[p]')
# plt.xticks(rotation=40)
# ax4.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
# #ax3.set_ylim(0, 1.6e12)
# #ax3.set_xticklabels([])
# plt.setp(ax4.get_xticklabels(), visible=False)
# #plt.title('MKDV1')
# plt.title(gauge_title)
# plt.grid('on')
# fig1.subplots_adjust(bottom=0.15)


# if save == 'save':
#     figName = 'pictures/pressure_' + gauge + '_' + today + '.png'
#     print('saving figure as: ' + figName)
#     fig1.savefig(figName, dpi = 200)
# else:
#     print('showing figure:')
#     plt.show()
# #fig1.savefig('pictures/pressure_' + gauge +'.png', dpi=200)

# #plt.show()

