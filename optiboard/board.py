from dataclasses import dataclass
import numpy as np
from .utils.units import Units
from enum import Enum
import matplotlib.pyplot as plt


class Pattern(Enum):
    imperial_1in = "imperial_1in"
    metric_25mm = "metric_25mm"


class Breadboard:
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
