import shutil
import os
import platform
import subprocess
import time


def find_chrome_path():
    system = platform.system()

    if system == "Windows":
        possible_paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
    else:
        possible_paths = [
            shutil.which("google-chrome"),
            shutil.which("google-chrome-stable"),
        ]

    for path in possible_paths:
        if path and os.path.exists(path):
            return path
    return None


def open_chrome_debug(url=None, port=9222):
    chrome_path = find_chrome_path()
    if not chrome_path:
        raise RuntimeError("Chrome not found")

    user_data_dir = os.path.join(os.getcwd(), "chrome-debug-profile")

    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "--window-size=1380,1000",
        "--window-position=0,0", 
    ]

    if url:
        cmd.append(url)

    subprocess.Popen(cmd)
    time.sleep(2)
    return True
