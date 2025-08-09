from dataclasses import dataclass
import numpy as np
from typing import Optional
from optiboard.board import Breadboard
import matplotlib.pyplot as plt
from optiboard.utils.units import Units


class BeamPoint:
    def __init__(self, x: float, y: float, theta: float = 0.0):
        self.x = x
        self.y = y
        self.theta = theta
        self.nexts = []
        self.prevs = []

    def add_next(self, next: "BeamPoint"):
        self.nexts.append(next)

    def add_prev(self, prev: "BeamPoint"):
        self.prevs.append(prev)

    def normal_vector(self, prev_index: int = 0, next_index: int = 0):
        if len(self.nexts) == 0:
            raise Exception("BeamPoint has no nexts")
        if len(self.prevs) == 0:
            raise Exception("BeamPoint has no prevs")
        v_next = np.array(
            [self.nexts[next_index].x - self.x, self.nexts[next_index].y - self.y]
        )
        v_prev = np.array(
            [self.prevs[prev_index].x - self.x, self.prevs[prev_index].y - self.y]
        )
        normal_vector = v_next + v_prev
        normal_vector = normal_vector / np.linalg.norm(normal_vector)
        return normal_vector

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"BeamPoint({self.x}, {self.y})"


class Beam:
    def __init__(
        self,
        board: Breadboard,
        points: list[BeamPoint] = None,
        lw: Optional[float] = 1.5,
        style: Optional[str] = "-",
        wavelength: Optional[float] = 493.5 * Units.nm,
        w0: Optional[float] = 0.25,
        color: Optional[str] = None,
        opacity: Optional[float] = 0.8,
    ):
        self.board = board
        if points is None:
            points = []
        self.points = points
        self.lw = lw
        self.style = style
        self.wavelength = wavelength
        self.w0 = w0
        if color is None:
            self.color = self._wavelength_to_color(wavelength / Units.nm)
        else:
            self.color = color
        self.opacity = opacity

    def _wavelength_to_color(self, wavelength_nm: float) -> str:
        """Convert wavelength in nanometers to RGB color string."""
        # Visible light spectrum approximately 380-750 nm
        wl = wavelength_nm

        if wl < 380 or wl > 750:
            return "#808080"  # Gray for non-visible wavelengths

        # Define color transitions based on wavelength ranges
        if 380 <= wl < 440:
            # Violet to Blue
            red = -(wl - 440) / (440 - 380)
            green = 0.0
            blue = 1.0
        elif 440 <= wl < 490:
            # Blue to Cyan
            red = 0.0
            green = (wl - 440) / (490 - 440)
            blue = 1.0
        elif 490 <= wl < 510:
            # Cyan to Green
            red = 0.0
            green = 1.0
            blue = -(wl - 510) / (510 - 490)
        elif 510 <= wl < 580:
            # Green to Yellow
            red = (wl - 510) / (580 - 510)
            green = 1.0
            blue = 0.0
        elif 580 <= wl < 645:
            # Yellow to Red
            red = 1.0
            green = -(wl - 645) / (645 - 580)
            blue = 0.0
        else:  # 645 <= wl <= 750
            # Red
            red = 1.0
            green = 0.0
            blue = 0.0

        # Apply intensity factor near the edges of visible spectrum
        factor = 1.0
        if wl < 420:
            factor = 0.3 + 0.7 * (wl - 380) / (420 - 380)
        elif wl > 700:
            factor = 0.3 + 0.7 * (750 - wl) / (750 - 700)

        red *= factor
        green *= factor
        blue *= factor

        # Convert to hex color string
        r = int(red * 255)
        g = int(green * 255)
        b = int(blue * 255)

        return f"#{r:02x}{g:02x}{b:02x}"

    def get_color(self) -> str:
        """Get the color for this beam, either specified or based on wavelength."""
        if self.color is not None:
            return self.color
        else:
            return self._wavelength_to_color(self.wavelength / Units.nm)

    def draw(self, fig: plt.Figure, ax: plt.Axes):
        if len(self.points) < 2:
            return  # Need at least 2 points to draw a beam

        # Extract x and y coordinates from points
        x_coords = [point.x for point in self.points]
        y_coords = [point.y for point in self.points]

        # Draw the beam path
        ax.plot(
            x_coords,
            y_coords,
            linestyle=self.style,
            linewidth=self.lw,
            color=self.get_color(),
            alpha=self.opacity,
        )

    def begin(self, begin_x: float, begin_y: float):
        if len(self.points) != 0:
            raise ValueError("Beam must begin with a point")
        if (
            begin_x < 0
            or begin_x > self.board.width
            or begin_y < 0
            or begin_y > self.board.height
        ):
            raise ValueError("Beam point must be within board bounds")
        self.points.append(BeamPoint(begin_x, begin_y))
        return self.points[-1]

    def move_by(self, dx: float, dy: float):
        if len(self.points) == 0:
            raise ValueError("Beam must have at least one point")
        new_x = self.points[-1].x + dx
        new_y = self.points[-1].y + dy
        if (
            new_x < 0
            or new_x > self.board.width
            or new_y < 0
            or new_y > self.board.height
        ):
            raise ValueError("Beam point must be within board bounds")
        new_point = BeamPoint(new_x, new_y)

        # Link the points
        new_point.add_prev(self.points[-1])
        self.points[-1].add_next(new_point)

        self.points.append(new_point)
        return new_point

    def move_to(self, x: float, y: float):
        if len(self.points) == 0:
            raise ValueError("Beam must have at least one point")
        if x < 0 or x > self.board.width or y < 0 or y > self.board.height:
            raise ValueError("Beam point must be within board bounds")
        new_point = BeamPoint(x, y)

        # Link the points
        new_point.add_prev(self.points[-1])
        self.points[-1].add_next(new_point)

        self.points.append(new_point)
        return new_point

    def turn_and_move(self, theta: float, dr: float):
        if len(self.points) == 0:
            raise ValueError("Beam must have at least one point")
        new_x = self.points[-1].x + dr * np.cos(theta)
        new_y = self.points[-1].y + dr * np.sin(theta)
        if (
            new_x < 0
            or new_x > self.board.width
            or new_y < 0
            or new_y > self.board.height
        ):
            raise ValueError("Beam point must be within board bounds")
        new_point = BeamPoint(new_x, new_y, theta)

        # Link the points
        new_point.add_prev(self.points[-1])
        self.points[-1].add_next(new_point)

        self.points.append(new_point)
        return new_point

    def __str__(self):
        return f"Beam({self.points}, {self.lw}, {self.style})"

    def __repr__(self):
        return f"Beam({self.points}, {self.lw}, {self.style})"

    def __len__(self):
        return len(self.points)

    def __getitem__(self, index: int):
        return self.points[index]
