def farm_number():
    number = input("enter from which farm do we start: ")

    if number.isdigit():
        return int(number)
    else:
        return 0