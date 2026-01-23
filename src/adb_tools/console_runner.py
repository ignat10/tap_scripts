from subprocess import run

def adb_run(arguments: str, **kwargs) -> str:
    command = ["adb"] + arguments.split()
    output = run(command, **kwargs)
    return output.stdout
