from argparse import ArgumentError
import time, math

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need \
           superuser privileges.  You can achieve this by using 'sudo' to run \
           your script")

class Driver(object):

    def __init__(self, left_pins, right_pins):
        """
        Initializes driver object to implement PWM control of two motors

        params:
            - left_pins =   (left pin 1, left pin 2, left pwm pin). For example,
                            (AIN1, AIN2, APWM)
            - right_pins =  (right pin 1, right pin 2, right pwm pin). For
                            example, (BIN1, BIN2, BPWM)
        """
        (l_1, l_2, l_pwm) = left_pins
        self.L_1 = l_1
        self.L_2 = l_2
        self.L_PWM = l_pwm
        
        (r_1, r_2, r_pwm) = right_pins
        self.R_1 = r_1
        self.R_2 = r_2
        self.R_PWM = r_pwm

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) 

        GPIO.setup(self.L_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.L_2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.L_PWM, GPIO.OUT)
        GPIO.setup(self.R_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.R_2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.R_PWM, GPIO.OUT)

        self.right = GPIO.PWM(self.L_PWM, 50.0)
        self.left = GPIO.PWM(self.R_PWM, 50.0)

        self.right.start(0.0)
        self.left.start(0.0)
        self.u = 0
        self.theta_u = 0


    def set_direction(self, dir):
        """
        Sets the direction of the two motors in WASD format

        params:
            - dir = can be 'w', 's', 'a', or 'd'.

        returns:
            - nothing
        """
        if dir == 'w':
            GPIO.output(self.L_1, GPIO.HIGH)
            GPIO.output(self.L_2, GPIO.LOW)
            GPIO.output(self.R_1, GPIO.HIGH)
            GPIO.output(self.R_2, GPIO.LOW)
        elif dir == 'a':
            GPIO.output(self.L_1, GPIO.LOW)
            GPIO.output(self.L_2, GPIO.HIGH)
            GPIO.output(self.R_1, GPIO.HIGH)
            GPIO.output(self.R_2, GPIO.LOW)
        elif dir == 'd':
            GPIO.output(self.L_1, GPIO.HIGH)
            GPIO.output(self.L_2, GPIO.LOW)
            GPIO.output(self.R_1, GPIO.LOW)
            GPIO.output(self.R_2, GPIO.HIGH)
        elif dir == 's':
            GPIO.output(self.L_1, GPIO.LOW)
            GPIO.output(self.L_2, GPIO.HIGH)
            GPIO.output(self.R_1, GPIO.LOW)
            GPIO.output(self.R_2, GPIO.HIGH)
        else:
            self.left.ChangeDutyCycle(0.0)
            self.right.ChangeDutyCycle(0.0)
            raise ArgumentError(message='direction must be w, a, d, or s')

    
    def set_effort(self, u):
        """
        Sets how fast the robot will try to go while incorporating control
        effort theta_u

        params:
            - u =   double term from 0 to 1.0 (where 1.0 is the max speed)

        returns:
            - nothing
        """
        self.u = u
        self.left.ChangeDutyCycle(self.theta_u * self.u * 100.0)
        self.right.ChangeDutyCycle((1.0 - self.theta_u) * self.u * 100.0)


    def set_theta_effort(self, theta_u):
        """
        Sets continuous control effort theta_u which controls 'forwards'
        direction.

        params:
            - theta_u = double term, 0.5 is straight ahead (equal effort to both
                        motors), while 1.0 puts all effort in one motor, and 0.0
                        puts all effort into the other motor.
            
        returns:
            - nothing
        """
        self.theta_u = theta_u
        self.set_effort(self.u)