import paho.mqtt.client as mqtt 

class MQTT_Client:
    IP="IP"
    PORT=1883
    USERNAME="username"
    PASSWORD="password"
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(self.USERNAME, self.PASSWORD)
        self.client.connect(self.IP, self.PORT)
        
    def send(self, command):
        self.client.publish("COMMAND", command)
        



        