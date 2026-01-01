from time import sleep


from ..adb_tools.console_runner import adb_run
from ..utils.inputter import inputter



DEVICE_IP = "192.168.0.192"


def config() -> str:
    print("connecting adb device...")
    while True:
        sleep(1)


        if serial := _scan():
            break

        if (serial := _input_ip()) is None:
            continue

        if _connect(serial):
            continue

        print(f"error connecting to device \nretrying...")
        
    print(f"connected to device '{serial}'")
    return serial


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


def _input_ip() -> str | None:
    port = str(inputter("enter device port: ", 0))
    if len(port) == 5:
        return f"{DEVICE_IP}:{port}"
    return None


def _connect(device: str) -> bool:
    print(f"connecting to {device}...")
    output = adb_run(f"connect {device}", capture_output=True, text=True)
    return "connected" in output
