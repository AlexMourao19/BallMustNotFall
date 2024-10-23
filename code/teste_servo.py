
import time
#from adafruit_servokit import ServoKit # change library !!!
#from gpiozero import Servo
import RPi.GPIO as GPIO

servo1Pin = 3 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1Pin, GPIO.OUT)
servo1 = GPIO.PWM(servo1Pin, 50)
servo1.start(0)

def SetAngle(angle):
    duty = angle /18 +2
    GPIO.output(servo1Pin, True)
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo1Pin, False)
    servo1.ChangeDutyCycle(0)

SetAngle(90)

servo1.stop()
GPIO.cleanup()