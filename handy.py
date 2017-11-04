import os, sys, inspect, thread, time, timeit
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
# arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def handMovements(frame):
	for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

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

        handMovements(frame)

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