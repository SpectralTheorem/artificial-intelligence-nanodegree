import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def display_board(locations, shape):
    """Draw a chessboard with queens placed at each position specified
    by the assignment.
    Parameters
    ----------
    locations : list
        The locations list should contain one element for each queen
        of the chessboard containing a tuple (r, c) indicating the
        row and column coordinates of a queen to draw on the board.
    shape : integer
        The number of cells in each dimension of the board (e.g.,
        shape=3 indicates a 3x3 board)
    Returns
    -------
    matplotlib.figure.Figure
        The handle to the figure containing the board and queens
    """
    r = c = shape
    cmap = mpl.colors.ListedColormap(['#f5ecce', '#614532'])
    img = mpl.image.imread('queen.png').astype(np.float)
    boxprops = {"facecolor": "none", "edgecolor": "none"}

    x, y = np.meshgrid(range(c), range(r))
    plt.matshow(x % 2 ^ y % 2, cmap=cmap)
    plt.axis("off")  # eliminate borders from plot

    fig = plt.gcf()
    fig.set_size_inches([r, c])
    scale = 0.75 * fig.get_dpi() / max(img.shape)
    ax = plt.gca()
    for y, x in set(locations):
        box = mpl.offsetbox.OffsetImage(img, zoom=scale)
        ab = mpl.offsetbox.AnnotationBbox(box, (y, x), bboxprops=boxprops)
        ax.add_artist(ab)

    plt.show()
    return fig
