from optiboard.board import Breadboard, Pattern
from optiboard.beam import Beam, BeamPoint
from optiboard.utils.units import Units
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    board = Breadboard(
        width=10 * Units.inch, height=8 * Units.inch, pattern=Pattern.imperial_1in
    )

    # Create a beam example
    beam = Beam(board, wavelength=493.5 * Units.nm)

    # Start the beam at one corner
    beam_1_start = beam.begin(1 * Units.inch, 1 * Units.inch)

    beam.move_to(5 * Units.inch, 1 * Units.inch)
    beam.move_by(0, 1 * Units.inch)
    beam.turn_and_move(np.pi / 4, 1 * Units.inch)
    beam.turn_and_move(np.pi / 4, 1 * Units.inch)
    beam.turn_and_move(np.pi / 4, 1 * Units.inch)
    # Create another beam using turn_and_move
    beam2 = Beam(board, wavelength=650 * Units.nm)
    beam2.begin(BeamPoint(2 * Units.inch, 4 * Units.inch))
    beam2.turn_and_move(np.pi / 4, 2 * Units.inch)  # 45 degrees
    beam2.turn_and_move(0, 2 * Units.inch)  # horizontal
    beam2.turn_and_move(-np.pi / 4, 2 * Units.inch)  # -45 degrees

    fig, ax = plt.subplots()
    board.draw(fig, ax)
    beam.draw(fig, ax)
    beam2.draw(fig, ax)
    plt.show()
