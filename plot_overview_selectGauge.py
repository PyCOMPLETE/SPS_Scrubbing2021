import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pickle
import datetime
import sys

#plt.style.use('kostas')

#gauge = sys.argv[1]

gauge_type = input('VACCMW.VGHB enter: "V" or MKDVB enter: "M"')
while(gauge_type != 'V' and gauge_type != 'M'):
    gauge_type = input('Please enter "V" or "M"')

if(gauge_type == 'V'):
    gauge = input('enter gauge number: ')
    gauge_name = 'VACCMW.VGHB_' + gauge + '.PR'
elif(gauge_type == 'M'):
    gauge_name = 'MKDVB.51698:PRESSURE'
    gauge = 'MKDVB'

print('plotting for gauge ' + gauge_name)
save = input('save figure or show figure? (save/show)')

# gauge = '51860' #MKDV1, 10660, 61674, 51860, 52060, 51796
# gauge = 'MKDV1' #10660, 61674, 51860, 52060, 51796
# gauge_title = 'MKDVB'
gauge_title = gauge_name #'VGHB_' + gauge
plot_color = 'b' 
#pickle_file = 'overview_pickles/overview_thursday.pkl'
pickle_file = 'overview_pickles/overview_from_h5_' + gauge + '.pkl'

today = datetime.date.today().isoformat()
print(today)

ms = 3
overview = pickle.load(open(pickle_file,'rb'))

cycleStamps = np.array(overview['cycleStamps'])
max_int = np.array(overview['max_intensity'])
integrated_intensity = np.array(overview['integrated_intensity'])
gauge_to_plot = np.array(overview['max_pressure_' + gauge])

#mask = gauge_to_plot > 0
mask = max_int > 1e11
mask = np.logical_and(mask, gauge_to_plot > 0)

cycleStamps = cycleStamps[mask]
max_int = max_int[mask]
integrated_intensity = integrated_intensity[mask]
gauge_to_plot = gauge_to_plot[mask]

utc_dates = list(map(datetime.datetime.utcfromtimestamp, cycleStamps)) 

gva_dates = [date + datetime.timedelta(hours=2) for date in utc_dates]
        
dates = matplotlib.dates.date2num(gva_dates)
plot_style = plot_color + '.'
fig1 = plt.figure(1, figsize=[6.4*1.2, 4.8*1.3])
ax1 = fig1.add_subplot(414)
ax1.plot_date(dates, gauge_to_plot/integrated_intensity, plot_style, label = gauge, ms=ms)
ax1.set_ylabel('Normalized pressure\n[mbar/p/s]')
#ax1.set_ylim(0,0.8e-18)
#ax1.set_xlabel('Date')
plt.xticks(rotation=40)
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
ax1.set_yscale('log')
plt.grid('on')
#ax1.set_xlabel('Date')
#fig1.subplots_adjust(bottom=0.2)
#plt.title('MKDVB')
#plt.legend(loc='upper left')

ax2 = fig1.add_subplot(413, sharex=ax1)
ax2.plot_date(dates, gauge_to_plot, plot_style , label=gauge, ms=ms)
#ax2.plot_date(dates, np.array(vghb_10660)/np.array(integrated_intensity), 'b.', label='VGHB_10660', ms=ms)
ax2.set_ylabel('Pressure [mbar]')
#ax2.set_ylim(0,0.5e-6)
#ax2.set_xlabel('Date')
plt.xticks(rotation=40)
ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
plt.setp(ax2.get_xticklabels(), visible=False)
plt.grid('on')
#ax2.set_xticklabels([])
#plt.title('VGHB_10660')
#plt.legend(loc='upper left')

ax3 = fig1.add_subplot(412, sharex=ax1, yscale='log')
ax3.plot_date(dates, np.array(integrated_intensity), plot_style, label = gauge, ms=ms)
ax3.set_ylabel('Integrated \n intensity\n[p*s]')
plt.xticks(rotation=40)
ax3.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
#ax3.set_ylim(0, 1.6e12)
#ax3.set_xticklabels([])
plt.grid('on')
plt.setp(ax3.get_xticklabels(), visible=False)
#plt.title('MKDV1')

#fig1.subplots_adjust(bottom=0.15)
#fig1.savefig('pressure_MKDV1.png', dpi=200)

ax4 = fig1.add_subplot(411, sharex=ax1)
ax4.plot_date(dates, np.array(max_int), plot_style, label = gauge, ms=ms)
ax4.set_ylabel('Maximum intensity\n[p]')
plt.xticks(rotation=40)
ax4.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
#ax3.set_ylim(0, 1.6e12)
#ax3.set_xticklabels([])
plt.setp(ax4.get_xticklabels(), visible=False)
#plt.title('MKDV1')
plt.title(gauge_title)
plt.grid('on')
fig1.subplots_adjust(bottom=0.15)


if save == 'save':
    figName = 'pictures/pressure_' + gauge + '_' + today + '.png'
    print('saving figure as: ' + figName)
    fig1.savefig(figName, dpi = 200)
else:
    print('showing figure:')
    plt.show()
#fig1.savefig('pictures/pressure_' + gauge +'.png', dpi=200)

#plt.show()

