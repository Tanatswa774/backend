import subprocess
import os

DEVICE = "127.0.0.1:21503"  # Your emulator's ADB address

def adb(command: str) -> bytes:
    full_cmd = f'adb -s {DEVICE} {command}'
    print(f"Running ADB command: {full_cmd}")
    try:
        return subprocess.check_output(full_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"ADB error: {e}")
        return b""

def tap(x: int, y: int):
    print(f"Tapping at ({x}, {y})")
    adb(f'shell input tap {x} {y}')

def swipe(x1: int, y1: int, x2: int, y2: int, duration=300):
    print(f"Swiping from ({x1}, {y1}) to ({x2}, {y2})")
    adb(f'shell input swipe {x1} {y1} {x2} {y2} {duration}')

def take_screenshot(filename: str = "screenshot.png"):
    path = os.path.abspath(filename)
    print(f"Saving screenshot to {path}")
    data = adb("exec-out screencap -p")
    if data:
        with open(path, "wb") as f:
            f.write(data)
