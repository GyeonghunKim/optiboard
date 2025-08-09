from optiboard.components.base_component import BaseComponent


class KinematicMount(BaseComponent):
    """Rough rectangular footprint of a kinematic mirror mount."""
    @classmethod
    def from_pin_point()
    def __init__(
        self,
        x_pin: float,
        y_pin: float,
        x_beam: float,
        y_beam: float,
        theta: float = 0.0,
        color: str = "k",
    ):
        super().__init__(x_pin, y_pin, x_beam, y_beam, theta, color)

    def draw(self, fig: plt.Figure, ax: plt.Axes):
        raise NotImplementedError("Subclasses must implement .draw()")
