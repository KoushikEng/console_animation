import logging
import sys
import threading
import time

class DummySpinner:
    def __init__(self, stream, lock, name):
        self.stream = stream
        self.lock = lock
        self.name = name
    def write(self, text):
        with self.lock:
            self.stream.write(f"[{self.name}] {text}")
    def flush(self):
        self.stream.flush()

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

logger.info("Before hook")

# Hook
lock = threading.Lock()
orig_stdout = sys.stdout
orig_stderr = sys.stderr

safe_stdout = DummySpinner(orig_stdout, lock, "STDOUT_SAFE")
safe_stderr = DummySpinner(orig_stderr, lock, "STDERR_SAFE")

sys.stdout = safe_stdout
sys.stderr = safe_stderr

orig_emit = logging.StreamHandler.emit

def patched_emit(self, record):
    swapped = False
    orig_stream = self.stream
    if self.stream is orig_stdout:
        self.stream = safe_stdout
        swapped = True
    elif self.stream is orig_stderr:
        self.stream = safe_stderr
        swapped = True
        
    try:
        orig_emit(self, record)
    finally:
        if swapped:
            self.stream = orig_stream

logging.StreamHandler.emit = patched_emit

logger.info("During hook")

sys.stdout = orig_stdout
sys.stderr = orig_stderr
logging.StreamHandler.emit = orig_emit

logger.info("After hook")
