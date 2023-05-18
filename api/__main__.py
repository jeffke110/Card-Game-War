import argparse
import logging

from .app import app


LOCAL_IP = "127.0.0.1"
API_PORT = "10021"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--debug", action="store_true", help="enable debug logging")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s")

    app.run(host=LOCAL_IP, port=int(API_PORT), debug=args.debug)
