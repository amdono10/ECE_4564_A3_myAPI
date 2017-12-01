import RPi.GPIO as GPIO
import time
from zeroconf import Zeroconf

from flask import Flask, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

red   = GPIO.PWM(20, 100)
green = GPIO.PWM(21, 100)
blue  = GPIO.PWM(22, 100)

red.start(0)
green.start(0)
blue.start(0)

status = 'off'
color = 'none'
intensity = 0

@app.route("/LED", methods = ['GET', 'POST'])
def LED():
	global status
	global color
	global intensity
	
	if request.method == 'GET':
		return 'status: %s, color: %s\n' % (status, color)
		
	if request.method == 'POST':
		status = request.args.get('status')
		color = request.args.get('color')
		intensity = request.args.get('intensity')
	
		if(status == 'off'):
			red.ChangeDutyCycle(0)
			green.ChangeDutyCycle(0)
			blue.ChangeDutyCycle(0)
			
			return('LED set to off.\n')
			
		elif(status == 'on'):
			if(color == 'red'):
				red.ChangeDutyCycle(int(intensity))
				green.ChangeDutyCycle(0)
				blue.ChangeDutyCycle(0)	
				
				return('LED set to red.\n')
				
			elif(color == 'green'):
				red.ChangeDutyCycle(0)
				green.ChangeDutyCycle(int(intensity))
				blue.ChangeDutyCycle(0)	
				
				return('LED set to green.\n')
				
			elif(color == 'blue'):
				red.ChangeDutyCycle(0)
				green.ChangeDutyCycle(0)
				blue.ChangeDutyCycle(int(intensity))	
				
				return('LED set to blue.\n')
				
			elif(color == 'yellow'):
				red.ChangeDutyCycle(int(intensity))
				green.ChangeDutyCycle(int(intensity))
				blue.ChangeDutyCycle(0)	
				
				return('LED set to yellow.\n')
				
			elif(color == 'cyan'):
				red.ChangeDutyCycle(0)
				green.ChangeDutyCycle(int(intensity))
				blue.ChangeDutyCycle(int(intensity))	
				
				return('LED set to cyan.\n')
				
			elif(color == 'purple'):
				red.ChangeDutyCycle(int(intensity))
				green.ChangeDutyCycle(0)
				blue.ChangeDutyCycle(int(intensity))	
				
				return('LED set to purple.\n')
				
			elif(color == 'white'):
				red.ChangeDutyCycle(int(intensity))
				green.ChangeDutyCycle(int(intensity))
				blue.ChangeDutyCycle(int(intensity))	
				
				return('LED set to white.\n')
				
			else:
				return('LED not changed')

try:
	if __name__ == "__main__":
		app.run(host = '0.0.0.0', port = 5000, debug = True)
	
except KeyboardInterrupt:
	red.stop()
	green.stop()
	blue.stop()
	GPIO.cleanup()
