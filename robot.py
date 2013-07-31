import numpy as np
import time
import pyfirmata
import serial
import os
import weather
import tweet
import pygame
from MyThread import *

board = pyfirmata.Arduino('/dev/ttyACM0')
print "Setting up the connection to the board ..."
iter = pyfirmata.util.Iterator(board)
iter.start()
# Start reporting for defined pins
pin3 = board.get_pin('d:3:p')
PINS = (0,1,2)
pin2 = board.get_pin('d:2:i')
pin2.enable_reporting
pin12 = board.get_pin('d:12:i')
pin2.enable_reporting
DEBUG = 0
sev_seg_led = 1

# Init Sound Pool
pygame.mixer.init()

for pin in PINS:
    board.analog[pin].enable_reporting()


def input():
    	print "reading.."
	d = 1
	bflag = 1 
	global sev_seg_led
	global DEBUG
	global oldstate
	while 1:
		if pin2.read() == 1 and sev_seg_led <= 8:
			sev_seg_led = sev_seg_led + 1
			oldstate = 0
		if pin12.read() == 1 and sev_seg_led >= 1:
			sev_seg_led = sev_seg_led - 1
			oldstate = 0			
		board.pass_time(0.4)
	board.exit()

def led():
	x = 0.0
 	a = 0.05
	while 1:
		if x == 1 or x == 0:
			a = -a
		x = np.sum(x,a)			
		pin3.write(x)			

def volControl():

        while True:
		pygame.mixer.music.set_volume(float(board.analog[0].read()))
		time.sleep(0.4)

def terminate():
	while 1:
		#print pin2.read()

		if board.analog[2].read() < 0.002:
			print 'Light control TRIGGER>>>>>>!!!!'
				#w.kill()
			board.digital[13].write(1)
			time.sleep(1)
			board.digital[13].write(0)
		


def sevenSegWrite(digit):
	s_pin = 4

	for i in range(7):
		board.digital[s_pin].write(seven_seg_digits[digit][i])
		s_pin = s_pin + 1 	

def channel(i):
	pygame.mixer.music.load('channel/c'+ str(i) +'.mp3')
	if sev_seg_led == 9:
		pygame.mixer.music.load('channel/error.mp3')
	pygame.mixer.music.play(0)		
########
zero = [0,0,0,1,0,0,0]
one = [0,1,1,1,0,1,1]
two = [0,0,1,0,1,0,0]
three  = [0,0,1,0,0,0,1]
four = [0,1,0,0,0,1,1]
five = [1,0,0,0,0,0,1]
six = [1,0,0,0,0,0,0]
seven = [0,0,1,1,0,1,1]
eight = [0,0,0,0,0,0,0]
nine = [0,0,0,0,0,0,1]

seven_seg_digits = [zero,one,two,three,four,five,six,seven,eight,nine]

##########

t = MyThread(target = input)
t.start()

#led = MyThread(target = led)
#led.start()

vol = MyThread(target = volControl)
vol.start()

stop = MyThread(target = terminate)
stop.start()
	
oldstate = 0

while 1:
	sevenSegWrite(sev_seg_led)
	if oldstate == 0:
		if pygame.mixer.music.get_busy() == 1:
			pygame.mixer.music.stop()
		channel(sev_seg_led)
		oldstate = 1
	pass
