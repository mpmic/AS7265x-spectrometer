# Script to test spectrometer.py
import spectrometer as spect
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

"""
#spectrometer members:
def init()
def boardPresent()
def hwVersion()
def swVersion()
def temperatures()
def setBlueLED(state)
def shutterLED(device,state)
def setLEDDriveCurrent(current)
def setIntegrationTime(time)
def setGain(gain)
def readRAW()
def readCAL()
"""

fname = '/home/pi/python/'							# Directory for results data


def newFile(fname):

    # Open a unique file for the results data
    t = datetime.datetime.now()

    year = str(t.year)
    month = str(t.month)
    day = str(t.day)
    hour = str(t.hour)
    min = str(t.minute)

    fname = fname + 'spectrumdata' + year + \
        month.zfill(2) + day.zfill(2) + "time" + \
        hour.zfill(2) + 'h' + min.zfill(2) + '.txt'
    fh = open(fname, 'w')

    return fh

# Test read of all calibrated and raw values


def ReadAllData():

    # Desired time in secs for total run. 3600 secs per hour. 60 secs per minute.
    duration = 3600 * 20
    # Sleep seconds between passes (interval between measurements)
    sleepPeriod = 60 * 10
    # Board compute time per cycle (1 pass of RAW and CAL data fetch)
    procTime = 6
    passes = int(duration / (sleepPeriod + procTime))
    print("Test duration(s): " + str(duration) + " Sleep period: " +
          str(sleepPeriod) + " Number of Passes: " + str(passes))

    print("Start time: " + str(datetime.datetime.now()))

    fhandle = newFile(fname)

    count = 0
    while (count < passes):

        print(count)

        RAWvalues = spect.readRAW()
        CALvalues = spect.readCAL()

        string = ""
        for val in RAWvalues:
            string = string + str(val) + ','

        for val in CALvalues:
            string = string + str(val) + ','

        string = string + "\n"
        fhandle.write(string)
        print(string)

        time.sleep(sleepPeriod)
        count = count + 1

    print("End time: " + str(datetime.datetime.now()))
    fhandle.close()


def continuous_read_data(LEDLevel: int,
                        #  gain: int, 
						#  integration_time: int, 
						 refresh_time
						 ,
                         ):
						 
						 
	devices = ("AS72651", "AS72652", "AS72653")


	def animate(i):
		ax.clear()
		ax.set_ylim(0,65535)
		ax.set_title("Wavelength Intensity")
		ax.set_xlabel("Wavelength")
		ax.set_ylabel("Amplitude (units)")

		y = spect.readRAW()
		x = ['410nm', '435nm', '460nm', '485nm', '510nm', '535nm', '560nm', '585nm', '610nm', '645nm', '680nm', '705nm', '730nm', '760nm', '810nm', '860nm', '900nm', '940nm']
		plt.plot(x, y, label = 'Wavelength Intensity')
		
	spect.init()
	
	for device in devices:
		spect.shutterLED(device, True)
	
	spect.setLEDDriveCurrent(LEDLevel)

	# spect.setGain(gain)

	# spect.setIntegrationTime(integration_time)

	ami = FuncAnimation(plt.gcf(), animate, interval = refresh_time)
	

# ---- main()  -----


# spect.init()
# spect.hwVersion()
# 
ReadAllData()
