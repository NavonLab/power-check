from crontab import CronTab

my_cron = CronTab(user = 'pi')

#run check.py every minute to check power
checkpower = my_cron.new(command = 'sudo python3 /home/pi/python/check.py')
checkpower.minute.every(1)

#run mail every two weeks to send log
sendlog = my_cron.new(command = 'sudo python3 /home/pi/python/sendlog.py')
sendlog.hour.every(336)

#clear log once every year
clearlog = my_cron.new(command = 'rm /home/pi/python/power.log')
clearlog.hour.every(8736)

#my_cron.remove_all()
my_cron.write()