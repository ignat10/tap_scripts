def get_mine(): # to go to basic mine from the map
    global mine_type, color, lv, witch_mine
    os.system(f"{ADB} shell input tap {point_search[0]} {point_search[1]}")
    find_another()
    while True:
        check_color(point_search_back)
        if all(abs(a - t) < 15 for a, t in zip(color, (50, 48, 40, 255))):  # put #(XXX, XXX, XXX)
            check_color(point_gather)
            wait()
            if all(abs(a - t) < 5 for a, t in zip(color, (46, 37, 43, 255))):
                wait()
                gather_mine()
                break
            else:
                os.system(f"{ADB} shell input tap {point_mine[0]} {point_mine[1]}")
                gather_mine()
                break
        else:
            find_another()
            check_color(point_gather)
            if all(abs(a - t) < 5 for a, t in zip(color, (46, 37, 43, 255))):# put #(XXX, XXX, XXX) # I think that is good color                             # if found
                wait()
                gather_mine()
                break
            else:
                wait()
                os.system(f"{ADB} shell input tap {point_mine[0]} {point_mine[1]}")
                check_color(point_gather)    # check color of point_gather
                if all(abs(a - t) < 5 for a, t in zip(color, (46, 37, 43, 255))):
                    gather_mine()
                    break
                else:           # if not found
                    if mine_type < 470:
                        mine_type += 162
                    else:
                        mine_type = 0
                        lv += 1
                    find_another()
    witch_mine += 1