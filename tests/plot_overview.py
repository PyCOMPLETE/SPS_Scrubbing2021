import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pickle
import datetime

#plt.style.use('kostas')

ms = 3
lotta = pickle.load(open('overview_wednesday.pkl','rb'))

cycleStamps = np.array(lotta['cycleStamps'])
max_int = np.array(lotta['max_intensity'])
integrated_intensity = np.array(lotta['integrated_intensity'])
MKDVB = np.array(lotta['max_pressure_MKDVB'])
vghb_10660 = np.array(lotta['max_pressure_10660'])
vghb_61674 = np.array(lotta['max_pressure_61674'])

#mask = vghb_10660 > 0
mask = max_int > 1e11

cycleStamps = cycleStamps[mask]
max_int = max_int[mask]
integrated_intensity = integrated_intensity[mask]
MKDVB = MKDVB[mask]
vghb_10660 = vghb_10660[mask]

utc_dates = list(map(datetime.datetime.utcfromtimestamp, cycleStamps)) 

gva_dates = [date + datetime.timedelta(hours=2) for date in utc_dates]
        
dates = matplotlib.dates.date2num(gva_dates)
fig1 = plt.figure(1, figsize=[6.4*1.2, 4.8*1.3])
ax1 = fig1.add_subplot(313)
ax1.plot_date(dates, MKDVB/integrated_intensity, 'b.', label='MKDV1', ms=ms)
ax1.set_ylabel('Normalized pressure\n[mbar/p/s]')
#ax1.set_ylim(0,0.8e-18)
#ax1.set_xlabel('Date')
plt.xticks(rotation=40)
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
#ax1.set_xlabel('Date')
#fig1.subplots_adjust(bottom=0.2)
#plt.title('MKDVB')
#plt.legend(loc='upper left')

ax2 = fig1.add_subplot(312, sharex=ax1)
ax2.plot_date(dates, MKDVB, 'b.', label='MKVDV1', ms=ms)
#ax2.plot_date(dates, np.array(vghb_10660)/np.array(integrated_intensity), 'b.', label='VGHB_10660', ms=ms)
ax2.set_ylabel('Pressure [mbar]')
#ax2.set_ylim(0,0.5e-6)
#ax2.set_xlabel('Date')
plt.xticks(rotation=40)
ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
plt.setp(ax2.get_xticklabels(), visible=False)
#ax2.set_xticklabels([])
#plt.title('VGHB_10660')
#plt.legend(loc='upper left')

ax3 = fig1.add_subplot(311, sharex=ax1)
ax3.plot_date(dates, np.array(integrated_intensity), 'b.', ms=ms)
ax3.set_ylabel('Integrated intensity\n[p*s]')
plt.xticks(rotation=40)
ax3.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
#ax3.set_ylim(0, 1.6e12)
#ax3.set_xticklabels([])
plt.setp(ax3.get_xticklabels(), visible=False)
plt.title('MKDV1')
fig1.subplots_adjust(bottom=0.15)
#fig1.savefig('pressure_MKDV1.png', dpi=200)

plt.show()
