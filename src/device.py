from subprocess import run
from time import sleep

from screen_objects import device_config


def _run_lines(command: list[str]) -> list[str]:
    return run(command, capture_output=True, text=True).stdout.strip().splitlines()


def _instances():
    return set(_run_lines(['ldconsole', 'list']))


def launch_instance(name: str, serial: str) -> None:
    assert name in _instances(), f"instance {name} not found in instances: {_instances()}"

    run(['ldconsole', 'launch', '--name', name])
    sleep(1)
    while not serial in map(lambda line: line.split()[0].strip(), _run_lines(['adb', 'devices'])[1:]):
        pass
    device_config(serial=serial, app="camel")
    print("loaded instance")
