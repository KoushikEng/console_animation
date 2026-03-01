import sys
import threading
import time
import functools
import itertools
import traceback
import logging
from typing import Optional


class SpinnerSafeStdout:
    """
    A stdout proxy that safely pauses the spinner when writing to stdout or stderr.
    This is necessary because printing to stdout while the spinner is active causes 
    weird artifacts in the spinner animation.
    """
    def __init__(self, real_stream, clear_spinner, lock, cursor_state):
        self.real_stream = real_stream
        self.clear_spinner = clear_spinner
        self.lock = lock
        self.cursor_state = cursor_state

    def write(self, text):
        if not text:
            return
        with self.lock:
            if self.cursor_state[0]:
                self.clear_spinner()
            self.real_stream.write(text)
            self.real_stream.flush()
            
            if text.endswith('\n'):
                self.cursor_state[0] = True
            else:
                self.cursor_state[0] = False

    def flush(self):
        self.real_stream.flush()
    

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

            cursor_state = [True]

            original_stdout = sys.stdout
            original_stderr = sys.stderr

            safe_stdout = SpinnerSafeStdout(original_stdout, clear_spinner, write_lock, cursor_state)
            safe_stderr = SpinnerSafeStdout(original_stderr, clear_spinner, write_lock, cursor_state)

            sys.stdout = safe_stdout
            sys.stderr = safe_stderr

            original_emit = logging.StreamHandler.emit

            def patched_emit(self, record):
                swapped = False
                orig_stream = getattr(self, 'stream', None)
                if orig_stream is original_stdout:
                    self.stream = safe_stdout
                    swapped = True
                elif orig_stream is original_stderr:
                    self.stream = safe_stderr
                    swapped = True
                
                try:
                    original_emit(self, record)
                finally:
                    if swapped:
                        self.stream = orig_stream

            logging.StreamHandler.emit = patched_emit

            def spin():
                while not stop_event.is_set():
                    with write_lock:
                        if cursor_state[0]:
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

                with write_lock:
                    if cursor_state[0]:
                        clear_spinner()
                    else:
                        sys.__stdout__.write("\n")
                        sys.__stdout__.flush()

                sys.stdout = original_stdout
                sys.stderr = original_stderr
                logging.StreamHandler.emit = original_emit

                if done_text:
                    print(done_text)

                if hide:
                    sys.__stdout__.write("\033[?25h")
                    sys.__stdout__.flush()
                    
                return result

            except BaseException:

                stop_event.set()
                t.join()
                
                with write_lock:
                    if cursor_state[0]:
                        clear_spinner()
                    else:
                        sys.__stdout__.write("\n")
                        sys.__stdout__.flush()
                
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                logging.StreamHandler.emit = original_emit

                if hide:
                    sys.__stdout__.write("\033[?25h")
                    sys.__stdout__.flush()
                    
                if error:
                    print(error)
                    traceback.print_exc()
                else:
                    raise
            finally:
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                logging.StreamHandler.emit = original_emit

        return wrapper

    return decorator if _func is None else decorator(_func)
