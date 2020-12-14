# power-check
Software reposity for power check and alert system in SPL.
Hello! This is a quick guide to the organization of the power check software. 

I: SOFTWARE

All scripts are stored in the "python" directory (/home/pi/python). 

The main script that runs every minute is called "check.py". This script checks whether the power is out and sends various updates under different conditions. 
	-If the power just went out, it sends an SMS to all the numbers in the file "phonebook.py".
	-If the power has just been restored, it sends an SMS and an email to all the numbers and emails in 		"phonebook.py".
	-If it logs an exception, it will send an email to our lab account.

The only other script that runs directly is "sendlog.py" which is scheduled to run once every two weeks. All it does is send the "power.log" file as an attachment to our lab account.

Some brief descriptions of the other files in this folder:
	-"CronScheduler.py" schedules Cronjobs on the Pi. In order to clear/edit the cronjobs, see this file.
	-"data.pickle" stores a global variable representing the current status of the power.
	-"mail.py" includes functions that send emails in different situations.
	-"phonebook.py" contains a list of names, numbers, and emails that updates will be sent to. In order to 	edit who is receiving updates, see this file.
	-"power.log" is just a log of everything that "check.py" monitors.
	-"text.py" includes functions that send SMS messages in different situations.

II: HARDWARE

The Pi should be hardwired to the Arduino at all times. GPIO pin 6 should be connected to Arduino's ground, and pin 11 should be connected to Arduino's 3.3V port (see raspberrypi.org/documentation/usage/gpio for a schematic of the pin numbers). 

The Arduino should be plugged into the wall, and the Raspberry Pi to backup power.

The Raspberry Pi ideally should be connected to internet at all times. This is to prevent a bug that results from the Pi not being able to send emails via the 3G network. If the Pi fails to send the log every two weeks, the problem is likely that it has been disconnected from the internet.
