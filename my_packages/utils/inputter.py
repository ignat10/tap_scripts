def farm_number(base_val: int) -> int:
    
    value = input("enter from which google do we start: ")
    try:
        return int(value)
    except ValueError:
        return base_val
