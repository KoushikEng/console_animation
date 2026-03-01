import logging
import sys
import threading
import time

class DummySpinner:
    def __init__(self, stream, lock):
        self.stream = stream
        self.lock = lock
    def write(self, text):
        with self.lock:
            self.stream.write(f"HOOKED: {text}")
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
safe_stdout = DummySpinner(sys.stdout, lock)

sys.stdout = safe_stdout
patched = []
for handler in logger.handlers:
    if getattr(handler, 'stream', None) is orig_stdout:
        handler.stream = safe_stdout
        patched.append((handler, orig_stdout))

logger.info("During hook")

for handler, orig in patched:
    handler.stream = orig
sys.stdout = orig_stdout

logger.info("After hook")
