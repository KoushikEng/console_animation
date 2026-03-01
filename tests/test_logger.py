from console_animation import animate
import time
import sys

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def run_demo_loop():
    i = 0
    try:
        while True:
            i = i + 1
            
            if i >= 50000000:
                break
    except KeyboardInterrupt:
        return

@animate(start="Loading", end="Done")
def demo():
    try:
        logger.debug("\nsomething with a newline at first line")
        run_demo_loop()
        raise Exception("Something went wrong")
        logger.debug("\nsomething on newline")
        run_demo_loop()
    except Exception:
        logger.error("Exception caught")

demo()