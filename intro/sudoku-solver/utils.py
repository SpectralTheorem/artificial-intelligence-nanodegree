
import collections


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]


def extract_units(unitlist, boxes):
    """Initializes a mapping from box names to the units

    Args:
        unitlist: a list containing "units" of boxes
        boxes: a list of strings identifying each box on a sudoku board

    Returns:
        A dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    """
    units = collections.defaultdict(list)
    for current_box in boxes:
        for unit in unitlist:
            if current_box in unit:
                units[current_box].append(unit)
    return units


def extract_peers(units, boxes):
    """Initializes a mapping from box names to a list of peer boxes

    Args:
        units: a dictionary with a key for each box (string) whose value is a
        list containing the units that the box belongs to
        (i.e., the "member units")
        boxes: a list of strings identifying each box on a sudoku board

    Returns:
        A dictionary with a key for each box (string) whose value is a set
        containing all boxes that are peers of the key box (boxes that are in
        a unit together with the key box)
    """
    peers = collections.defaultdict(set)  # set avoids duplicates
    for key_box in boxes:
        for unit in units[key_box]:
            for peer_box in unit:
                if peer_box != key_box:
                    peers[key_box].add(peer_box)
    return peers


def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]


def values2grid(values):
    """Converts the dictionary board representation to as string

    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        A string representing a sudoku grid.
    """
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)


def grid2values(grid, convert_empty=True):
    """Converts grid into a dict of {square: char} with '123456789' for empties

    Args:
        grid: a string representing a sudoku grid.
        convert_empty: a boolean whether to convert empty to '123456789'

    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if convert_empty and val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


def display(values):
    """Displays the values as a 2-D grid.

    Args:
        values: the sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()
