import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as hf

class PlottingClassSPS():

    def __init__(self,figsize,pngfolder=None,*args,**kw):
        self.pngfolder = pngfolder
        self.figsize = figsize
        self.figname = self.__class__.__name__
        self._nrows = 1
        self._ncols = 1
        self._sharex = False
        self._sharey = False

    def createFigure(self):
        self.figure = plt.figure(self.figname,figsize=self.figsize)
        plt.show(block=False)

    def initializeFigure(self):
        self.createFigure()
        self.drawFigure()

    def clearFigure(self):
        self.figure.clear()

    def removeLines(self):
        axs = self._getAxes()
        for ax in axs:
            for line in ax.get_lines():
                line.remove()

    def clearAxes(self):
        axs = self._getAxes()
        [ax.cla() for ax in axs]

    def createSubplots(self,*args,**kwargs):
        nrows = self._nrows
        ncols = self._ncols
        num = self.figname
        sharex = self._sharex
        sharey = self._sharey
        f,axs = plt.subplots(nrows,ncols,num=num,
                    sharex=sharex,sharey=sharey,*args,**kwargs)
        self.axs = axs
        return f, axs

    def _getAxes(self):
        axs = self.figure.get_axes()
        axs = [axs] if not isinstance(axs, list) else axs
        return axs

    def setFigureSize(self):
        self.figure.set_size_inches(*self.figsize) 

    def drawFigure(self):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def generateTitleStr(self,data):
        ts_str = hf.getCycleStampLocalTz(data).strftime('(%d.%m.%Y - %H:%M:%S)')
        user = hf.getSelector(data)
        return user+' '+ts_str

    def saveFigure(self,filename):
        pass

class ECLOUD(PlottingClassSPS):

    def __init__(self, devices, mode= '1D', figsize=(10, 10), *args, **kw):
        super().__init__(figsize,*args,**kw)
        self._nrows = 2
        self._ncols = 2
        self._sharex = True
        self._sharey = True
        self._leftmargin = 0.1
        self._rightmargin = 0.02
        self._bottommargin = 0.05
        self._topmargin = 0.05
        self._hspace = 0.11
        self._subhspace = 0.05
        self._wspace = 0.11
        self._width = (1-self._wspace*(self._ncols-1)-\
                    self._leftmargin-self._rightmargin)/self._ncols
        self._height = (1-self._hspace*(self._nrows-1)-\
                    self._bottommargin-self._topmargin)/self._nrows
        self._sptopheightratio = 0.3
        self.initializeFigure()
        self.devices = devices
        self.mode = mode
        self.liner = {}
        self.liner['BESCLD-VECM11733/Acquisition'] = ' (Cu-LESS, cleaned)'
        self.liner['BESCLD-VECM11737/Acquisition'] = ' (SS-MBB, fresh)'
        self.liner['BESCLD-VECM11738/Acquisition'] = ' (CNe13 - since 2008)'
        self.liner['BESCLD-VECM11754/Acquisition'] = ' (Cr2O3 on Al - for M. Barnes)'
        self.deadChannels = {l: [] for l in self.liner.keys()}
        self.deadChannels['BESCLD-VECM11754/Acquisition'].append(34)
        self.deadChannels['BESCLD-VECM11737/Acquisition'].append(14)
        self.signalInversion = {l: 1 for l in self.liner.keys()}
        #self.signalInversion['BESCLD-VECM11754/Acquisition'] = 1
        self._nChannelsMax = 48

    def createSubplots2(self,*args,**kwargs):
        nrows = self._nrows
        ncols = self._ncols
        num = self.figname
        sharex = self._sharex
        sharey = self._sharey
        leftmargin = self._leftmargin
        rightmargin = self._rightmargin
        bottommargin = self._bottommargin
        topmargin = self._topmargin
        hspace= self._hspace
        subhspace = self._subhspace
        wspace = self._wspace
        width = self._width
        height = self._height
        sptopheightratio = self._sptopheightratio
        axes = []
        for i in range(ncols):
            axes.append([])
            for j in np.arange(nrows)[::-1]:
                xmin = leftmargin+i*width+(i)*wspace
                ymin = bottommargin+j*height+(j)*hspace
                topheight = sptopheightratio*(height-subhspace)
                topymin = ymin+subhspace + (height-subhspace)*(1-sptopheightratio)
                sp1=self.figure.add_axes([xmin,topymin,width,topheight])
                bottomheight = (1-sptopheightratio)*(height-subhspace)
                sp2=self.figure.add_axes([xmin,ymin,width,bottomheight])
                axes[i].extend([sp1,sp2])
        self.axs = np.array(axes).T
        if self._sharex:
            for i in range(ncols):
                for j in np.arange(nrows):
                    axes[i][2*j].get_shared_x_axes().join(axes[i][2*j],axes[0][0])
                    axes[i][2*j+1].get_shared_x_axes().join(axes[i][2*j+1],axes[0][1])
        if self._sharey:
            for i in range(ncols):
                for j in np.arange(nrows):
                    axes[i][2*j].get_shared_y_axes().join(axes[i][2*j],axes[0][0])
                    axes[i][2*j+1].get_shared_y_axes().join(axes[i][2*j+1],axes[0][1])
        return self.figure, self.axs

    '''
    def plot(self, data):
        if not plt.fignum_exists(self.figname):
            return
        self.clearFigure()
        figure, axs = self.createSubplots()
        for j, device in enumerate(self.devices):
            ax = axs.flatten()[j]
            d = data[device]['value']
            n_channels, n_meas_2d = d['sem2DRaw'].shape
            n_meas_eff = d['nbOfMeas']
            d['sem2DRaw'] = d['sem2DRaw'].astype(np.float) / d['totalGain']
            d['sem2DRaw'][self.deadChannels[device], :] = np.nan
            d['sem2DRaw'] = d['sem2DRaw'][:self._nChannelsMax,:]
            position = (np.arange(self._nChannelsMax)-self._nChannelsMax/2)*2.17
            if self.mode == '2D':   
                ax.pcolormesh(position, d['measStamp'], 
                    d['sem2DRaw'][:, :n_meas_eff].T, shading='nearest')
            elif self.mode == '1D':
                cmap = matplotlib.cm.get_cmap('viridis')
                for ii in range(n_meas_eff):
                    c = cmap(float(ii)/n_meas_eff)
                    ax.plot(position,-d['sem2DRaw'][:, ii],c=c)
            else:
                print('WARNING, mode=',self.mode,' not understood')
            title_str = device.split('/')[0] + self.liner[device]
            ax.set_title(title_str + '\n' + self.generateTitleStr(data[device]), fontsize=10)
            ax.xaxis.set_tick_params(labelbottom=True)
            ax.yaxis.set_tick_params(labelleft=True) #
            ax.set_xlabel('Position (mm)')
        ax.set_ylim(bottom=-0.02*ax.get_ylim()[1])
        if self.mode == '2D':
            [ax.set_ylabel('Cycle time (ms)') for ax in self.axs[:,0]]
        elif self.mode == '1D':
            [ax.set_ylabel('e-cloud signal (a.u.)') for ax in self.axs.flatten()]#[:,0]]
        plt.tight_layout()
        self.drawFigure()
    '''

    def plot(self, data):
        if not plt.fignum_exists(self.figname):
            return
        self.clearFigure()
        figure, axs = self.createSubplots2()
        for j, device in enumerate(self.devices):
            d = data[device]['value']
            n_channels, n_meas_2d = d['sem2DRaw'].shape
            n_meas_eff = d['nbOfMeas']
            signal = d['sem2DRaw'].astype(np.float) / d['totalGain'] 
            signal[self.deadChannels[device], :] = np.nan
            signal *= self.signalInversion[device]
            signal = signal[:self._nChannelsMax,:]
            signal_sum = np.nansum(signal,axis=0)
            position = (np.arange(self._nChannelsMax)-self._nChannelsMax/2)*2.17
            ax = axs.T.flatten()[j*2+1]
            axt = axs.T.flatten()[j*2]
            if self.mode == '2D':   
                ax.pcolormesh(position, d['measStamp'], 
                    signal[:, :n_meas_eff].T, shading='nearest')
                ax.set_ylabel('Cycle time (ms)')
            elif self.mode == '1D':
                cmap = matplotlib.cm.get_cmap('viridis')
                for ii in range(n_meas_eff):
                    c = cmap(float(ii)/n_meas_eff)
                    ax.plot(position,signal[:, ii],c=c)
                ax.set_ylabel('e-cloud signal (a.u.)')
            else:
                print('WARNING, mode=',self.mode,' not understood')
            axt.plot(d['measStamp'],signal_sum[:n_meas_eff],'r')
            axt.set_xlabel('Cycle time (ms)')
            axt.set_ylabel('e-cloud signal \nintegrated (a.u.)')
            title_str = device.split('/')[0] + self.liner[device]
            axt.set_title(title_str + '\n' + self.generateTitleStr(data[device]), fontsize=10)
            ax.xaxis.set_tick_params(labelbottom=True)
            ax.yaxis.set_tick_params(labelleft=True) #
            ax.set_xlabel('Position (mm)')
        ax.set_ylim(bottom=-0.02*ax.get_ylim()[1])
        self.drawFigure()


