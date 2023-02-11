import subprocess
import threading
import os
import time

cmd = [
    "/home/gianni13700k/Documents/projects/av1an-nate/target/release/av1an",
    "-i", "/home/gianni13700k/Videos/marq-ipgon.webm",
    "-y",
    "--split-method", "av-scenechange",
    "-m", "hybrid",
    "-c", "ffmpeg",
    "-e", "rav1e",
    "--force",
    "--video-params", "--tiles 1 -s 6 --quantizer 100 --threads 1",
    "-w", "0",
    "-o", "/home/gianni13700k/Videos/marq-ipgon-rAV1ator.mkv",
]
print(" ".join(cmd))
process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True)
# last update
last_update = time.time()
for line in process.stdout:
    tokens = line.strip().split("/")
    if len(tokens) == 2:
        progress = int(tokens[0])/int(tokens[1])
        progress = round(progress,2)
        if time.time() - last_update > 1:
            print(progress)
            last_update = time.time()
process.wait()