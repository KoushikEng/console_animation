from console_animation import animate
import time

@animate(start="Loading", loaded="Done!")
def demo():
    time.sleep(2)

demo()
