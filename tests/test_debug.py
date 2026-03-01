import logging
import sys
import console_animation
from console_animation import animate

@animate(start="Loading", end="Done")
def demo():
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    
    logger.debug("\nLine 1\nLine 2")
    
demo()
