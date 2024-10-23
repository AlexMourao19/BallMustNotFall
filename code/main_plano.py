import cv2
import numpy as np
import time
import RPi.GPIO as GPIO


# Inicializar os 2 servos
#servosPin = np.array([5, 3])
servo1Pin = 5
servo2Pin = 3
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1Pin, GPIO.OUT)
GPIO.setup(servo2Pin, GPIO.OUT)
servo1 = GPIO.PWM(servo1Pin, 50)
servo2 = GPIO.PWM(servo2Pin, 50)
servo1.start(0)
servo2.start(0)

#Coordenadas do centro
center_x = 0.0
center_y = 0.0

# Min e Max angulos de cada servo
min_ang = np.array([0, 60])
max_ang = np.array([120, 140])

def SetAngle(angle, pin, servo):
    duty = angle /18 + 2
    GPIO.output(pin, True)
    servo.ChangeDutyCycle(duty)
    #time.sleep(1)
    GPIO.output(pin, False)
    #servo.ChangeDutyCycle(0)

# Inicializar as posiçoes iniciais dos servos
init_ang = np.array([70, 90])

SetAngle(init_ang[0], servo1Pin, servo1)
SetAngle(init_ang[1], servo2Pin, servo2)

# PID parametros
kp = 0.1
ki = 0.01
kd = 0.01

# Inicializar variaveis de PID
errors = np.zeros(2)
integral = np.zeros(2)
derivative = np.zeros(2)
pid_control_prev_errors = np.zeros(2)

    
# ... script posicao da bola


def ball_finder(): # alterar para o script da pos da bola
    x = float(input("Enter x: "))
    y = float(input("Enter y: "))
    result = (x, y)
    return result

# Funcao para mover os servos com PID
def move_servos(pid):
    for i in range(2):
        angle = init_ang[i] + pid[i]
        angle = np.floor(angle)
        if angle > max_ang[i]:
            print(f"Servo {i} at maximum angle")
            angle = max_ang[i]
        if angle < min_ang[i]:
            print(f"Servo {i} at minimum angle")
            angle = min_ang[i]
        if i == 0:
            SetAngle(angle, servo1Pin, servo1)
        if i == 1:
            SetAngle(angle, servo2Pin, servo2)

# Funcao para calcular os erros com base na posicao da bola
def get_errors(x, y):
    global center_x, center_y, errors
    errors[0] = center_x - x
    errors[1] = center_y - y
    
# Funcao para controlar os servos usando PID
def pid_control():
    global errors, integral, derivative, pid_control_prev_errors
    integral = integral + errors
    derivative = errors - pid_control_prev_errors
    pid = kp * errors + ki * integral + kd * derivative
    pid_control_prev_errors = errors
    return pid
# Loop principal

while True:
    x, y = ball_finder()
    get_errors(x, y)
    pid = pid_control()
    move_servos(pid)
    #print("x = ", x)
    #print("y = ", y)
    time.sleep(1)

