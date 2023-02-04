import subprocess
import threading
import os
import time


def run_in_thread():
    i = 0
    while i < 10:
        print(i)
        time.sleep(1)
        i += 1

thread = threading.Thread(target=run_in_thread)
thread.start()

i = 0
while True:
    print(str(i) + " second")
    time.sleep(1)
    i += 1

