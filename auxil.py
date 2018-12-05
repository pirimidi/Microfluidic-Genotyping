#!/usr/local/bin/python

"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: May 19, 2011.

 For: PDMS microdevice-based (with off-chip temperature control) genotyping 
 project automation [temperature controller software] at the Ju Lab - Chemical 
 Engineering Department, Columbia University.
 
 Purpose: This program contains the utility functions for the 5R7-001
 temperature controller auxiliary subroutines in Python.

 Calibration curve: The temperature correlation function can be determined by 
 simultaneously measuring the temperature on the top of the Peltier element
 [INPUT 1 sensor] and on the top of the glass slide [INPUT 2 sensor]. 

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

import math
import time

def set_command(command, value):
	"""Return the controlling ASCII string of commands in hexadecimal format translated 
	from command and decimal value arguments"""
	
	value = int(math.ceil(value))

	sum = 0
	cmd = '*00' + command + '0000000000\r'
	cml = list(cmd)

	if (value == 0 or value == 1):  
		h = hex(value).split('x')[1]
		cml[12] = h[-1]

	elif value != 'NA':
		h = hex(value).split('x')[1]

		if len(h) == 4:
			cml[9] = h[-4]
			cml[10] = h[-3]
			cml[11] = h[-2]

		if len(h) == 3:
			cml[10] = h[-3]
			cml[11] = h[-2]

		if len(h) == 2:
			cml[11] = h[-2]

		cml[12] = h[-1]

	for x in range(1, 13):
		sum += ord(cml[x])

	cs = hex(sum%256).split('x')[1]

	if len(cs) == 1:
		cml[14] = cs[0]

	else:
		cml[13] = cs[0]
		cml[14] = cs[1]

	return "".join(cml)

def get_response(response):
	"""Return the ASCII string of response in decimal format translated 
	from serial port response in hexadecimal format"""

	time.sleep(0.1)
	res = '****'
	rel = list(res)

	rel[0] = response[-7]
	rel[1] = response[-6]
	rel[2] = response[-5]
	rel[3] = response[-4]

	return '%.4f' % (float(int("".join(rel), 16)))

def check_sum(command):
		"""Return the controlling ASCII string of commands in hexadecimal format translated 
		from read command argument"""

		sum = 0
		cmd = '*00' + command + '0000000000\r'
		cml = list(cmd)

		for x in range(1, 13):
			sum += ord(cml[x])

		cs = hex(sum%256).split('x')[1]

		if len(cs) == 1:
			cml[14] = cs[0]

		else:
			cml[13] = cs[0]
			cml[14] = cs[1]

		return "".join(cml)

