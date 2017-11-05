from __future__ import division
from flask import Flask, render_template
app = Flask(__name__)
import os, sys, inspect, thread, time, timeit
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
# arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

moveCounter = 0
xCounterSmall = 0
xCounterGood = 0
xCounterHigh = 0
yCounterSmall = 0
yCounterGood = 0
yCounterHigh = 0
zCounterSmall = 0
zCounterGood = 0
zCounterHigh = 0

roll_angle_left = 0
yaw_angle_left = 0
pitch_angle_left = 0
roll_angle_right = 0
yaw_angle_right = 0
pitch_angle_right = 0
angle_count_left = 1
angle_count_right = 1

frame_counter = 0
hands_in_frame_counter = 0
percent_sweet_array = []
time_counter = []

def hand_in_frames(frame):
    global frame_counter, hands_in_frame_counter, percent_sweet_array, time_counter
    frame_counter += 2
    for hand in frame.hands:
        hands_in_frame_counter += 1
    print "hands in frame {}".format(hands_in_frame_counter)
    print "frames {}".format(frame_counter)

def hand_placement(frame):

    global roll_angle_left, yaw_angle_left, pitch_angle_left, roll_angle_right, yaw_angle_right, pitch_angle_right, angle_count_left, angle_count_right
    for hand in frame.hands:
        handType = "Left hand" if hand.is_left else "Right hand"

        normal = hand.palm_normal
        direction = hand.direction

        real_roll = normal.yaw * Leap.RAD_TO_DEG
        real_yaw = direction.roll * Leap.RAD_TO_DEG
        real_pitch = direction.pitch * Leap.RAD_TO_DEG

        if handType == "Left hand":
            angle_count_left += 1
            roll_angle_left += real_roll
            yaw_angle_left += real_yaw
            pitch_angle_left += real_pitch
        else:
            angle_count_right += 1
            roll_angle_right += real_roll
            yaw_angle_right += real_yaw
            pitch_angle_right += real_pitch

        #print "%s roll on the now y-axis: %f" % (handType, real_roll)
        #print "%s yaw on the now z-axis: %f" % (handType, real_yaw)
        #print "%s pitch on the now x-axis: %f" % (handType, real_pitch)

def handMovements(frame):
	for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            #print "  %s, id %d, velocity: %s" % (handType, hand.id, hand.palm_velocity)

            global moveCounter, xCounterSmall, xCounterGood, xCounterHigh, yCounterSmall, yCounterGood, yCounterHigh, zCounterSmall, zCounterGood, zCounterHigh
            moveCounter += 1
            if abs(hand.palm_velocity.x) < 50:
            	xCounterSmall += 1
            elif abs(hand.palm_velocity.x) > 200:
            	xCounterHigh += 1
            else:
            	xCounterGood += 1

            if abs(hand.palm_velocity.y) < 50:
            	yCounterSmall += 1
            elif abs(hand.palm_velocity.y) > 200:
            	yCounterHigh += 1
            else:
            	yCounterGood += 1

            if abs(hand.palm_velocity.z) < 50:
            	zCounterSmall += 1
            elif abs(hand.palm_velocity.z) > 200:
            	zCounterHigh += 1
            else:
            	zCounterGood += 1

fingerCounter = 0
badFingerCounter = 0

def fingerPointing(frame):
	global fingerCounter, badFingerCounter
	oneFinger = False
	multiFingers = False
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	for hand in frame.hands:
		for finger in hand.fingers:
			#print "finger extended is {}".format(finger.is_extended)
			if finger.is_extended and not oneFinger:
				oneFinger = True
			elif finger.is_extended and oneFinger:
				multiFingers = True
			fingerCounter += 1
		if oneFinger and not multiFingers:
			badFingerCounter += 1
		oneFinger = False
		multiFingers = False

x_speed_mes = ''
y_speed_mes = ''
openness = ''
message_open = ''
finger_message = ''
sweetness = ''
x_speed = 0
y_speed = 0
sweet_spot = 0
x_speed_array = []
y_speed_array = []

def displayResults():

	global moveCounter, xCounterSmall, xCounterGood, xCounterHigh, yCounterSmall, yCounterGood, yCounterHigh, zCounterSmall, zCounterGood, zCounterHigh
	global x_speed_mes, y_speed_mes, openness, message_open, finger_message, sweetness
	global x_speed, y_speed, x_speed_array, y_speed_array
	x_speed = xCounterGood / moveCounter * 100
	y_speed = yCounterGood / moveCounter * 100
	x_speed = '{0:.4g}'.format(x_speed)
	y_speed = '{0:.4g}'.format(y_speed)
	if xCounterGood / moveCounter * 100 > 60:
		x_speed_mes = 'Great speed for hand gestures!'
	else:
		if ((xCounterSmall/moveCounter) * 100) > ((xCounterHigh/moveCounter) * 100):
			x_speed_mes = 'A little to slow or not enough movement.'
		else:
			x_speed_mes = 'Slow down there cowboy.'
	if yCounterGood / moveCounter * 100 > 60:
		y_speed_mes = 'Great speed for hand gestures!'
	else:
		if ((yCounterSmall/moveCounter) * 100) > ((yCounterHigh/moveCounter) * 100):
			y_speed_mes = 'A little to slow or not enough movement.'
		else:
			y_speed_mes = 'Slow down there cowboy.'

	x_speed_array.append((xCounterSmall/moveCounter) * 100)
	x_speed_array.append((xCounterGood/moveCounter) * 100)
	x_speed_array.append(100 - ((xCounterSmall/moveCounter) * 100) - ((xCounterGood/moveCounter) * 100))

	y_speed_array.append((yCounterSmall/moveCounter) * 100)
	y_speed_array.append((yCounterGood/moveCounter) * 100)
	y_speed_array.append(100 - ((yCounterSmall/moveCounter) * 100) - ((yCounterGood/moveCounter) * 100))

	global roll_angle_left, yaw_angle_left, pitch_angle_left, roll_angle_right, yaw_angle_right, pitch_angle_right, angle_count_left, angle_count_right
	if abs(pitch_angle_left/angle_count_left) < 40 and abs(pitch_angle_right/angle_count_right) < 40 and abs(roll_angle_left/angle_count_left) > 90 and abs(roll_angle_right/angle_count_right) > 90:
		message_open = 'Good job! You kept your palms open.\nThis makes you seem approachable to your crowd.'
		openness = 'Open'
	else:
		message_open = 'Work on keeping your palms more open.\nIt makes you instantly more approachable to your audience.'
        openness = 'Not Open'

	global fingerCounter, badFingerCounter
	if badFingerCounter > 10:
		finger_message = 'Try not to point too much while talking!\nIt can be seen as agressive by the audience.'
	else:
		finger_message = 'Well done. You kept your fingers away from the crowd.'

	global frame_counter, hands_in_frame_counter, sweet_spot
	sweet_spot = (hands_in_frame_counter/frame_counter)*100
	sweet_spot = '{0:.4g}'.format(sweet_spot)
	if sweet_spot > 50:
		sweetness = 'Well done.'
	else:
		sweetness = 'Try to keep your hands in the sweet spot.'


startTime = 0
beforeTime = 0

class LeapEventListener(Leap.Listener):

    #global count = 0
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        #controller.enable_gesture(Leap.Gesture.Type.TYPE_SWIPE)
        #controller.config.set("Gesture.Swipe.MinLength", 200.0)
        #controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_frame(self, controller):
        frame = controller.frame()
        #Process frame data

        #Show time elapsed
        global startTime
        global beforeTime
        global percent_sweet_array, time_counter, hands_in_frame_counter, frame_counter
        if startTime == 0:
        	startTime = timeit.default_timer()
        if int ((timeit.default_timer() - startTime) * 10) % 10 == 0:
        	if beforeTime != int(timeit.default_timer() - startTime):
        		print "Elapsed {}".format(int(timeit.default_timer() - startTime))
        		beforeTime = int(timeit.default_timer() - startTime)
        		percent_sweet_array.append((hands_in_frame_counter/frame_counter)*100)
        		time_counter.append(beforeTime)

        handMovements(frame)
        hand_placement(frame)
        fingerPointing(frame)
        hand_in_frames(frame)

    def on_exit(self, controller):
        print "Exited"
        displayResults()
        #the method where we return our statistics

'''
def main():
	listener = LeapEventListener()
	controller = Leap.Controller()
	controller.add_listener(listener)
	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)
'''

@app.route("/")
def handy():
	listener = LeapEventListener()
	controller = Leap.Controller()
	controller.add_listener(listener)
	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)
	print percent_sweet_array
	print time_counter
	return render_template('handyWeb.html', x_speed_mes=x_speed_mes, y_speed_mes=y_speed_mes, openness=openness, finger_message=finger_message, sweetness=sweetness, x_speed=x_speed, y_speed=y_speed, badFingerCounter=badFingerCounter, sweet_spot=sweet_spot, x_speed_array=x_speed_array, y_speed_array=y_speed_array ,percent_sweet_array=percent_sweet_array, time_counter=time_counter)

if __name__ == "__main__":
	app.run()
