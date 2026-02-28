from console_animation import animate
import time
import sys

def run_demo_loop():
    i = 0
    try:
        while True:
            i = i + 1
            
            if i >= 50000000:
                print("\nbreaking out of loop")
                break
    except KeyboardInterrupt:
        return

@animate(start="Loading")
def demo():
    try:
        print("\nsomething with a newline at first line")
        run_demo_loop()
        print("\nsomething on newline")
        run_demo_loop()
        print("something on the same line at end\n")
    except KeyboardInterrupt:
        sys.exit(1)

demo()