import threading
from Client import Mqtt_Client
from MotorV3 import Motor

if __name__ == "__main__":
    motor = Motor(12, 11, 16, 18, 15, 13, 22)
    client = Mqtt_Client(motor)
    thread = threading.Thread(target=client.run)
    thread.start()
