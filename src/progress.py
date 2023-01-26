import subprocess
import threading
import os

cmd = [
    "av1an",
    "-i", "/home/gianni4770k/Videos/PolyMC_Tutorial_Windows2.mp4",
    "-y",
    "--split-method", "av-scenechange",
    "-m", "hybrid",
    "-c", "ffmpeg",
    "-e", "rav1e",
    "--force",
    "--video-params", "--tiles 1 -s 6 --quantizer 100 --threads 1",
    "-w", "0",
    "-o", "/home/gianni4770k/Videos/PolyMC_Tutorial_Windows2-aviator.mkv",
]
print(cmd)
process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True)
print("starting...")
for line in process.stdout:
    print(line)
print("waiting")
process.wait()
print("done")