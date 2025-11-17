from time import sleep

from .console_runner import adb_run



def config() -> str:
    print("connecting adb")
    while True:
        sleep(1)

        if device := _scan():
            print(f"device found: '{device}'")
            return device

        ip = _get_clipboard_ip()
        if not ip:
            continue

        if _connect(ip):
            print(f"connected to device '{ip}'")
            return ip

        print(f"error connecting to device '{ip}'\nretrying...")


def _scan() -> str | None:
    output = adb_run("devices", capture_output=True, text=True)
    lines: list[str] = output.splitlines()
    for line in lines[1::]:
        if not line.strip():
            continue

        name, status = line.split()
        if status == "device":
            return name
        
    return None


def _get_clipboard_ip() -> str | None:
    import pyperclip
    from ..data.poco_coordinates import DEVICE_IP

    clipboard = pyperclip.paste()
    
    if DEVICE_IP not in clipboard:
        print(f"copy your ip:port to clipboard (current: '{clipboard}')")
        return None
    
    return clipboard


def _connect(device: str) -> bool:
    output = adb_run(f"connect {device}", capture_output=True, text=True)
    return "connected" in output
