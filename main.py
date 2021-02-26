import random
from splinter import Browser
import time
from selenium.webdriver.remote.errorhandler import UnexpectedAlertPresentException

UNCLICKED = "UNCLICKED"
FLAGGED = "FLAGGED"
BOMB_DEATH = "BOMB_DEATH"
BOMB_REVEALED = "BOMB_REVEALED"
COMPLETED = "COMPLETED"
large_size = (29, 15)
med_size = (15, 15)
small_size = (8, 8)
large_url = "https://minesweeperonline.com/#"
medium_url = "https://minesweeperonline.com/#intermediate"
small_url = "https://minesweeperonline.com/#beginner"

cell_class_dict = {
    "square blank": UNCLICKED,
    "square bombdeath": BOMB_DEATH,
    "square bombrevealed": BOMB_REVEALED,
    "square bombflagged": FLAGGED,
    "square bombmisflagged": FLAGGED
}

browser = Browser('firefox')


def grid_print(grid):
    n = 0
    for each in grid:
        print("row " + str(n) + ": " + str(each))
        n = n + 1


def right_click_cell(cell):
    cell_id = get_cell_id(cell)
    if read_cell(cell) == UNCLICKED:
        browser.find_by_id(cell_id).right_click()
        print("Right click performed on cell: " + str(cell[0]) + ", " + str(cell[1]))
    else:
        print("Right click was called but cell was already flagged: " + str(cell[0]) + ", " + str(cell[1]))


def left_click_cell(cell):
    cell_id = get_cell_id(cell)
    browser.find_by_id(cell_id).click()


def get_cell_id(cell):
    cell_id = str(cell[1] + 1) + "_" + str(cell[0] + 1)
    return cell_id


def read_cell(cell):
    cell_id = get_cell_id(cell)
    cell_class = browser.find_by_id(cell_id).first["class"]
    if "square open" in cell_class:
        return int(cell_class[-1])
    else:
        return cell_class_dict[cell_class]


def cell_is_int_greater_than_0(cell_value):
    return isinstance(cell_value, int) and cell_value > 0


def read_cells(grid):
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            if get_grid_cell(x, y, grid) == UNCLICKED:
                set_grid_cell(x, y, grid, read_cell([x, y]))
    return grid


def is_game_over(grid):
    for each in grid:
        if BOMB_DEATH in each or BOMB_REVEALED in each:
            print("Game Lost")
            return True
    return False


def remove_many_agnostic_to_existance(a_list: list, values: list):
    for value in values:
        if value in a_list:
            a_list.remove(value)


def click_if_flags_are_greater_than_spot_num(x, y, grid, size):
    spot_number = get_grid_cell(x, y, grid)
    flagged_adj_count, unclicked_adjacents, numbered_adjacents \
        = get_unclicked_adj_and_flagged_adj_count(grid, size, x, y)
    if int(spot_number) > flagged_adj_count and int(spot_number) == len(unclicked_adjacents) + flagged_adj_count:
        print("Right clicking unclicked adjacents of cell: {x}, {y}".format(**{"x": x, "y": y}))
        for cell in unclicked_adjacents:
            right_click_cell(cell)
        set_grid_cell(x, y, grid, COMPLETED)
        return True
    elif flagged_adj_count == spot_number and len(unclicked_adjacents) > 0:
        for cell in unclicked_adjacents:
            left_click_cell(cell)
        set_grid_cell(x, y, grid, COMPLETED)
        return True
    elif spot_number == flagged_adj_count + 1 and len(unclicked_adjacents) == 2:
        print("2 reference case first parameter met for cell: " + str([x, y]))
        print("numbered_adjacents: " + str(numbered_adjacents))
        for numbered_adj_cell in numbered_adjacents:
            adj_flagged_adj_count, adj_unclicked_adjacents, adj_numbered_adjacents \
                = get_unclicked_adj_and_flagged_adj_count(grid, size, numbered_adj_cell[0], numbered_adj_cell[1])
            if 1 == get_grid_cell(numbered_adj_cell[0], numbered_adj_cell[1], grid) - adj_flagged_adj_count:
                print("checking for numbered_adj_cell: " + str(numbered_adj_cell))
                if len(adj_unclicked_adjacents) == 3:
                    differences = []
                    print("unclicked_adjacents: " + str(unclicked_adjacents))
                    print("adj_unclicked_adjacents: " + str(adj_unclicked_adjacents))
                    for a_list in adj_unclicked_adjacents:
                        if a_list not in unclicked_adjacents:
                            differences.append(a_list)
                    print("differences: " + str(differences))
                    if len(differences) == 1:
                        print("Left clicking difference")
                        for cell in differences:
                            left_click_cell(cell)
                elif len(unclicked_adjacents) == 2:
                    print("Checking t bone scenario")
                    go_ahead = True
                    for a_list in unclicked_adjacents:
                        if a_list not in adj_unclicked_adjacents:
                            go_ahead = False
                    if go_ahead:
                        differences = []
                        for a_list in adj_unclicked_adjacents:
                            if a_list not in unclicked_adjacents:
                                differences.append(a_list)
                        for cell in differences:
                            print("Left clicking on t bone cells: " + str(differences))
                            left_click_cell(cell)
            elif 2 == get_grid_cell(numbered_adj_cell[0], numbered_adj_cell[1], grid) - adj_flagged_adj_count:
                if len(adj_unclicked_adjacents) == 3:
                    differences = []
                    print("unclicked_adjacents: " + str(unclicked_adjacents))
                    print("adj_unclicked_adjacents: " + str(adj_unclicked_adjacents))
                    for a_list in adj_unclicked_adjacents:
                        if a_list not in unclicked_adjacents:
                            differences.append(a_list)
                    print("differences: " + str(differences))
                    if len(differences) == 1:
                        print("Right clicking difference")
                        for cell in differences:
                            right_click_cell(cell)
    else:
        return False


def get_unclicked_adj_and_flagged_adj_count(grid, size, x, y):
    flagged_adj_count = 0
    unclicked_adjacents = []
    numbered_adjacents = []
    adj_spots = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ]
    if x == 0:
        remove_many_agnostic_to_existance(adj_spots, [(-1, -1), (-1, 0), (-1, 1)])
    if x == size[0]:
        remove_many_agnostic_to_existance(adj_spots, [(1, -1), (1, 0), (1, 1)])
    if y == 0:
        remove_many_agnostic_to_existance(adj_spots, [(-1, -1), (0, -1), (1, -1)])
    if y == size[1]:
        remove_many_agnostic_to_existance(adj_spots, [(-1, 1), (0, 1), (1, 1)])
    for spot in adj_spots:
        spot_to_check = [x + spot[0], y + spot[1]]
        grid_content_at_spot_to_check = get_grid_cell(spot_to_check[0], spot_to_check[1], grid)
        if grid_content_at_spot_to_check == FLAGGED:
            flagged_adj_count = flagged_adj_count + 1
        elif grid_content_at_spot_to_check == UNCLICKED:
            unclicked_adjacents.append(spot_to_check)
        elif cell_is_int_greater_than_0(grid_content_at_spot_to_check):
            numbered_adjacents.append(spot_to_check)
            #print("numbered_adjacents: " + str(numbered_adjacents))
    return flagged_adj_count, unclicked_adjacents, numbered_adjacents


def get_grid_cell(x, y, grid):
    try:
        return grid[y][x]
    except IndexError as e:
        print("Index error on get grid for cell: " + str([x, y]))
        raise e


def set_grid_cell(x, y, grid, new_value):
    try:
        grid[y][x] = new_value
    except IndexError as e:
        print("Index error on set grid for cell: " + str([x, y]))
        raise e


def cycle_through_number_cells(grid, size):
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if cell_is_int_greater_than_0(get_grid_cell(x, y, grid)):
                if click_if_flags_are_greater_than_spot_num(x, y, grid, size):
                    return True
    print("Cycled through every cell without making a move")
    #time.sleep(1)
    return False


def play_new_game(autoplay):
    if not autoplay:
        input("Press enter to continue...")


def open_minesweeper_webpage():
    while True:
        size_input = input("Want to play a small, medium, or large game? (s, m, l): ")
        if size_input.upper() == "L":
            url = large_url
            size = large_size
            break
        elif size_input.upper() == "M":
            url = medium_url
            size = med_size
            break
        elif size_input.upper() == "S":
            url = small_url
            size = small_size
            break
        else:
            print("Sorry, please input s, m, or l")
    co_op = input("Co-Op? y/n: ")
    if co_op.upper() == "Y":
        co_op = True
        autoplay = False
    else:
        co_op = False
        autoplay = input("Autoplay? y/n: ")
        if autoplay.upper() == "Y":
            autoplay = True
        else:
            autoplay = False
    browser.visit(url)
    while True:
        try:
            browser.find_by_id("face").first.click()
            starting_click = (random.randint(1, size[0] - 1), random.randint(1, size[1] - 1))
            print("starting_click: " + str(starting_click))
            left_click_cell(starting_click)
            print("starting bot while loop")
            game_over = False
            grid = [[UNCLICKED] * (size[0] + 1) for _ in range((size[1] + 1))]
            while not game_over:
                grid = read_cells(grid)
                if not cycle_through_number_cells(grid, size) and not co_op:
                    game_over = True
                elif browser.find_by_id("face")["class"] == "facewin":
                    print("Game won")
                    game_over = True
                else:
                    game_over = is_game_over(grid)
            play_new_game(autoplay)
        except UnexpectedAlertPresentException as e:
            print("Score alert pop up found")
            play_new_game(autoplay)



if __name__ == '__main__':
    open_minesweeper_webpage()

