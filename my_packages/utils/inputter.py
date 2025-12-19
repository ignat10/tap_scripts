def inputter(msg: str, base):
    type_ = type(base)
    string = input(msg)
    try:
        return type_(string)
    except ValueError:
        return base
