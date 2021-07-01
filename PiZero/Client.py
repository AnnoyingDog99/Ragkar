import paho.mqtt.client as mqtt

class Mqtt_Client(mqtt.Client):
    USERNAME = "ENTER_USERNAME_HERE"
    PASSWORD = "ENTER_PASSWORD_HERE"
    BROKER_IP = "ENTER_BROKER_IP_HERE"
    BROKER_PORT = 1883
    TOPIC = "ENTER_MQTT_TOPIC_HERE"
    
    def __init__(self, motor, app):
        super().__init__()
        self.motor = motor
        self.app = app

    def on_connect(self, client, obj, flags, rc):
        self.client = client
        print("Connected!")
        self.app.set_connected(True)

    def on_message(self, client, userdata, msg):
        self.motor.set_current_command(str(msg.payload.decode("utf-8")))
        print(str(msg.payload.decode("utf-8")))
        
    def on_disconnect(self, client, userdata, rc=0):
        print("Disconnected!")
        self.loop.stop()

    def run(self):
        self.username_pw_set(self.USERNAME, self.PASSWORD)
        self.connect(self.BROKER_IP, self.BROKER_PORT, 60)
        self.subscribe(self.TOPIC)
        self.loop_start()
    