#!/usr/local/bin/python

"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: June 2, 2011.

 For: PDMS microdevice-based (with off-chip temperature control) genotyping 
 project automation [temperature controller software] at the Ju Lab - Chemical 
 Engineering Department, Columbia University.
 
 Purpose: Performs a 10 uL PCR cycle consisting of the following 
 schematics:
 
 1. 24-94 C -> hold for 15 s (denaturation step)
 2. 94-57 C -> hold for 30 s (annealing step)
 3. 57-70 C -> hold for 75 s (elongation step)
 4. 70-72 C -> hold for 2 min (final elongation)
 5. 72-4  C -> hold for infinity (final hold)

 to determine the control-channel temperature correlation function.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file.
-------------------------------------------------------------------------------- 
"""

import sys
import time
import commands

import auxil
import serial
import ConfigParser
from logger import Logger

from temperature_control import Temperature_control

#------------------------- Configuration file handling ---------------------------------

print '\nINFO\t *\t--> START GENOTYPING PCR MAIN - genotyping_pcr.py\n'

config = ConfigParser.ConfigParser()  # Create configuration file parser object.
config.read('config.txt')  # Fill it in with configuration parameters from file.

#--------------------- Serial port / logging initialization ----------------------------

logger = Logger(config)  # Create logger object.

serial = serial.Serial(0)  # Create serial port object.
serial.port = config.get("communication","serial_port")  # Set appropiate serial port. 
logger.info("-\t--> Serial connection established")

#--------------------- Temperature controller initialization --------------------------
 
t0 = time.time()  # Initial time stamp for log-file.
temperature_control = Temperature_control(config, serial, logger)  # Initialize temperature controller object.

if temperature_control.speech_option == 1:
	commands.getstatusoutput('mplayer -ao pulse ../speech/welcome.wav')
	commands.getstatusoutput('mplayer -ao pulse ../speech/start.wav')

logger.info("*\t--> Started genotyping PCR")

log_dir = config.get("communication", "log_dir")  # Get log directory from configuration parameters.
temperature_control.logfile = open(log_dir + 'pcr_temperature.log', 'w')

temperature_control.set_control_on()  # Turn temperature controller on.
temperature_control.pcr_wo_trigger()  # Perform PCR protocol on reagent in genotyping chip (without trigger points).
#temperature_control.pcr_wi_trigger()  # Perform PCR protocol on reagent in genotyping chip (with trigger points).
temperature_control.set_control_off()  # Turn temperature controller off.

delta = (time.time() - t0) / 60  # Calculate elapsed time for PCR protocol.
logger.warn("*\t--> Finished genotyping PCR - duration: %.2f minutes" % delta)

if biochem.speech_option == 1:
	commands.getstatusoutput('mplayer -ao pulse ../speech/end.wav')

print 'INFO\t *\t--> END GENOTYPING PCR MAIN - genotyping_pcr.py\n'

