# Sense Hat Off Button Program
# When this program is active, press the middle button twice
# to shutdown the Raspberry Pi, and press three times to instead
# end the program. Allows for a convenient way to shutdown the Pi,
# especially useful when headless.
# By Julius Villamayor, 2017

from sense_hat import SenseHat
from time import sleep
import os

s = SenseHat()
last_time = -1
second_last_time = -1
last_direction = ""
second_last_direction = ""
time_passed = 99
s.rotation = 270
low_light = True

# When the middle button is doubled pressed, this function is called.
# It looks for a third middle button press for 1 second. If it finds
# one, the screen displays '1' and the program ends. Otherwise, it turns
# the Raspberry Pi off.
def shutdown():
        third = False
        s.stick.get_events()
        sleep(1)
        recent_events = s.stick.get_events()
        if len(recent_events) > 0:
                for x in recent_events:
                        if x[1] == 'middle' and x[2] == 'pressed':
                                third = True
        if third == True:
                s.show_letter("1")
                sleep(2)
                s.clear()
                quit()
        else:
                s.show_letter("0")
                sleep(2)
                s.clear()
                os.system("sudo shutdown -h now")

while(True):
	event = s.stick.wait_for_event(emptybuffer=True)

	if (event.action == "released" or event.direction != "middle"):
		continue

	second_last_time = last_time
	second_last_direction = last_direction
	last_time = event.timestamp
	last_direction = event.direction

	if second_last_time == -1:
		time_passed = 99
	else:
		time_passed = last_time - second_last_time

	#print("time passed: {}\n direction: {}".format(time_passed,event.direction))

	if time_passed < .3:
		shutdown()

