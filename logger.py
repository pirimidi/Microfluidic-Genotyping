"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: May 19, 2011.

 For: PDMS microdevice-based genotyping project automation [temperature 
 controller software] at the Ju Lab - Chemical Engineering Department, 
 Columbia University.
 
 Purpose: This program contains the complete code for class Logger, containing
 device operation logging facility in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

import os
import time
import logging

class Logger:

	def __init__(self, config):
		"""Initialize logging facility with default parameters"""

		if os.access(config.get("communication","log_dir"), os.F_OK) is False:
			os.mkdir(config.get("communication","log_dir"))

		logging.basicConfig(level=logging.DEBUG,	# set logger format configuration parameters
				    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
				    datefmt='%m-%d %H:%M:%S',
				    filename = config.get("communication","log_dir") + 'pcr_process.log',
				    filemode='a')

		formatter = logging.Formatter('%(levelname)-8s %(message)s')	# set a format which is simpler for console use

		console = logging.StreamHandler()	# define a Handler which writes INFO messages or higher to the sys.stderr
		console.setLevel(logging.INFO)
		console.setFormatter(formatter)	# tell the handler to use this format
		logging.getLogger('').addHandler(console)	# add the handler to the root logger

		loglevel = 1

	def log(self, level, message):
		"Forwards log messages to the logging module instance."
		logging.log(level,message)

	def warn(self, message):
		"Diplays a warning message via logging facility."
		logging.warn(message)

	def info(self, message):
		"Diplays an informative message via logging facility."
		logging.info(message)

	def error(self, message):
		"Diplays an error message via logging facility."
		logging.error(message)

	def debug(self, message):
		"Diplays a debugging message via logging facility."
		logging.debug(message)

