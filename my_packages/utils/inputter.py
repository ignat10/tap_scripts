def farm_number() -> int:
    number = input("enter from which google do we start: ")

    if number.isdigit():
        return int(number)
    else:
        return 0