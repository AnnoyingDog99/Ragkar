import RPi.GPIO as GPIO
import threading

class Motor:

    def __init__(self, pwma_pin, pwmb_pin, ain1_pin, ain2_pin, bin1_pin, bin2_pin, stby_pin):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        # Motor 1: forwards/backwards
        self.ain1_pin = ain1_pin
        self.ain2_pin = ain2_pin
        # Motor 2: left/right
        self.bin1_pin = bin1_pin
        self.bin2_pin = bin2_pin
        
        self.stby_pin = stby_pin

        GPIO.setup(pwma_pin, GPIO.OUT)
        GPIO.setup(pwmb_pin, GPIO.OUT)
        GPIO.setup(ain1_pin, GPIO.OUT)
        GPIO.setup(ain2_pin, GPIO.OUT)
        GPIO.setup(bin1_pin, GPIO.OUT)
        GPIO.setup(bin2_pin, GPIO.OUT)
        GPIO.setup(stby_pin, GPIO.OUT)

        self.pwma = GPIO.PWM(pwma_pin, 100)
        self.pwmb = GPIO.PWM(pwmb_pin, 100)
        self.pwma.start(100)
        self.pwmb.start(100)

        self.commands = {
            "GO_FORWARDS": self.forward,
            "GO_BACKWARDS": self.reverse,
            "TURN_LEFT": self.left,
            "TURN_RIGHT": self.right,
            "FORWARD_TURN_LEFT": self.forward_left,
            "FORWARD_TURN_RIGHT": self.forward_right,
            "BACKWARD_TURN_LEFT": self.reverse_left,
            "BACKWARD_TURN_RIGHT": self.reverse_right,
            "NONE": self.off,
        }

        self.current_command = "NONE"

    def get_current_command(self):
        return self.current_command
    
    def set_current_command(self, command):
        self.current_command = command

    def control(self, command):
        self.commands[command]()

    # 0 is forward/backwards
    # 1 is left/right
    def forward(self):
        self.run_motor(0, 60, 0)
        self.run_motor(1, 0, 0)

    def reverse(self):
        self.run_motor(0, 60, 1)
        self.run_motor(1, 0, 0)

    def left(self):
        self.run_motor(0, 0, 0)
        self.run_motor(1, 40, 0)

    def right(self):
        self.run_motor(0, 0, 0)
        self.run_motor(1, 40, 1)

    def forward_left(self):
        self.run_motor(0, 60, 0)
        self.run_motor(1, 20, 0)

    def forward_right(self):
        self.run_motor(0, 60, 0)
        self.run_motor(1, 20, 1)
    
    def reverse_left(self):
        self.run_motor(0, 60, 1)
        self.run_motor(1, 20, 0)

    def reverse_right(self):
        self.run_motor(0, 60, 1)
        self.run_motor(1, 20, 1)
    
    def off(self):
        self.run_motor(0, 0, 0)
        self.run_motor(1, 0, 0)
        
    def run_motor(self, motor, speed, direction):
        GPIO.output(self.stby_pin, GPIO.HIGH);
        in1 = GPIO.HIGH
        in2 = GPIO.LOW

        if(direction == 1):
            in1 = GPIO.LOW
            in2 = GPIO.HIGH

        if(motor == 0):
            GPIO.output(self.ain1_pin, in1)
            GPIO.output(self.ain2_pin, in2)
            self.pwma.ChangeDutyCycle(speed)
        elif(motor == 1):
            GPIO.output(self.bin1_pin, in1)
            GPIO.output(self.bin2_pin, in2)
            self.pwmb.ChangeDutyCycle(speed)