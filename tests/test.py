from console_animation import animate
import time
import sys

def run_demo_loop():
    i = 0
    try:
        while True:
            i = i + 1
            
            if i >= 50000000:
                break
    except KeyboardInterrupt:
        return

@animate(start="Loading")
def demo():
    try:
        run_demo_loop()
        print("something")
        run_demo_loop()
    except KeyboardInterrupt:
        sys.exit(1)

demo()
