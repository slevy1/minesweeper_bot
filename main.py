import msvcrt
from selenium import webdriver
from selenium.webdriver import ActionChains
import random
import pprint
import time
from  splinter import Browser

UNCLICKED = "UNCLICKED"
FLAGGED = "FLAGGED"
BOMB_DEATH = "BOMB_DEATH"
BOMB_REVEALED = "BOMB_REVEALED"
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
# selenium
# driver = webdriver.Firefox()
# actionChains = ActionChains(driver)

# splinter
browser = Browser('firefox')


def grid_print(grid):
    n = 0
    for each in grid:
        #print("row " + str(n) + ": " + str(each))
        n = n + 1


def right_click_cell(cell, grid, c=1):
    #time.sleep(2)
    #print("Reading cell {cell}, with value {value} before right click to make sure that it is not flagged.".format(cell=cell, value=read_cell(cell)))
    #if read_cell(cell) != FLAGGED:
    cell_id = get_cell_id(cell)
    browser.find_by_id(cell_id).right_click()
    print("Right click performed on cell: " + str(cell[0]) + ", " + str(cell[1]) + ": " + str(grid_cell(cell[0], cell[1], grid)))
        #time.sleep(2)
        #if read_cell(cell) != FLAGGED:
         #   print("Cell is not flagged even though it is supposed to be, right clicking cell again. retry count = " + str(c))
          #  right_click_cell(cell, grid, c=c+1)
    #else:
    #    print("For some reason right click was called on a cell that was already flagged")


def left_click_cell(cell):
    cell_id = get_cell_id(cell)
    browser.find_by_id(cell_id).click()


def get_cell_id(cell):
    cell_id = str(cell[1] + 1) + "_" + str(cell[0] + 1)
    return cell_id


def read_cell(cell):
    cell_id = get_cell_id(cell)
    #print(cell_id)
    cell_class = browser.find_by_id(cell_id).first["class"]
    if "square open" in cell_class:
        return int(cell_class[-1])
    else:
        return cell_class_dict[cell_class]


def cell_is_int_greater_than_0(cell):
    return isinstance(cell, int) and cell > 0


def read_cells(size):
    grid = []
    for y in range(0, size[0] + 1):
        row = []
        for x in range(0, size[1] + 1):
            cell_def = read_cell([x, y])
            #print(str(x-1) + ", " + str(y-1) + ": " + str(cell_def))
            row.append(cell_def)
            #grid[x-1][y-1] = cell_def
        grid.append(row)
    grid_print(grid)
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
    #print("starting click_if_flags_are_greater_than_spot_num")
    spot_number = grid_cell(x, y, grid)
    flagged_adj_count = 0
    unclicked_adjacents = []
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
    #print("Spot: " + str(x) + ", " + str(y))
    #print("adj_spots: " + str(adj_spots))
    for spot in adj_spots:
        spot_to_check = [x+spot[0], y+spot[1]]
        grid_content_at_spot_to_check = grid[spot_to_check[1]][spot_to_check[0]]
        if grid_content_at_spot_to_check == FLAGGED:
            flagged_adj_count = flagged_adj_count + 1
        elif grid_content_at_spot_to_check == UNCLICKED:
            unclicked_adjacents.append(spot_to_check)
    if int(spot_number) > flagged_adj_count and int(spot_number) == len(unclicked_adjacents) + flagged_adj_count:
        print("Right clicking unclicked_adjacents on cell: {x}, {y}".format(**{"x": x, "y": y}))
        for cell in unclicked_adjacents:
            right_click_cell(cell, grid)
        return True
    elif flagged_adj_count == spot_number and len(unclicked_adjacents) > 0:
        #print("unclicked_adjacents: " + str(unclicked_adjacents))
        for cell in unclicked_adjacents:
            left_click_cell(cell)
        return True
    else:
        return False


def grid_cell(x, y, grid):
    try:
        return grid[y][x]
    except IndexError as e:
        print("Index error on grid for cell: " + str([x, y]))
        return None


def click_on_unclicked_if_algos(grid, x, y, size):
    # 1 corner 1
    if x > 0 and y > 0 and grid[y-1][x-1] == 1 \
            and cell_is_int_greater_than_0(grid_cell(x - 1, y, grid)) \
            and cell_is_int_greater_than_0(grid_cell(x, y - 1, grid)):
        right_click_cell((x, y), grid)
        print("True on 1 corner 1")
        return True
    # 1 corner 2
    elif x < size[0] and y < size[1] and grid_cell(x + 1, y + 1, grid) == 1 \
            and cell_is_int_greater_than_0(grid_cell(x+1, y, grid)) \
            and cell_is_int_greater_than_0(grid_cell(x, y + 1, grid)):
        right_click_cell((x, y), grid)
        print("True on 1 corner 2")
        return True
    elif x < size[0] and y > 0 and grid_cell(x + 1, y - 1, grid) == 1 \
            and cell_is_int_greater_than_0(grid_cell(x, y - 1, grid)) \
            and cell_is_int_greater_than_0(grid_cell(x + 1, y, grid)):
        right_click_cell((x, y), grid)
        print("True on 1 corner 3")
        return True
    return False


def check_cell_unclicked(grid, size):
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid_cell(x, y, grid) == UNCLICKED:
                if click_on_unclicked_if_algos(grid, x, y, size):
                    return True
            elif cell_is_int_greater_than_0(grid_cell(x, y, grid)):
                if click_if_flags_are_greater_than_spot_num(x, y, grid, size):
                    return True
    return False



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

    # driver.get(url)
    browser.visit(url)
    while True:
        start_input = input("start a new game? y/n: ")
        if start_input.upper() in ("Y", "YES"):
            #driver.find_element_by_id("face").click()
            browser.find_by_id("face").first.click()
            starting_click = (random.randint(1, size[0] - 1), random.randint(1, size[1] - 1))
            print("starting_click: " + str(starting_click))
            left_click_cell(starting_click)
            print("starting bot while loop")
            game_over = False
            while not game_over:
                #print("sleeping to allow class updates")
                #time.sleep(1)
                grid = read_cells(size)
                if not check_cell_unclicked(grid, size):
                    print("Cycled through every cell without making a move")
                    game_over = True
                else:
                    game_over = is_game_over(grid)
        else:
            break
    print("Closing down")
    browser.close()


# Press the green button in the gutter to run the script.
"""
def rate_checker_selenium():
    url = small_url
    driver.get(url)
    cell_id = "1_1"
    for i in range(0, 10):
        print(driver.find_element_by_id(cell_id).get_attribute("class"))
        actionChains.context_click(driver.find_element_by_id(cell_id)).perform()
        time.sleep(1)

"""
def rate_checker_splinter():
    browser.visit(small_url)
    cell_id = "1_1"
    for i in range(0, 10):
        print(browser.find_by_id(cell_id).first['class'])
        browser.find_by_id(cell_id).right_click()
        time.sleep(1)


if __name__ == '__main__':
    open_minesweeper_webpage()
    #rate_checker_selenium()
    #rate_checker_splinter()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
