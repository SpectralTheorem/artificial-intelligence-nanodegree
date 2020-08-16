import copy
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units


diagonal_units = []
diagonal_units.append([rows[i]+cols[i] for i in range(9)])
diagonal_units.append([rows[i]+cols[8-i] for i in range(9)])
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminates values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all
    other boxes in the same unit.

    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with the naked twins eliminated from peers
    """
    for label in values:
        for peer in peers[label]:
            value = values[label]
            if value == values[peer] and len(value) == 2:
                for other in set(peers[label]) & set(peers[peer]):
                    for digit in value:
                        values[other] = values[other].replace(digit, '')

    return values


def eliminate(values):
    """Applies the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with the assigned values eliminated from peers
    """
    for label, value in values.items():
        if len(value) == 1:  # If the value is determined.
            for peer in peers[label]:
                values[peer] = values[peer].replace(value, '')

    return values


def only_choice(values):
    """Applies the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a
    certain digit, then that box must be assigned that digit.

    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in '123456789':
            count = 0
            box = ''
            for label in unit:
                if digit in values[label]:
                    count += 1
                    box = label
            if count == 1:
                values[box] = digit

    return values


def reduce_puzzle(values):
    """Reduces a Sudoku puzzle by repeatedly applying all constraint strategies

    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary after continued application of the constraint
        strategies no longer produces any changes, or False if the puzzle is
        unsolvable
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Named Twins Strategu
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Applies depth first search to solve Sudoku puzzles

    Args:
        values: a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with all boxes assigned or False
    """
    values = reduce_puzzle(values)
    if values is False:  # Unsolvable
        return False
    if all(len(value) == 1 for value in values.values()):  # Solved
        return values

    length = 9
    box = ''
    for label, value in values.items():
        if 1 < len(value) < length:
            length = len(value)
            box = label
    value = values[box]

    for digit in value:
        values_copy = copy.deepcopy(values)
        values_copy[box] = digit
        results = search(values_copy)
        if results is not False:  # Solved
            return results

    return False


def solve(grid):
    """Finds the solution using search and constraint propagation

    Args:
        grid: a string representing a sudoku grid.

    Returns:
        The dictionary representation of the final sudoku grid or False if no
        solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = (
        '2........'
        '.....62..'
        '..1....7.'
        '..6..8...'
        '3...9...7'
        '...6..4..'
        '.4....8..'
        '..52.....'
        '........3')
    display(grid2values(diag_sudoku_grid, False))
    result = solve(diag_sudoku_grid)
    display(result)
