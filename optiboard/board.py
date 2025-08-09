from dataclasses import dataclass
import numpy as np
from .utils.units import Units
from enum import Enum
import matplotlib.pyplot as plt


class Pattern(Enum):
    """Enumeration of available hole patterns for breadboards.

    Attributes
    ----------
    imperial_1in : str
        Imperial pattern with 1-inch spacing between holes.
    metric_25mm : str
        Metric pattern with 25mm spacing between holes.

    Examples
    --------
    >>> pattern = Pattern.imperial_1in
    >>> pattern.value
    'imperial_1in'
    """

    imperial_1in = "imperial_1in"
    metric_25mm = "metric_25mm"


class Breadboard:
    """A breadboard for optical experiments with a regular pattern of mounting holes.

    Parameters
    ----------
    width : float
        Width of the breadboard in meters.
    height : float
        Height of the breadboard in meters.
    pattern : Pattern, optional
        The hole pattern type. Default is Pattern.imperial_1in.

    Attributes
    ----------
    width : float
        Width of the breadboard in meters.
    height : float
        Height of the breadboard in meters.
    pattern : Pattern
        The hole pattern type.
    hole_diam : float
        Diameter of mounting holes in meters.
    margin : float
        Margin from board edge to first holes in meters.

    Raises
    ------
    ValueError
        If an invalid pattern is specified.

    Examples
    --------
    >>> from optiboard.utils.units import Units
    >>> board = Breadboard(10*Units.inch, 8*Units.inch)
    >>> board.width == 10*Units.inch
    True
    >>> board.pattern == Pattern.imperial_1in
    True

    >>> # Create a metric breadboard
    >>> board_metric = Breadboard(0.3, 0.2, Pattern.metric_25mm)
    Traceback (most recent call last):
        ...
    ValueError: Invalid pattern: Pattern.metric_25mm
    """

    def __init__(
        self,
        width: float,
        height: float,
        pattern: Pattern = Pattern.imperial_1in,
    ):
        self.width = width
        self.height = height
        self.pattern = pattern
        if self.pattern == Pattern.imperial_1in:
            self.hole_diam = 0.25 * Units.inch
            self.margin = 0.5 * Units.inch
        else:
            raise ValueError(f"Invalid pattern: {self.pattern}")

    def draw(self, fig: plt.Figure, ax: plt.Axes):
        """Draw the breadboard on a matplotlib figure.

        Draws the breadboard boundary and hole pattern on the provided axes.
        The breadboard is drawn as a black rectangle with gray circular holes
        arranged in a grid pattern.

        Parameters
        ----------
        fig : plt.Figure
            The matplotlib figure to draw on.
        ax : plt.Axes
            The matplotlib axes to draw on.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from optiboard.utils.units import Units
        >>> board = Breadboard(4*Units.inch, 3*Units.inch)
        >>> fig, ax = plt.subplots()
        >>> board.draw(fig, ax)
        >>> ax.get_xlim()[1] == 4*Units.inch
        True
        >>> ax.get_ylim()[1] == 3*Units.inch
        True
        """
        # Draw the outer boundary of the breadboard
        rect = plt.Rectangle(
            (0, 0),
            self.width,
            self.height,
            linewidth=2,
            edgecolor="black",
            facecolor="black",
        )
        ax.add_patch(rect)

        # Draw the hole pattern
        if self.pattern == Pattern.imperial_1in:
            # Calculate hole positions for 1-inch grid pattern
            spacing = 1.0 * Units.inch

            # Start from margin and go to width/height minus margin
            x_positions = np.arange(
                self.margin, self.width - self.margin + spacing / 2, spacing
            )
            y_positions = np.arange(
                self.margin, self.height - self.margin + spacing / 2, spacing
            )

            # Draw holes at grid intersections
            for x in x_positions:
                for y in y_positions:
                    if x <= self.width - self.margin and y <= self.height - self.margin:
                        hole = plt.Circle(
                            (x, y),
                            self.hole_diam / 2,
                            facecolor="gray",
                            edgecolor="gray",
                            linewidth=0.5,
                        )
                        ax.add_patch(hole)

        # View only the board and hide all axes
        ax.set_aspect("equal")
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.axis("off")
