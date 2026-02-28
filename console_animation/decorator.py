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
    def __init__(self, real_stdout, clear_spinner, lock):
        self.real_stdout = real_stdout
        self.clear_spinner = clear_spinner
        self.lock = lock
        self.cursor_at_start = True

    def write(self, text):
        if not text:
            return
        with self.lock:
            if self.cursor_at_start:
                self.clear_spinner()
            self.real_stdout.write(text)
            self.real_stdout.flush()
            
            if text.endswith('\n'):
                self.cursor_at_start = True
            else:
                self.cursor_at_start = False

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
            write_lock = threading.Lock()

            done_text = end if end else loaded
            spinner_cycle = itertools.cycle(spinner)
            prefix = f"{start} " if start else ""

            def clear_spinner():
                clear_str = " " * (len(prefix) + 2)
                sys.__stdout__.write(f"\r{clear_str}\r")
                sys.__stdout__.flush()

            original_stdout = sys.stdout
            sys.stdout = safe_stdout = SpinnerSafeStdout(original_stdout, clear_spinner, write_lock)

            def spin():
                while not stop_event.is_set():
                    with write_lock:
                        if safe_stdout.cursor_at_start:
                            sys.__stdout__.write(f"\r{prefix}{next(spinner_cycle)}")
                            sys.__stdout__.flush()
                    time.sleep(interval)

            t = threading.Thread(target=spin)
            hide = hide_cursor and sys.__stdout__.isatty()

            if hide:
                sys.__stdout__.write("\033[?25l")
                sys.__stdout__.flush()
            
            t.start()

            try:
                result = func(*args, **kwargs)

                stop_event.set()
                t.join()

                sys.stdout = original_stdout
                with write_lock:
                    if safe_stdout.cursor_at_start:
                        clear_spinner()
                    else:
                        sys.__stdout__.write("\n")
                        sys.__stdout__.flush()

                if done_text:
                    print(done_text)

                if hide:
                    sys.__stdout__.write("\033[?25h")
                    sys.__stdout__.flush()
                    
                return result

            except BaseException:

                stop_event.set()
                t.join()
                
                sys.stdout = original_stdout
                with write_lock:
                    if safe_stdout.cursor_at_start:
                        clear_spinner()
                    else:
                        sys.__stdout__.write("\n")
                        sys.__stdout__.flush()
                
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
