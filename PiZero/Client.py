import paho.mqtt.client as mqtt

class Mqtt_Client(mqtt.Client):
    USERNAME = "ragkar"
    PASSWORD = "rakgar"
    BROKER_IP = "192.168.1.103"
    BROKER_PORT = 1883
    TOPIC = "COMMAND"
    
    def __init__(self, motor):
        super().__init__()
        self.motor = motor

    def on_connect(self, client, obj, flags, rc):
        print("Connected!")

    def on_message(self, client, userdata, msg):
        print(str(msg.payload.decode("utf-8")))
        self.motor.control(str(msg.payload.decode("utf-8")))

    def run(self):
        self.username_pw_set(self.USERNAME, self.PASSWORD)
        self.connect(self.BROKER_IP, self.BROKER_PORT, 60)
        self.subscribe(self.TOPIC)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
    