import websockets
import asyncio
from MQTT_Client import MQTT_Client

class Websocket:
    
    def __init__(self):
        self.start_server = websockets.serve(self.command_rec, "localhost", 3333)
        self.client = MQTT_Client()
        
    def start_ws(self):
        print("starting ws...")
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()
        
    async def command_rec(self, websocket, path):
        while True:
            command = await websocket.recv()
            self.client.send(command)
            print(command)
        
if __name__ == '__main__':
    ws = Websocket()
    ws.start_ws()
