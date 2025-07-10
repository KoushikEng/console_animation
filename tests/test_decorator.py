import time
from console_animation import animate

def test_loading_animation_runs_without_error():
    @animate(start="Running test...", loaded="Test done.")
    def quick_task():
        time.sleep(1)
        return True

    assert quick_task() is True
