import sys
import threading
import time
import functools
import itertools
import traceback
from typing import Optional


class SpinnerSafeStdout:
    """
    A stdout proxy that safely pauses the spinner when writing to stdout.
    This is necessary because printing to stdout while the spinner is active causes 
    weird artifacts in the spinner animation.
    """
    def __init__(self, real_stdout, pause_spinner, resume_spinner):
        self.real_stdout = real_stdout
        self.pause_spinner = pause_spinner
        self.resume_spinner = resume_spinner

    def write(self, text):
        self.pause_spinner()
        self.real_stdout.write(text)
        self.real_stdout.flush()
        self.resume_spinner()

    def flush(self):
        self.real_stdout.flush()
    

def animate(
    _func=None,
    *,
    start: Optional[str] = None,
    end: Optional[str] = None,
    loaded: Optional[str] = None,
    error: Optional[str] = None,
    spinner: str = "|/-\\",
    interval: float = 0.1,
    hide_cursor: bool = True
):
    """
    An animated spinner that shows while the function is running.
    
    Args:
    _func: The function to decorate. (Do not use this directly.)
    start: The text to display before the spinner.
    end: The text to display after the spinner. If None, uses loaded.
    loaded: The text to display after the spinner when successful.
    error: The text to display after the spinner when an error occurs.
    spinner: The spinner characters to use.
    interval: The interval between spinner characters.
    hide_cursor: Whether to hide the cursor while the spinner is active.

    Returns:
    The decorated function.
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            stop_event = threading.Event()
            pause_event = threading.Event()
            pause_event.clear()

            done_text = end if end else loaded
            spinner_cycle = itertools.cycle(spinner)
            prefix = f"{start} " if start else ""

            def spin():
                while not stop_event.is_set():
                    if not pause_event.is_set():
                        sys.__stdout__.write(f"\r{prefix}{next(spinner_cycle)}")
                        sys.__stdout__.flush()
                    time.sleep(interval)

            def pause():
                pause_event.set()
                sys.__stdout__.write("\r")
                sys.__stdout__.flush()

            def resume():
                pause_event.clear()

            t = threading.Thread(target=spin)
            hide = hide_cursor and sys.__stdout__.isatty()

            if hide:
                sys.__stdout__.write("\033[?25l")
                sys.__stdout__.flush()
            
            t.start()

            original_stdout = sys.stdout
            sys.stdout = SpinnerSafeStdout(original_stdout, pause, resume)

            try:
                result = func(*args, **kwargs)

                stop_event.set()
                t.join()

                sys.stdout = original_stdout
                sys.__stdout__.write("\r")

                if done_text:
                    print(done_text)

                if hide:
                    sys.__stdout__.write("\033[?25h")
                    sys.__stdout__.flush()
                    
                return result

            except Exception:

                stop_event.set()
                t.join()
                sys.stdout = original_stdout
                sys.__stdout__.write("\r")
                
                if hide:
                    sys.__stdout__.write("\033[?25h")
                    sys.__stdout__.flush()
                    
                if error:
                    print(error)
                    traceback.print_exc()
                else:
                    raise

        return wrapper

    return decorator if _func is None else decorator(_func)

