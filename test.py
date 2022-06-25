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

		ax = plt.gca()
		ax.clear()

		ax.set_title("Wavelength Intensity")
		ax.set_xlabel("Wavelength")
		ax.set_ylabel("Amplitude (units)")

		y_cal = spect.readCAL()
		x = ['410nm', '435nm', '460nm', '485nm', '510nm', '535nm', '560nm', '585nm', '610nm', '645nm', '680nm', '705nm', '730nm', '760nm', '810nm', '860nm', '900nm', '940nm']
		plt.plot(x, y_cal, label = 'Wavelength Intensity')
		
	spect.init()
	
	for device in devices:
		spect.shutterLED(device, True)
	
	spect.setLEDDriveCurrent(LEDLevel)

	# spect.setGain(gain)

	# spect.setIntegrationTime(integration_time)

	ami = FuncAnimation(plt.gcf(), animate, interval = refresh_time)
	plt.show()


def record_data(refresh_time, devs):
	
	
	devices = {"uv":"AS72653", "visible": "AS72652", "infra": "AS72651" }
	
	spect.init()
	
	input("Press enter to start")

	# Turn off all LEDS
	for device in devices.values():
		spect.shutterLED(device, False)


	# Turn on all LEDs in devs
	for device in devices:
		if device in devs.keys():
			spect.shutterLED(device, True)

	with file.open(rf'data/{time.strftime("%Y%m%d-%H%M%S")}', 'a', buffering=1) as fh:
		
		class_name = input("Enter sample name")
		header = """410nm, 435nm, 460nm, 485nm, 510nm, 535nm, 560nm, 585nm, 610nm, 645nm, 680nm, 705nm, 730nm, 760nm, 810nm, 860nm, 900nm, 940nm, class_name"""

		for lid_stage in range(2):
			stage = "Close" if lid_stage==0 else "Open"
			input(f"{stage} the lid now and press enter")

			# Cycle through the currents
			for currents in range(1,4):
				print(f"Current LED intensity level is {currents}")
				spect.setLEDDriveCurrent(LEDLevel)

				y_cal = spect.readCAL()
				"""x = ['410nm', '435nm', '460nm', '485nm', '510nm', '535nm', 
					'560nm', '585nm', '610nm', '645nm', '680nm', '705nm', 
					'730nm', '760nm', '810nm', '860nm', '900nm', '940nm']"""

				fh.write(','.join(y_cal))
				fh.write(f',{class_name}\n')
				

				

			
	





		

# ---- main()  -----


# spect.init()
# spect.hwVersion()
# 
# ReadAllData()
continuous_read_data(3, 1000)
