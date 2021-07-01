import threading
from Client import Mqtt_Client
from MotorV3 import Motor
import time

class App:
    is_connected = False
    
    def set_connected(self, is_connected):
        self.is_connected = is_connected
        
    def start(self, motor):
        if self.is_connected:
            motor.start_motors()
        else:
            time.sleep(1)
            self.start(motor)
            

if __name__ == "__main__":
    app = App()
    motor = Motor(12, 11, 18, 16, 15, 13, 22) 
    client = Mqtt_Client(motor, app)
    thread = threading.Thread(target=client.run)
    thread.start()
    app.start(motor)
    
