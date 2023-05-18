from gamecomm.client import GameClient

class MyGameClient(GameClient):
    
    def __init__(self, url, token=None, on_event=None, info=dict):
        # if overriding (e.g. to add additional parameters above), you
        # MUST call the superclass implementation of this method as follows
        super().__init__(url, token, on_event)
        self.info = info

    def is_event(self, message: dict):
        return "event" in message

    def is_success(self, response: dict):
        return response["status"] == "ok"

    def start(self):
        super().start()

    def stop(self):
        super().stop()

    def on_success(self, response : dict):
        print(response)

    def on_error(self, response : dict):
        print(response)
        
    def send_message(self, message):
        """Sends a message to the server"""
        self.send(message, on_success = self.on_success, on_error = self.on_error)