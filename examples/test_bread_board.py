from optiboard.board import Breadboard, Pattern
from optiboard.utils import Units
import matplotlib.pyplot as plt


if __name__ == "__main__":
    board = Breadboard(
        width=10 * Units.inch, height=5 * Units.inch, pattern=Pattern.imperial_1in
    )
    fig, ax = plt.subplots()
    board.draw(fig, ax)
    plt.show()
