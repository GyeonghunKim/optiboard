from dataclasses import dataclass
import numpy as np
from typing import Optional
from optiboard.board import Breadboard


class BeamPoint:
    def __init__(self, x: float, y: float, theta: float = 0.0):
        self.x = x
        self.y = y

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
        style: Optional[str] = "--",
        wavelength_nm: Optional[float] = 493.0,
        w0_mm: Optional[float] = 0.25,
    ):
        self.board = board
        if points is None:
            points = []
        self.points = points
        self.lw = lw
        self.style = style
        self.wavelength_nm = wavelength_nm
        self.w0_mm = w0_mm

    def draw(self):
        for point in self.points:
            self.board.draw_point(point.x, point.y, self.lw, self.style)

    def begin(self, point: BeamPoint):
        if len(self.points) != 0:
            raise ValueError("Beam must begin with a point")
        if (
            point.x < 0
            or point.x > self.board.width_mm
            or point.y < 0
            or point.y > self.board.height_mm
        ):
            raise ValueError("Beam point must be within board bounds")
        self.points.append(point)

    def move_by(self, dx: float, dy: float):
        if len(self.points) == 0:
            raise ValueError("Beam must have at least one point")
        if (
            self.points[-1].x + dx < 0
            or self.points[-1].x + dx > self.board.width_mm
            or self.points[-1].y + dy < 0
            or self.points[-1].y + dy > self.board.height_mm
        ):
            raise ValueError("Beam point must be within board bounds")
        self.points.append(BeamPoint(self.points[-1].x + dx, self.points[-1].y + dy))

    def move_to(self, x: float, y: float):
        if len(self.points) == 0:
            raise ValueError("Beam must have at least one point")
        if x < 0 or x > self.board.width_mm or y < 0 or y > self.board.height_mm:
            raise ValueError("Beam point must be within board bounds")
        self.points.append(BeamPoint(x, y))

    def turn_and_move(self, theta: float, dr: float):
        if len(self.points) == 0:
            raise ValueError("Beam must have at least one point")
        if (
            self.points[-1].x + dr * np.cos(theta) < 0
            or self.points[-1].x + dr * np.cos(theta) > self.board.width_mm
            or self.points[-1].y + dr * np.sin(theta) < 0
            or self.points[-1].y + dr * np.sin(theta) > self.board.height_mm
        ):
            raise ValueError("Beam point must be within board bounds")
        self.points.append(
            BeamPoint(
                self.points[-1].x + dr * np.cos(theta),
                self.points[-1].y + dr * np.sin(theta),
            )
        )

    def __str__(self):
        return f"Beam({self.points}, {self.lw}, {self.style})"

    def __repr__(self):
        return f"Beam({self.points}, {self.lw}, {self.style})"

    def __len__(self):
        return len(self.points)

    def __getitem__(self, index: int):
        return self.points[index]
