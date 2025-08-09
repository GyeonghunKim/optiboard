from dataclasses import dataclass
from .base_component import Component, rect_shape


@dataclass
class KinematicMount(Component):
    """Rough rectangular footprint of a kinematic mirror mount."""

    w: float = 50.0
    h: float = 30.0

    def shape(self):
        return rect_shape(self.w, self.h, self.x, self.y, self.theta_deg)
