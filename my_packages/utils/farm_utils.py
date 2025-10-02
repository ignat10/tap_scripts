from time import sleep

from my_packages.core.adb_console import click
from my_packages.data.poco_coordinates import points, STEPS
from my_packages.image_tools import get_coords, screen_states


def wait_and_click(coords: tuple[int, int], delay=0.5):
    sleep(delay)
    click(coords)


def repeat_click(coords: tuple[int, int], times: int):
    for _ in range(times):
        click(coords)


def point_step(name: str,
               index: int,
               times: int,
               ) -> tuple[int, int]:

    point: list[int] = list[int](points[name])
    step = STEPS[name]
    print(f"point: {point}, index: {index} step: {step}, times: {times}, name: [{name}]")
    point[index] += step * times
    print(f"return point: {point}")
    assert points[name] != point, f"point after step hasn't been changed: {point}"
    return tuple[int,int](point)


def close_add():
    print("Closing add...")
    while not screen_states.main_menu():
        coords = get_coords.x() or points["close"]
        click(coords)


def gather_mine():
    wait_and_click(points["gather"])
    wait_and_click(points["go"])
    wait_and_click(points["back"])


def loading():
    while screen_states.loading():
        print("loading")
    print("loaded")


def lord_skills():
    print("Harvesting...")
    wait_and_click(points["lord"])
    wait_and_click(points["harvest"])
    wait_and_click(points["use"])
    print("end harvest")
    wait_and_click(points["recall_all"])
    wait_and_click(points["use"])
    print("end recall_all")
    wait_and_click(points["close"])
    wait_and_click(points["close"])


def inside():
    loading()
    print("running inside")  # Inside the castle
    close_add()
    lord_skills()
    click(points["map"])
    print("finished inside")