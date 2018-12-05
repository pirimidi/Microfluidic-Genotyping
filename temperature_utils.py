#!/usr/local/bin/python

"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: June 13, 2011.

 For: PDMS microdevice-based genotyping project automation [temperature 
 controller software] at the Ju Lab - Chemical Engineering Department, 
 Columbia University.

 Purpose: given function command, this utility program performs any temperature 
 controller method contained in temperature controller module.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file.
------------------------------------------------------------------------------- 
"""

import sys
import time
import commands

#----------------------------- Input argument handling ---------------------------------

if len(sys.argv) == 1:
	print """\n
     ----------------------------------------------------------------------   
     -                                                                    -      
     -        WELCOME TO THE TEMPERATURE CONTROLLER UTILITY PROGRAM       -
     -                                                                    -
     -             Usage: python temperature_utils.py <method>            -
     -                                                                    -
     ----------------------------------------------------------------------

     |  Methods defined here:
     |  
     |  get_config_parameters(self)
     |      Retieves all temperature controller related configuration parameters from the confi-
     |      guration file using the ConfigParser facility. It assigns each parameter to a field of 
     |      the temperature controller object, thus it can access it any time during a run.
     |  
     |  get_control_temperature(self):
     |	    Gets control temperature sensor reading, a float.
     |
     |  get_D_gain(self):
     |	    Gets derivative gain in PID control, a float. 
     |
     |  get_I_gain(self):
     |	    Gets integral gain in PID control, a float.   
     |
     |  get_P_bandwidth(self):
     |	    Gets proportional bandwidth in PID control, a float.  
     |
     |  get_periphery_temperature(self):
     |      Gets periphery temperature sensor reading, a float.
     |
     |	get_set_temperature(self):
     |	    Gets set temperature value of temperature controller, a float.
     |  
     |  incubate_reagent(self, time_sec)
     |      Incubates reagent for given amount of time and dynamically counts elapsed time 
     |      in seconds to update user about incubation state.
     |
     |  log_temperature(self)
     |      Records target temperature related parameters of biochip into a log-file.
     |
     |  monitor_temperature(self)
     |      Prints continuous temperature log into console in (time, control sensor tempearture)
     |      format. Units are in 's' and 'C' respectively.
     |
     |  monitor_parameters(self)
     |      Prints continuous temperature log into console in (time, set, control probe, periphery sensor, 
     |      target temperatures and relative power output) format. Units are in 's', 'C' and '%'
     |      respectively.
     |
     |  pcr_wi_trigger(self):
     |	    Performs PCR cycle in gene-chip (with trigger points).
     |
     |  pcr_wo_trigger(self):
     |	    Performs PCR cycle in gene-chip (without trigger points).
     |
     |  pull_trigger(self, poll_temp, tolerance=None):
     |      Breaks out of a temperature ramping procedure defined by a previous temperature
     |	    set point at a given trigger point. This function can set a step-wise ramping,
     |      providing a steeper temperature ramping curve.
     |
     |  sample_parameters(self)
     |      Records contious target temperature related parameters of biochip into a log-file.
     |  
     |  set_control_off(self)
     |      Clears RUN flag in regulator, so main output is blocked.
     |  
     |  set_control_on(self)
     |      Sets RUN flag in regulator, so main output is opened.
     |  
     |  set_temperature(self, temperature)
     |      Sets main temperature reference (C), a float.
     |
     |	set_P_bandwidth(self, pb)
     |	    Sets proportional bandwidth in PID control, a float".
     |
     |	set_I_gain(self, pb)
     |	    Sets integral gain in PID control, a float".
     |
     |	set_D_gain(self, pb)
     |	    Sets derivative gain in PID control, a float".
     |  
     |  wait_for_SS(self, set_temp, tolerance=None)
     |      Waits until steady-state temperature is reached, or exits wait block if ramping
     |      time exceeds time limit parameter set in configuration file."""
	
	print "\n"
	sys.exit()

elif len(sys.argv) < 2:
	print '\n--> Error: not correct input!\n--> Usage: python temperature_utils.py <method>\n'
	sys.exit()

else:
	import auxil
	import serial
	import ConfigParser
	from logger import Logger

	from temperature_control import Temperature_control

	#------------------------- Configuration file handling ---------------------------------

	print '\nINFO\t -\t--> Process started - temperature_utils.py'  # start process

	config = ConfigParser.ConfigParser()  # create configuration file parser object
	config.read('config.txt')  # fill it in with configuration parameters from file

	#--------------------- Serial port / logging initialization ----------------------------

	t0 = time.time()  # get current time
	logger = Logger(config)  # create logger object

	serial = serial.Serial(0)  # create serial port object
	serial.port = config.get("communication","serial_port")  # set appropiate serial port 
	logger.info("-\t--> Serial connection established")

	temperature_control = Temperature_control(config, serial, logger)  # initialize temperature controller object

	log_dir = config.get("communication", "log_dir")  # get log directory from configuration parameters.
	temperature_control.logfile = open(log_dir + 'pcr_temperature.log', 'w')

	#---------------------------------------------------------------------------------------
	#				TEMPERATURE CONTROLLER FUNCTIONS
	#---------------------------------------------------------------------------------------

	logger.info('-\t--> Started %s method execution - temperature_utils.py' % sys.argv[1])
	method = sys.argv[1]  # set method to second argument

	if method == 'get_config_parameters':
		temperature_control.get_config_parameters()

	elif method == 'get_control_temperature':
		pt = temperature_control.get_control_temperature()
		print "INFO\t -\t--> Current control temperature: %0.2f C" % pt

	elif method == 'get_periphery_temperature':
		gt = temperature_control.get_periphery_temperature()
		print "INFO\t -\t--> Current periphery temperature: %0.2f C" % gt

	elif method == 'get_set_temperature':
		st = temperature_control.get_set_temperature()
		print "INFO\t -\t--> Desired set temperature: %0.2f C" % st

	elif method == 'get_D_gain':
		dg = temperature_control.get_D_gain()
		print "INFO\t -\t--> Current derivative gain: %0.2f" % dg

	elif method == 'get_I_gain':
		ig = temperature_control.get_I_gain()
		print "INFO\t -\t--> Current integral gain: %0.2f" % ig

	elif method == 'get_P_bandwidth':
		pb = temperature_control.get_P_bandwidth()
		print "INFO\t -\t--> Current proportional bandwidth: %0.2f" % pb

	elif method == 'incubate_reagent':
		print "INFO\t -\t--> Please, enter seconds of incubation time [int]: ",
		it = int(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		temperature_control.set_temperature(it)

	elif method == 'log_temperature':
		print "INFO\t -\t--> Please, enter a desired target temperature [float]: ",
		target = float(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		temperature_control.log_temperature()

	elif method == 'monitor_temperature':
		temperature_control.monitor_temperature()

	elif method == 'monitor_parameters':
		temperature_control.monitor_parameters()

	elif method == 'pcr_wi_trigger':
		temperature_control.pcr_wi_trigger()

	elif method == 'pcr_wo_trigger':
		temperature_control.pcr_wo_trigger()

	elif method == 'pull_trigger':
		print "INFO\t -\t--> Please, enter: poll_temp, tolerance separated by single space [floats]: ",
		v = sys.stdin.readline().strip().split(' ')  # use stdin explicitly and remove trailing newline character
		temperature_control.pull_trigger(float(v[0]), float(v[1]))

	elif method == 'sample_parameters':
		temperature_control.sample_parameters()

	elif method == 'set_control_off':
		temperature_control.set_control_off()

	elif method == 'set_control_on':
		temperature_control.set_control_on()

	elif method == 'set_temperature':
		print "INFO\t -\t--> Please, enter desired target set temperature [float]: ",
		temperature = float(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		temperature_control.set_temperature(temperature)

	elif method == 'set_P_bandwidth':
		print "INFO\t -\t--> Please, enter desired proportional bandwidth value [float]: ",
		pb = float(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		temperature_control.set_P_bandwidth(pb)

	elif method == 'set_I_gain':
		print "INFO\t -\t--> Please, enter desired integral gain value [float]: ",
		ig = float(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		temperature_control.set_I_gain(ig)

	elif method == 'set_D_gain':
		print "INFO\t -\t--> Please, enter desired derivative gain value [float]: ",
		dg = float(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		temperature_control.set_D_gain(dg)

	elif method == 'wait_for_SS':
		print "INFO\t -\t--> Please, enter: set_temp, tolerance separated by single space [floats]: ",
		v = sys.stdin.readline().strip().split(' ')  # use stdin explicitly and remove trailing newline character
		temperature_control.wait_for_SS(float(v[0]), float(v[1]))

	else:
		print '\nWARN\t -\t--> Error: not correct method input!\nWARN\t -\t--> Double check method name (2nd argument)\n'
		sys.exit()

	#-------------------------- Duration of temperature_controlistry test ------------------------------

	delta = (time.time() - t0) / 60  # Calculate elapsed time for flowcell flush.
	logger.info('-\t--> Finished %s method execution - duration: %0.2f minutes\n' % (method, delta))

