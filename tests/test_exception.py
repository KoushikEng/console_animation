from console_animation import animate
import time
import sys


def run_demo_loop():
    i = 0
    try:
        while True:
            i = i + 1
            
            if i >= 100000000:
                break
    except KeyboardInterrupt:
        return

@animate(start="Loading")
def demo():
    try:
        run_demo_loop()
        print("something")
        print("something else\n")
        raise RuntimeError("This is a test exception")
        run_demo_loop()
    except Exception as e:
        print(f"Caught an exception: {e}")
        sys.exit(1)
        return "Exiting gracefully after catching the exception"


if __name__ == "__main__":
    demo()