import RPi.GPIO as GPIO
import text
import sys
import pickle
from influxdb import InfluxDBClient
import datetime
import serial

#set logging settings to ouptut to power.log and log everything above "warning" level
import logging
logging.basicConfig(
filename = 'power.log', filemode ='a',
format = '%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S',
level=logging.WARNING
)

#configure pin 11 on RPi to read from arduino
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#variable to keep track of whether power is currently out
power_out = 0

try:
    #open file that contains current status of power and load into power_out variable
    with open('/home/pi/python/data.pickle', 'rb') as f:
        power_out = pickle.load(f)

    #define state as input of GPIO pin 
    state = GPIO.input(11)
    
    #power is out case
    if (state == GPIO.LOW):
        
        #first time reading power outage
        if (power_out == 0):        
            print("Power has gone out.")
            text.power_out()
            #mail.outage()
            #set power_out to true
            power_out = 1
            logging.warning('Power outage.')
            
        #if alert has already been sent, do nothing
        else:
            print("Power is still out.")

    #power is not out case
    elif (state == GPIO.HIGH):
        import mail
        #send update that power has been restored
        if (power_out == 1):        
            print("Power has been restored.")
            text.power_restored()
            mail.restored()
            #set power_out to false
            power_out = 0
            logging.warning('Power restored.')
        
        #if power is on, do nothing
        else:
            print("Power is on.")
    
    #dump current status of power into pickle file
    with open('/home/pi/python/data.pickle', 'wb') as f:
        pickle.dump(power_out, f, pickle.HIGHEST_PROTOCOL)
        
    #send data to influxdb server
    url = ""
    port = ""
    username = ""
    pwd = ""
    db_name = ""
    client = InfluxDBClient(url, port, username, pwd, db_name)
    current_time = str(datetime.datetime.utcnow())
    current_status = "On"
    if (power_out == 0):
        current_status = "Out"
    json_body = [
        {"measurement": "Power Status",
            "time": current_time,
            "fields": {
                "Status": current_status
                }
            }
        ]
    client.write_points(json_body)
    
        
        
        
    
#log and email any exceptions that occur
except Exception as e:
    import mail
    print(e)
    logging.error("Exception occured", exc_info=True)
    mail.exception(e)
    sys.exit()


