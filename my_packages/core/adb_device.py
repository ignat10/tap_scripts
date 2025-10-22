from .adb_console import adb_run


class AdbDevice:
    def __init__(self):
        self.device = None
        self.is_connected = False


    def find(self):
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
                    self.device = serial
                    break
        print(f"find adb devices self.device: {self.device}")

    def connect(self, dev: str) -> None:
        output = adb_run(f"connect {dev}", capture_output=True, text=True)
        success: bool = f"connected to {dev}" in output
        print(f"success connection: {success}")
        self.is_connected = success

    def action(self, arguments: str, **kwargs) -> str:
        command = f"-s {self.device} {arguments}"
        return adb_run(command, **kwargs)

device = AdbDevice()