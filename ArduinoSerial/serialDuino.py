import serial
from time import sleep, time, strftime
from sys import exit

# import matplotlib
# matplotlib.use('GTKAgg')

# from pylab import array, loadtxt, plot, plot_date, savefig, strpdate2num, xlabel, ylabel, shape, gca, linspace, figure, gcf
from datetime import datetime

#from matplotlib.dates import MinuteLocator
# from matplotlib.dates import DAILY, MINUTELY

class SerialDuino():
	def __init__(self,port='/dev/ttyUSB0',baudrate=38400,waitTime=0.05):
		self.name='Arduino'
		self.port=port
		self.waitTime=waitTime	# time to wait after sending a command for the Arduino to have responded

		self.ser=serial.Serial()
		self.ser.port=port
		self.ser.baudrate=baudrate


		self.ser.open()
		self.ser.flushInput()
		print('SerialDuino.__init__():: opened serial port '+self.port)

		##### wait until the arduino reports it is ready, as each time a serial port is opened the arduino is reset... (for some bizarre reason!!!)
#		print 'sleeping 5s for arduino to reset'
		sleep(5.0)

#		print 'here'
# 		m=0
# 		while (int(self.ser.inWaiting())<2):	# waits for 7 characters on the serial port: "ready\r\n"
# 			sleep(0.1)
# 			m=m+1
# 			if m>20:
# 				self.ser.write('++')

# 		sleep(0.1)
# 		num=self.ser.inWaiting()

# 		response=self.ser.read(num).rstrip()

# 		if '++' in response:
# 			print('Arduino is ready!')
# 		else:
# 			print('ERROR: SerialDuino:: invalid response: '+response)
# 			exit()

# 		self.ser.flushInput()


	def __del__(self):
		self.ser.close()
		print('SerialDuino.__del__():: closed serial port '+self.port)


	def send(self,cmd):
		self.ser.write(cmd)
		return

	def sendReceive(self,cmd):
#		self.ser.flushInput()
		self.ser.write(cmd)
		sleep(self.waitTime)

#		num=self.ser.inWaiting()

		if 1:
#			while self.ser.inWaiting()==0:
#				sleep(self.waitTime)
			response=self.ser.readline().rstrip()

		if 0:
			while self.ser.inWaiting()==0:
				sleep(self.waitTime)

			num=self.ser.inWaiting()
			print(num)

			response=self.ser.read(num).rstrip()

#		print self.name + ' at '+self.port + ' reports: ' + response
		return response

	def get(self,cmd):
		ret=''
		response=-1

		if 'temperature' in cmd:
			resp=self.sendReceive('T?')
			ret=float(resp)
			response=resp+'C'
		elif 'pt1000' in cmd:
			resp=self.sendReceive('pt1000?')
			ret=float(resp)
			response=resp+'C'
		elif 'humidity' in cmd:
			resp=self.sendReceive('H?')
			ret=float(resp)
			response=resp+'\%'
		elif 'name' in cmd:
			resp=self.sendReceive('*idn?')
			response=resp
			ret=resp
		elif 'position' in cmd:
			resp=self.sendReceive('x?')
			response=resp
			ret=float(resp)


		return response, ret


	def updateLog(self, T=0.0, H=0.0, T2=0.0):
		currtime=strftime("%H:%M:%S")
		f=open('log.txt','a')
		outstr='%s, %4.3f, %4.3f, %4.3f\n' % (currtime, T, H, T2)
		f.write(outstr)
		f.close()


# 	def updateFigure(self):
# 		logtime=[]
# 		humidity=[]
# 		temp=[]
# 		temp2=[]

# 		f=open('log.txt','r')
# 		for line in f:
# 			time_obj = datetime.strptime(line.split(',')[0], '%H:%M:%S')
# 			logtime.append(time_obj)
# 			temp.append(float(line.split(',')[1]))
# 			humidity.append(float(line.split(',')[2]))
# 			temp2.append(float(line.split(',')[3]))

# 		f.close()
# 	
# 		figure(figsize=(9,5))

# 		plot(array(logtime),array(temp2),'bo-')
# 		ax=gca()
# #		loc = ax.xaxis.get_major_locator()
# #		loc.maxticks[MINUTELY] = 7
# #		loc.maxticks[MINUTELY] = 7
# 		gcf().autofmt_xdate()

# 		xlabel('Time')
# 		ylabel('Temperature $\circ$C')
# 		savefig('static/log.png')


if __name__=='__main__':

	if 0:
		t1=time()
		a=SerialDuino()
		t2=time()
		print(t2-t1)

		t1=time()
		out=a.sendReceive('*idn?')
		t2=time()
		print(t2-t1)

		t1=time()
		out=a.sendReceive('*idn?')
		t2=time()
		print(t2-t1)

		t1=time()
		out=a.sendReceive('*idn?')
		t2=time()
		print(t2-t1)


	a=SerialDuino(port='/dev/ttyACM0')  # initialising an instance of arduino class

	for m in range(10):
		print(m, a.get('position')[1])
		sleep(1.0)


	if 0:
		t1=time()
		T=a.get('temperature')[1]
		t2=time()
	#	print(t2-t1)

		t1=time()
		H=a.get('humidity')[1]
		t2=time()
	#	print(t2-t1)
		print(T, H)

		a.updateLog(T=T,H=H,T2=0)
		a.updateFigure()


'''--------------------------------------------------------------------------------------------------------------------
----------------------------------------------LIBRARIES AND CONSTANTS--------------------------------------------------
--------------------------------------------------------------------------------------------------------------------'''


'''--------------------------------------------------------------------------------------------------------------------
----------------------------------------------------FUNCTIONS----------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------'''



'''--------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------MAIN CODE---------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------'''
# arduino = serial.Serial(port='COM5', baudrate=38400, timeout=.1)

'''--------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------CODE ENDS---------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------'''
