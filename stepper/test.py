import RPi.GPIO as GPIO
import time
from HR8825 import HR8825


try:
    # small stepper motors
	Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=26)#, mode_pins=(16, 17, 20))
	Motor2 = HR8825(dir_pin=10, step_pin=9, enable_pin=11)#, mode_pins=(21, 22, 27))
	# big stepper motors
	Motor3 = HR8825(dir_pin=21, step_pin=20, enable_pin=16)#, mode_pins=(16, 17, 20))
	Motor4 = HR8825(dir_pin=5, step_pin=6, enable_pin=12)#, mode_pins=(21, 22, 27))

	"""
	# 1.8 degree: nema23, nema14
	# software Control :
	# 'fullstep': A cycle = 200 steps
	# 'halfstep': A cycle = 200 * 2 steps
	# '1/4step': A cycle = 200 * 4 steps
	# '1/8step': A cycle = 200 * 8 steps
	# '1/16step': A cycle = 200 * 16 steps
	# '1/32step': A cycle = 200 * 32 steps
	"""
	Motor1.SetMicroStep('hardware')
	#0.001 stepdelay for small stepper motors at fastest speed (1/4 step is chosen as optimal, thus 800 steps is 1 cycle, 800*1/4*1.8=360 degree)
	Motor1.TurnStep(Dir='forward', steps=800, stepdelay = 0.001)
	time.sleep(0.5)
	Motor1.TurnStep(Dir='backward', steps=800, stepdelay = 0.001)
	Motor1.Stop()

	"""
	# 28BJY-48:
	# software Control :
	# 'fullstep': A cycle = 2048 steps
	# 'halfstep': A cycle = 2048 * 2 steps
	# '1/4step': A cycle = 2048 * 4 steps
	# '1/8step': A cycle = 2048 * 8 steps
	# '1/16step': A cycle = 2048 * 16 steps
	# '1/32step': A cycle = 2048 * 32 steps
	"""
	Motor2.SetMicroStep('hardware')    
	Motor2.TurnStep(Dir='forward', steps=2000, stepdelay=0.001)
	time.sleep(0.5)
	Motor2.TurnStep(Dir='backward', steps=2000, stepdelay=0.001)
	Motor2.Stop()
	
	Motor3.SetMicroStep('hardware')    
	Motor3.TurnStep(Dir='forward', steps=2000, stepdelay=0.001)
	time.sleep(0.5)
	Motor3.TurnStep(Dir='backward', steps=2000, stepdelay=0.001)
	Motor3.Stop()
	
	Motor4.SetMicroStep('hardware')    
	Motor4.TurnStep(Dir='forward', steps=2000, stepdelay=0.001)
	time.sleep(0.5)
	Motor4.TurnStep(Dir='backward', steps=2000, stepdelay=0.001)
	Motor4.Stop()

	Motor1.Stop()
	Motor2.Stop()
	Motor3.Stop()
	Motor4.Stop()
    
except:
    # GPIO.cleanup()
    print("\nMotor stop")
    Motor1.Stop()
    Motor2.Stop()
    Motor3.Stop()
    Motor4.Stop()
    exit()