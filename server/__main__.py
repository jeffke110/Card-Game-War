import logging
import sys
from gameauth import TokenValidator

import server.config as config
from .server import MyServer

LOCAL_IP = ""
LOCAL_PORT = 10020



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format="%(levelname)s %(name)s %(threadName)s %(message)s")

    enable_auth = bool(config.ENABLE_AUTH)
    token_validator = TokenValidator(config.TOKEN_ISSUER_URI, config.PUBLIC_KEY_FILE) if enable_auth else None
    server = MyServer(config.LOCAL_IP, int(config.WS_LISTENER_PORT), token_validator)
    server.run()
    

