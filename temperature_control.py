"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: June 13, 2011.

 For: PDMS microdevice-based (with off-chip temperature control) genotyping 
 project automation [temperature controller software] at the Ju Lab - Chemical 
 Engineering Department, Columbia University.
 
 Purpose: This program contains the complete code for class Temperature_control,
 containing 5R7-001 temperature controller communication subroutines to 
 determine control-channel temperature correlation function in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

import os
import sys 
import time

import auxil
import commands

class Temperature_control():

	def __init__(self, config, serial, logger=None):
		"Initialize 5R7-001 temperature controller object with default parameters"

		self.cycle = 0  # initialize pcr cycle loop iteration counter

		if logger is not None:
			self.logging = logger  # if defined, assign logger object to temperature controller

		self.serial = serial  # assign serial port object to temperature controller
		self.config = config  # assign configuration object to temperature controller
		self.get_config_parameters()  # retrieve all configuatrion parameters from file
		self.log_config_parameters()  # register current configuration parameter list

		self.logging.info("-\t--> Temperature controller object constructed")

#--------------------------------------------------------------------------------------#
#		    5R7-001 temperature controller FUNCTIONS     		       #
#--------------------------------------------------------------------------------------#
#
# Performs low-level functional commands (e.g. set target temperature, turns power on, 
# ect). Each command implemented here must know the command set of the hardware being 
# controlled, but does not need to know how to communicate with the device. Each func-
# tional command will block until execution is complete.
#
#--------------------------------------------------------------------------------------#
#				BASIC SETTINGS   				       #
#--------------------------------------------------------------------------------------#

#------------------------ Turn temperature controller ON -------------------------------

	def set_control_on(self):
		"Sets RUN flag in regulator, so main output is opened"

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/control_on.wav')

		self.serial.flushInput()  # flush input buffer
		self.serial.write(auxil.set_command('2d', 1))  # set RUN flag command
		self.logging.info("%i\t--> Set temperature control ON" % self.cycle)

#------------------------ Turn temperature controller OFF ------------------------------

	def set_control_off(self):
		"Clears RUN flag in regulator, so main output is blocked"

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/control_off.wav')

		self.serial.flushInput()  # flush input buffer
		self.serial.write(auxil.set_command('2d', 0))  # clear RUN flag command 
		self.logging.info("%i\t--> Set temperature control OFF" % self.cycle)

#--------------------------------------------------------------------------------------#
#				REGULATOR SETTINGS				       #	
#--------------------------------------------------------------------------------------#

#---------------------------- Set target temperature -----------------------------------

	def set_temperature(self, temperature):
		"Sets main temperature reference (C), a float"

		if self.speech_option == 1:

			if temperature == self.temp1:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_temp1.wav')
			elif temperature == self.temp2:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_temp2.wav')
			elif temperature == self.temp3:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_temp3.wav')
			elif temperature == self.temp4:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_temp4.wav')
			elif temperature == self.temp5:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_temp5.wav')
			elif temperature == self.temp6:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_temp6.wav')
 			else:
				commands.getstatusoutput('mplayer -ao pulse ../speech/set_to_target.wav')

		self.serial.flushInput()  # flush input buffer
		self.serial.write(auxil.set_command('1c', temperature * 100))
		self.logging.info("%i\t--> Set target temperature to %.2f C" % (self.cycle, temperature))

#---------------------------- Set proportional bandwidth -------------------------------

	def set_P_bandwidth(self, pb):
		"Sets proportional bandwidth in PID control, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write(auxil.set_command('1d', pb * 50))
		self.logging.info("%i\t--> Set proportional bandwidth to %.2f" % (self.cycle, pb))

#--------------------------------- Set integral gain -----------------------------------

	def set_I_gain(self, ig):
		"Sets integral gain in PID control, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write(auxil.set_command('1e', ig * 100))
		self.logging.info("%i\t--> Set integral gain to %.2f" % (self.cycle, ig))

#--------------------------------- Set integral gain -----------------------------------

	def set_D_gain(self, dg):
		"Sets derivative gain in PID control, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write(auxil.set_command('1f', dg * 100))
		self.logging.info("%i\t--> Set derivative gain to %.2f" % (self.cycle, dg))

#--------------------------------------------------------------------------------------#
#				 STATUS CHECKING				       #
#--------------------------------------------------------------------------------------#

#---------------------------- Get control temperature ----------------------------------

	def get_control_temperature(self):
		"Gets control temperature sensor reading, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write('*00010000000041\r')
		return float(auxil.get_response(self.serial.read(12)))/100

#--------------------------- Get periphery temperature ---------------------------------

	def get_periphery_temperature(self):
		"Gets periphery temperature sensor reading, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write('*00060000000046\r')
		return float(auxil.get_response(self.serial.read(12)))/100

#------------------------------ Get set temperature ------------------------------------

	def get_set_temperature(self):
		"Gets set temperature value of temperature controller, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write('*00030000000043\r')
		return float(auxil.get_response(self.serial.read(12)))/100


#---------------------------- Get proportional bandwidth -------------------------------

	def get_P_bandwidth(self):
		"Gets proportional bandwidth in PID control, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write('*00510000000046\r')
		return float(auxil.get_response(self.serial.read(12)))/50

#--------------------------------- Get integral gain -----------------------------------

	def get_I_gain(self):
		"Gets integral gain in PID control, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write('*00520000000047\r')
		return float(auxil.get_response(self.serial.read(12)))/100

#--------------------------------- Get integral gain -----------------------------------

	def get_D_gain(self):
		"Gets derivative gain in PID control, a float"

		self.serial.flushInput()  # flush input buffer
		self.serial.write('*00530000000048\r')
		return float(auxil.get_response(self.serial.read(12)))/100

#--------------------------------------------------------------------------------------# 
# 				COMPLEX FUNCTIONS 				       # 
#--------------------------------------------------------------------------------------#

#---------------------------- Log_config_parameters ------------------------------------

	def log_config_parameters(self):
		"""Logs all biochemistry and device related configuration parameters contained in 
		the ConfigParser object using Logger facility."""

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/log_config.wav')


 		if self.log_option == 0:
			self.logging.info("""\n
*********************************************************************   
*                                                                   *      
*              ***  THIS IS THE GENOTYPER LOG-FILE  ***             *
*                                                                   *
*                Current biochemistery parameter set:	            *
*                                                                   *
*********************************************************************\n""")

          		for section in self.config.sections():
             			self.logging.info("[" + section + "]\n")

             			for (key, value) in self.config.items(section):
                 			if key == "__name__":
                     				continue
                 			self.logging.info("%s = %s" % (key, value))
             			self.logging.info("\n")

 		elif self.log_option == 1:

			if os.access(self.config.get("communication","cfg_dir"), os.F_OK) is False:
				os.mkdir(self.config.get("communication","cfg_dir"))

			os.chdir(self.config.get("communication","cfg_dir"))

			from datetime import datetime
			t = datetime.now()
			time = t.strftime('%m-%d-%y %H:%M:%S')
			
			cfg_log = open("parameter_" + time + ".log", 'a')  # open up log-file to be written
			cfg_log.write("""
*********************************************************************   
*                                                                   *      
*              ***  THIS IS THE GENOTYPER LOG-FILE  ***             *
*                                                                   *
*                Current biochemistery parameter set:	            *
*                                                                   *
*********************************************************************\n\n""")

          		for section in self.config.sections():
             			cfg_log.write("[" + section + "]\n\n")

             			for (key, value) in self.config.items(section):
                 			if key == "__name__":
                     				continue
                 			cfg_log.write("%s = %s\n" % (key, value))
             			cfg_log.write("\n")
			cfg_log.close()  # close log-file

 		else:
			print '--> Error: not correct input!\n--> Usage in log-file: [communications] > log_option > 0|1\n'
			sys.exit()

#--------------------------- Get configuration parameters ------------------------------

	def get_config_parameters(self):
		"""Retieves all temperature controller related configuration parameters from the confi-
		guration file using the ConfigParser facility. It assigns each parameter to a field of 
		the temperature controller object, thus it can access it any time during a run."""

		self.logging.info("%i\t--> Retrieve configuration parameters from file" % self.cycle)

		#----------------------- Device communication --------------------------

		self.log_option = int(self.config.get("communication","log_option"))
		self.speech_option = int(self.config.get("communication","speech_option"))

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/get_config.wav')

		#------------------------------ PCR parameters -------------------------------------

		self.loop_iter = int(self.config.get("pcr_parameters","loop_iter"))

		self.P_bandwidth1 = float(self.config.get("pcr_parameters","P_bandwidth1"))
		self.P_bandwidth2 = float(self.config.get("pcr_parameters","P_bandwidth2"))
		self.P_bandwidth3 = float(self.config.get("pcr_parameters","P_bandwidth3"))
		self.P_bandwidth4 = float(self.config.get("pcr_parameters","P_bandwidth4"))
		self.P_bandwidth5 = float(self.config.get("pcr_parameters","P_bandwidth5"))

		self.I_gain1 = float(self.config.get("pcr_parameters","I_gain1"))
		self.I_gain2 = float(self.config.get("pcr_parameters","I_gain2"))
		self.I_gain3 = float(self.config.get("pcr_parameters","I_gain3"))
		self.I_gain4 = float(self.config.get("pcr_parameters","I_gain4"))
		self.I_gain5 = float(self.config.get("pcr_parameters","I_gain5"))

		self.D_gain1 = float(self.config.get("pcr_parameters","D_gain1"))
		self.D_gain2 = float(self.config.get("pcr_parameters","D_gain2"))
		self.D_gain3 = float(self.config.get("pcr_parameters","D_gain3"))
		self.D_gain4 = float(self.config.get("pcr_parameters","D_gain4"))
		self.D_gain5 = float(self.config.get("pcr_parameters","D_gain5"))

		self.temp1 = float(self.config.get("pcr_parameters","temp1"))
		self.temp2 = float(self.config.get("pcr_parameters","temp2"))
		self.temp3 = float(self.config.get("pcr_parameters","temp3"))
		self.temp4 = float(self.config.get("pcr_parameters","temp4"))
		self.temp5 = float(self.config.get("pcr_parameters","temp5"))

		self.SS_time1 = int(self.config.get("pcr_parameters","SS_time1"))
		self.SS_time2 = int(self.config.get("pcr_parameters","SS_time2"))
		self.SS_time3 = int(self.config.get("pcr_parameters","SS_time3"))
		self.SS_time4 = int(self.config.get("pcr_parameters","SS_time4"))
		self.SS_final = int(self.config.get("pcr_parameters","SS_final"))

		self.temp_tolerance = float(self.config.get("pcr_parameters","temp_tolerance"))
		self.time_limit = int(self.config.get("pcr_parameters","time_limit"))
		self.sampling_time = float(self.config.get("pcr_parameters","sampling_time"))
		self.sampling_period = float(self.config.get("pcr_parameters","sampling_period"))

#------------------------- Steady-state temperature waiting ----------------------------

	def wait_for_SS(self, channel_target, tolerance=None):
		"""Waits until steady-state temperature is reached, or exits wait block if ramping
		time exceeds time limit parameter set in configuration file."""

		self.logging.info("%i\t--> Wait for steady-state - set temperature: %.2f C" % (self.cycle, channel_target))

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/wait_for_SS.wav')

		if tolerance is None:  # if temperature tolerance is not defined, set default to +/- 1 C
			tolerance = 1

		t0 = time.time()  # get current time
		while(True):

			ct = self.get_control_temperature()  # get control temperature value
			temp_diff = abs(channel_target - ct)  # calculate difference between target and actual temperature of control probe

			delta = time.time() - t0 # elapsed time in seconds

			sys.stdout.write("TIME\t -\t--> Elapsed time [s]: %i and current temperature [C]: %0.2f  \r" % (int(delta), ct))
			sys.stdout.flush()
			self.log_temperature()  # log temperature related parameters into log-file
			time.sleep(self.sampling_time)

			if temp_diff <= tolerance and temp_diff != 0:
				break
                        
			if delta > self.time_limit * 60:
				self.logging.warn("%i\t--> Time limit of %s minute(s) exceeded -> [current: %0.2f, target: %0.2f] C" % (self.cycle, self.time_limit, ct, channel_target))
				break

		elapsed = (time.time() - t0)
		self.logging.warn("%i\t--> Time to set steady-state temperature: %0.2f seconds and current temperature: %0.2f C" % (self.cycle, elapsed, ct))

#------------------------------ Pulling trigger point ----------------------------------

	def pull_trigger(self, poll_temp, tolerance=None):
		"""Breaks out of a temperature ramping procedure defined by a previous temperature
		   set point at a given trigger point. This function can set a step-wise ramping,
		   providing a steeper temperature ramping curve."""

		self.logging.info("%i\t--> Pull trigger - poll temperature: %0.2f C" % (self.cycle, poll_temp))

		if tolerance is None:  # if temperature tolerance is not defined, set default to +/- 1 C
			tolerance = 1

		t0 = time.time()  # get current time
		hs = self.get_control_temperature()  # get control temperature value

		if set_temp - poll_temp >= 0:  # if ramping up
			if poll_temp >= hs:

				temp_diff = abs(poll_temp - hs)  # calculate difference between poll and heat spreader temperature
				while temp_diff > tolerance:
					
					temp_diff = abs(poll_temp - hs)  # calculate difference between poll and heat spreader temperature
					hs = self.get_control_temperature()  # get control temperature value

					delta = time.time() - t0 # elapsed time in seconds
					sys.stdout.write("TIME\t -\t--> Elapsed time [s]: %i and current temperature [C]: %0.2f  \r" % (int(delta), hs))
					sys.stdout.flush()
					self.log_temperature()  # log temperature related parameters into log-file
					time.sleep(self.sampling_time)
                         
					if delta > self.time_limit * 60:
						self.logging.warn("%i\t --> Time limit %s exceeded -> [current: %0.2f, target: %0.2f] C" % (self.cycle, self.time_limit, hs, poll_temp))
						break
		else:  # if ramping down
			if poll_temp <= hs:

				temp_diff = abs(poll_temp - hs)  # calculate difference between poll and heat spreader temperature
				while temp_diff > tolerance:
					
					temp_diff = abs(poll_temp - hs)  # calculate difference between poll and heat spreader temperature
					hs = self.get_control_temperature()  # get control temperature value

					delta = time.time() - t0 # elapsed time in seconds
					sys.stdout.write("TIME\t -\t--> Elapsed time [s]: %i and current temperature [C]: %0.2f  \r" % (int(delta), hs))
					sys.stdout.flush()
					self.log_temperature()  # log temperature related parameters into log-file
					time.sleep(self.sampling_time)
                         
					if delta > self.time_limit * 60:
						self.logging.warn("%i\t --> Time limit %s exceeded -> [current: %0.2f, target: %0.2f] C" % (self.cycle, self.time_limit, hs, poll_temp))
						break		

		elapsed = (time.time() - t0) / 60

		self.logging.warn("%i\t--> Time to reach trigger point: %0.2f minutes and current temperature: %0.2f C" % (self.cycle, elapsed, hs))

#------------------------- Incubate and count elapsed time ----------------------------

	def incubate_reagent(self, time_sec):
		"""Incubates reagent for given amount of time and dynamically counts elapsed time 
		in seconds to update user about incubation state."""

		self.logging.info("%i\t--> Incubate reagent for %i s at %0.2f C target temperature" % (self.cycle, time_sec, target_temp))

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/incubate_reagent.wav')

		delta = 0  # initial time difference, ergo zero
		t0 = time.time()  # get current time

		while delta <= time_sec:  # incubation time loop

			ct = self.get_control_temperature()  # get actual control temperature value
			time.sleep(self.sampling_time)
			delta = time.time() - t0 # elapsed time in seconds

			sys.stdout.write("TIME\t %i\t--> Elapsed time [s]: %i of %i and current temperature [C]: %0.2f\r" % (self.cycle, int(delta), time_sec, ct))
			sys.stdout.flush()
			self.log_temperature()  # log temperature related parameters into log-file

		print '\n'

#----------------------------- Record temperature log ----------------------------------

	def log_temperature(self):
		"""Records target temperature related parameters of microdevice into a log-file."""

		st = self.get_set_temperature()   # get set temperature of controller
		pt = self.get_control_temperature()  # get control probe temperature
		ct = self.get_periphery_temperature()  # get actual periphery temperature value

		self.logfile.write("%f\t%f\t%f\t%f\n" % (time.time(), st, pt, ct))  # write time (s), set, control probe and microdevice channel temperature (C) into log-file

#------------------------- Monitor temperature on console ------------------------------

	def monitor_temperature(self):
		"""Prints continuous temperature reading along with time steps on console."""

		ti = 0  # set initial time to zero
		print("\nT (s)\tCONTROL (C)") 

		self.serial.flushInput()  # clear input buffer

		while(True):
			gt = self.get_control_temperature()  # get control temperature

			print("%i\t%0.2f" % (ti, gt))  # print time and control temperature
			ti = ti + 1  # update current sampling time 
			time.sleep(1)  # sleep for one sampling time duration

#-------------------------- Monitor parameters on console ------------------------------

	def monitor_parameters(self):
		"""Prints continuous temperature parameters on console."""

		ti = 0  # set initial time to zero
		print("\nT (s)\tST (C)\tPT (C)\tGT (C)") 

		self.serial.flushInput()  # clear input buffer

		while(True):

			st = self.get_set_temperature()   # get set temperature of controller
			pt = self.get_control_temperature()  # get control probe temperature
			gt = self.get_periphery_temperature()  # get periphery temperature

			print("%i\t%0.2f\t%0.2f\t%0.2f" % (ti, st, pt, gt))  # print time (s), set, control probe and periphery sensor temperature (C)
			ti = ti + 1  # update current sampling time 
			time.sleep(1)  # sleep for one sampling time duration

#-------------------------- Monitor parameters on console ------------------------------

	def sample_parameters(self):
		"""Records contious target temperature related parameters of microdevice onto console and into a log-file."""

		t0 = time.time()  # get current time
		ti = 0  # set initial time to zero
		delta = 0  # initial time difference, ergo zero		

		self.serial.flushInput()  # clear input buffer
		print("\nT (s)\tST (C)\tPT (C)\tGT (C)") 

		while delta <= self.sampling_period * 60:  # incubation time loop

			st = self.get_set_temperature()   # get set temperature of controller
			pt = self.get_control_temperature()  # get control probe temperature
			gt = self.get_periphery_temperature()  # get periphery temperature

			self.log_temperature()  # log temperature related parameters into log-file
			print("%i\t%0.2f\t%0.2f\t%0.2f" % (ti, st, pt, gt))  # print time (s), set, control probe and periphery sensor temperature (C)

			ti = ti + 1  # update current sampling time 
			time.sleep(0.11781) # sleep for one sampling time duration
			delta = time.time() - t0 # elapsed time in seconds

#-------------------------- Press enter to exit execution ------------------------------

	def press_q_to_exit(self):

		sys.stdout.write("PROMPT\t %i\t--> Press 'Q' to quit final cooling step: " % (self.cycle))

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/exit.wav')

		response = (sys.stdin.readline()).strip()  # read user prompt from keyboard

		if response == 'Q' or response == 'q':  # if 'Q' or 'q' pressed
			sys.stdout.write("PROMPT\t %i\t--> PCR final cooling step ended!\n\n" % (self.cycle))
			self.set_control_off()  # turn external temperature controller OFF
			self.logfile.close()  # close log-file when completely finished
			sys.stdout.write('\n')
			sys.exit()  # quit execution	
		else:
			self.press_q_to_exit()  # otherwise recurse

#----------------------- Perform PCR cycle without trigger points ----------------------

	def pcr_wo_trigger(self):
		"""Performs PCR cycle in gene-chip (without trigger points) consisting of the following schematics:

		1. 24-90 C -> hold for 15 s (denaturation step)
		2. 90-40 C -> hold for 30 s (annealing step)
		3. 40-70 C -> hold for 75 s (elongation step)
		4. 70-4  C -> hold for infinity (final hold)

		[Note: steps 1-3 are repeated 20 times.]"""

		self.logging.info("%i\t--> In polymerase chain reaction" % self.cycle)

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/pcr_start.wav')

		# Step 1 - denaturation
		self.logging.info("%i\t--> In (outer) denaturation step" % self.cycle)
		self.logging.info("%i\t--> Set PCR solution temperature to %.2f C" % (self.cycle, self.temp1))  # set temperature: 90 C

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/outer_denaturation.wav')

		self.set_P_bandwidth(self.P_bandwidth1)  # set proportional bandwidth
		self.set_I_gain(self.I_gain1)  # set integral gain
		self.set_D_gain(self.D_gain1)  # set derivative gain

		self.set_temperature(self.temp1)  # set target temperature to 90 C
		self.wait_for_SS(self.temp1, self.temp_tolerance)  # wait until steady-state is reached
		self.incubate_reagent(self.SS_time1)  # incubate reagent for 15 sec

		#------------------------------ Iteration loop -------------------------------------
		
		for i in range(0, self.loop_iter):

			self.cycle = i + 1  # update PCR cycle iteration number

			if self.speech_option == 1:
				commands.getstatusoutput('mplayer -ao pulse ../speech/cycle_' + str(self.cycle) + '.wav')

			if i != 0:  # not first time into loop

				# Step 2 - denaturation
				self.logging.info("%i\t--> In (inner) denaturation step" % self.cycle)
				self.logging.info("%i\t--> Set PCR solution temperature to %.2f C" % (self.cycle, self.temp2))  # set temperature: 90 C

				if self.speech_option == 1:
					commands.getstatusoutput('mplayer -ao pulse ../speech/inner_denaturation.wav')

				self.set_P_bandwidth(self.P_bandwidth2)  # set proportional bandwidth
				self.set_I_gain(self.I_gain2)  # set integral gain
				self.set_D_gain(self.D_gain2)  # set derivative gain

				self.set_temperature(self.temp2)  # set target temperature to 90 C
				self.wait_for_SS(self.temp2, self.temp_tolerance)  # wait until steady-state is reached
				self.incubate_reagent(self.SS_time2)  # incubate reagent for 15 sec

			# Step 3 - annealing
			self.logging.info("%i\t--> In (inner) annealing step" % self.cycle)
			self.logging.info("%i\t--> Set PCR solution temperature to %.2f C" % (self.cycle, self.temp3))  # set temperature: 40 C

			if self.speech_option == 1:
				commands.getstatusoutput('mplayer -ao pulse ../speech/annealing.wav')

			self.set_P_bandwidth(self.P_bandwidth3)  # set proportional bandwidth
			self.set_I_gain(self.I_gain3)  # set integral gain
			self.set_D_gain(self.D_gain3)  # set derivative gain

			self.set_temperature(self.temp3)  # set target temperature to 40 C
			self.wait_for_SS(self.temp3, self.temp_tolerance)  # wait until steady-state is reached
			self.incubate_reagent(self.SS_time3)  # incubate reagent for 30 sec

			# Step 4 - elongation
			self.logging.info("%i\t--> In (inner) elongation step" % self.cycle)
			self.logging.info("%i\t--> Set PCR solution temperature to %.2f C" % (self.cycle, self.temp4))  # set temperature: 70 C

			if self.speech_option == 1:
				commands.getstatusoutput('mplayer -ao pulse ../speech/inner_elongation.wav')

			self.set_P_bandwidth(self.P_bandwidth4)  # set proportional bandwidth
			self.set_I_gain(self.I_gain4)  # set integral gain
			self.set_D_gain(self.D_gain4)  # set derivative gain

			self.set_temperature(self.temp4)  # set target temperature to 70 C
			self.wait_for_SS(self.temp4, self.temp_tolerance)  # wait until steady-state is reached
			self.incubate_reagent(self.SS_time4)  # incubate reagent for 75 sec

		# Step 5 - final hold
		self.logging.info("%i\t--> In (outer) final hold" % self.cycle)
		self.logging.info("%i\t--> Set PCR solution temperature to %.2f C" % (self.cycle, self.temp5))  # set temperature: 25 C

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/final_hold.wav')

		self.set_P_bandwidth(self.P_bandwidth5)  # set proportional bandwidth
		self.set_I_gain(self.I_gain5)  # set integral gain
		self.set_D_gain(self.D_gain5)  # set derivative gain

		self.set_temperature(self.temp5)  # set target temperature to 25 C
		self.incubate_reagent(self.SS_final)  # incubate reagent for 1 minute

		if self.speech_option == 1:
			commands.getstatusoutput('mplayer -ao pulse ../speech/pcr_end.wav')

		self.press_q_to_exit()  # press 'Q' to exit final cooling step when desired

#--------------------- Perform PCR cycle with trigger points ---------------------------

	def pcr_wi_trigger(self):
		"""Performs PCR cycle in gene-chip (with trigger points) consisting of the following schematics:

		1. 24-90 C -> hold for 15 s (denaturation step)
		2. 90-40 C -> hold for 30 s (annealing step)
		3. 40-70 C -> hold for 75 s (elongation step)
		4. 70-4  C -> hold for infinity (final hold)

		[Note: steps 1-3 are repeated 20 times.]"""

		self.logging.info("%i\t--> In polymerase chain reaction" % self.cycle)

		# Step 1 - denaturation
		self.logging.info("%i\t--> In (outer) denaturation step" % self.cycle)
		self.logging.info("%i\t--> Set PCR solution temperature to %i C" % (self.cycle, self.temp1))  # set control temperature: 90 C

		self.set_P_bandwidth(self.P_bandwidth1)  # set proportional bandwidth
		self.set_I_gain(self.I_gain1)  # set integral gain
		self.set_D_gain(self.D_gain1)  # set derivative gain

		self.set_temperature(self.set_temp1)  # set control temperature to 100 C
		self.poll_trigger(self.poll_temp1, self.temp_tolerance)  # wait until poll temperature 85 C reached

		self.set_temperature(self.temp1)  # set control temperature to 90 C
		self.wait_for_SS(self.temp1, self.temp_tolerance)  # wait until steady-state is reached
		self.incubate_reagent(self.SS_time1)  # incubate reagent for 15 sec

		#------------------------------ Iteration loop -------------------------------------
		
		for i in range(0, self.loop_iter):

			self.cycle = i + 1  # update PCR cycle iteration number

			# Step 2 - denaturation
			self.logging.info("%i\t--> In (inner) denaturation step" % self.cycle)
			self.logging.info("%i\t--> Set PCR solution temperature to %i C" % (self.cycle, self.temp2))  # set temperature: 90 C

			if i == 0:  # first time into loop
				self.incubate_reagent(self.SS_time2)  # incubate reagent for 15 sec

			else:
				self.set_P_bandwidth(self.P_bandwidth2)  # set proportional bandwidth
				self.set_I_gain(self.I_gain2)  # set integral gain
				self.set_D_gain(self.D_gain2)  # set derivative gain

				self.set_temperature(self.set_temp2)  # set control temperature to 100 C
				self.poll_trigger(self.poll_temp2, self.temp_tolerance)  # wait until poll temperature 85 C reached

				self.set_temperature(self.temp2)  # set control temperature to 90 C
				self.wait_for_SS(self.temp2, self.temp_tolerance)  # wait until steady-state is reached
				self.incubate_reagent(self.SS_time2)  # incubate reagent for 15 sec

			# Step 3 - annealing
			self.logging.info("%i\t--> In (inner) annealing step" % self.cycle)
			self.logging.info("%i\t--> Set PCR solution temperature to %i C" % (self.cycle, self.temp3))  # set temperature: 40 C

			self.set_P_bandwidth(self.P_bandwidth3)  # set proportional bandwidth
			self.set_I_gain(self.I_gain3)  # set integral gain
			self.set_D_gain(self.D_gain3)  # set derivative gain

			self.set_temperature(self.set_temp3)  # set control temperature to 0 C
			self.poll_trigger(self.poll_temp3, self.temp_tolerance)  # wait until poll temperature 42 C reached

			self.set_temperature(self.temp3)  # set control temperature to 40 C
			self.wait_for_SS(self.temp3, self.temp_tolerance)  # wait until steady-state is reached
			self.incubate_reagent(self.SS_time3)  # incubate reagent for 30 sec

			# Step 4 - elongation
			self.logging.info("%i\t--> In (inner) elongation step" % self.cycle)
			self.logging.info("%i\t--> Set PCR solution temperature to %i C" % (self.cycle, self.temp4))  # set temperature: 70 C

			self.set_P_bandwidth(self.P_bandwidth4)  # set proportional bandwidth
			self.set_I_gain(self.I_gain4)  # set integral gain
			self.set_D_gain(self.D_gain4)  # set derivative gain

			self.set_temperature(self.set_temp4)  # set control temperature to 80 C
			self.poll_trigger(self.poll_temp4, self.temp_tolerance)  # wait until poll temperature 65 C reached

			self.set_temperature(self.temp4)  # set control temperature to 70 C
			self.wait_for_SS(self.temp4, self.temp_tolerance)  # wait until steady-state is reached
			self.incubate_reagent(self.SS_time4)  # incubate reagent for 75 sec

		# Step 5 - final hold
		self.logging.info("%i\t--> In (outer) final hold" % self.cycle)
		self.logging.info("%i\t--> Set PCR solution temperature to %i C" % (self.cycle, self.temp6))  # set temperature: 4 C

		self.set_P_bandwidth(self.P_bandwidth5)  # set proportional bandwidth
		self.set_I_gain(self.I_gain5)  # set integral gain
		self.set_D_gain(self.D_gain5)  # set derivative gain

		self.set_temperature(self.temp5)  # set target temperature to 25 C
		self.incubate_reagent(self.SS_final)  # incubate reagent for 1 minute

		self.press_enter_to_exit()  # press 'Q' to exit final cooling step when desired


