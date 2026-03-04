from time import sleep


from ..adb_tools.console_runner import adb_run
from ..utils.inputter import inputter


_ADB_PORT_LENGTH = 5
DEVICE_IP = "192.168.0.192"


def configure_device() -> str:
    print("connecting adb device...")

    serial: str | None = _scan()
    while serial is None:
        if (ip := _input_ip()) is not None:
            _connect(ip)

        serial = _scan()

        
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
    if len(port) == _ADB_PORT_LENGTH:
        return f"{DEVICE_IP}:{port}"
    return None


def _connect(device: str) -> bool:
    print(f"connecting to {device}...")
    output = adb_run(f"connect {device}", capture_output=True, text=True)
    return "connected" in output
