from subprocess import run
from time import sleep

from screen_objects import device_config


def _run_lines(command: list[str]) -> list[str]:
    return run(command, capture_output=True, text=True).stdout.strip().splitlines()


def _instances():
    return set(_run_lines(['ldconsole', 'list']))


def launch_instance(name: str, serial: str) -> None:
    global instance_name
    assert name in _instances(), f"instance {name} not found in instances: {_instances()}"
    instance_name = name

    run(['ldconsole', 'launch', '--name', name])
    sleep(1)
    while not serial in map(lambda line: line.split()[0].strip(), _run_lines(['adb', 'devices'])[1:]):
        pass
    device_config(serial=serial, app="camel")
    print("loaded instance")


instance_name: str | None = None


def shake() -> None:
    assert instance_name is not None, "Call launch_instance before shake"
    run(['ldconsole', 'action', '--name', instance_name, '--key', 'call.shake', '--value', 'null'])
