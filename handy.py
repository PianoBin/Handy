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

def hand_placement(frame):
    count = 0
    hands = frame.hands
    left = hands.leftmost()
    right = hands.rightmost()

    normalL = left.palm_normal
    normalR = right.palm_normal
    directionL = left.direction
    directionR = right.direction

    Lroll = normalL.yaw * Leap.RAD_TO_DEG
    Rroll = normalR.yaw * Leap.RAD_TO_DEG
    Lyaw = directionL.roll * Leap.RAD_TO_DEG
    Ryaw = directionR.roll * Leap.RAD_TO_DEG
    Lpitch = directionL.pitch * Leap.RAD_TO_DEG
    Rpitch = directionR.pitch * Leap.RAD_TO_DEG

    print "pitch left: %f\npitch right: %f\nroll left: %f\nroll right: %f\nyaw left: %f\nyaw right %f" % (
        Lpitch, Rpitch,
        Lroll, Rroll,
        Lyaw, Ryaw)

def handMovements(frame):
	for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, velocity: %s" % (handType, hand.id, hand.palm_velocity)

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


startTime = 0
beforeTime = 0

class LeapEventListener(Leap.Listener):

    #global count = 0
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.Type.TYPE_SWIPE)
        controller.config.set("Gesture.Swipe.MinLength", 200.0)
        controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_frame(self, controller):
        frame = controller.frame()
        #Process frame data

        #Show time elapsed
        global startTime
        global beforeTime
        if startTime == 0:
        	startTime = timeit.default_timer()
        if int ((timeit.default_timer() - startTime) * 10) % 10 == 0:
        	if beforeTime != int(timeit.default_timer() - startTime):
        		print "Elapsed {}".format(int(timeit.default_timer() - startTime))
        		beforeTime = int(timeit.default_timer() - startTime)

        hand_placement(frame)

    def on_exit(self, controller):
        print "Exited"
        #the method where we return our statistics

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

if __name__ == "__main__":
    main()
