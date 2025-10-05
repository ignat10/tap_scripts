from .adb_console import adb_run

device = None


def find_device() -> str | None:
    global device
    output = adb_run("devices", capture_output=True, text=True)
    if output is not None:
        lines: list[str] = output.splitlines()
        devices: list[tuple[str, str]] = []
        for line in lines[1::]:
            if line.strip():
                name, status = line.split()
                devices.append((name, status))
        for serial, status in devices:
            if status == "device":
                device = serial
                break
    print(f"find adb devices: {device}")
    return device


def connect_device(serial: str) -> bool:
    output = adb_run(f"connect {serial}", capture_output=True, text=True)
    is_success: bool = output.find(f"connected to {serial}") == 1
    print(f"found {is_success} connected devs")
    return is_success


def get_device_name() -> str | None:
    return device