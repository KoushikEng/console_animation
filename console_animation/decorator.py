import sys
import threading
import time
import functools
import itertools
import traceback
from typing import Optional

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
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            stop_event = threading.Event()

            done_text = end if end is not None else loaded
            spinner_cycle = itertools.cycle(spinner)
            prefix = f"{start} " if start else ""

            def animate():
                while not stop_event.is_set():
                    sys.stdout.write(f"\r{prefix}{next(spinner_cycle)}")
                    sys.stdout.flush()
                    time.sleep(interval)

            if hide_cursor:
                sys.stdout.write("\033[?25l")  # Hide cursor
                sys.stdout.flush()

            anim_thread = threading.Thread(target=animate)
            anim_thread.start()

            try:
                result = func(*args, **kwargs)

                stop_event.set()
                anim_thread.join()

                if hide_cursor:
                    sys.stdout.write("\033[?25h")  # Show cursor

                if done_text:
                    sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear the line
                    sys.stdout.write(f"{done_text}\n")
                else:
                    sys.stdout.write("\r")
                    sys.stdout.flush()

                return result

            except Exception as e:
                stop_event.set()
                anim_thread.join()

                if hide_cursor:
                    sys.stdout.write("\033[?25h")  # Show cursor

                sys.stdout.write("\r")
                sys.stdout.flush()

                if error:
                    print(error)
                    traceback.print_exc()
                else:
                    raise  # Let Python handle it naturally

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

