class BaseComponent:
    def __init__(
        self,
        name: str,
        x_pin: float,
        y_pin: float,
        x_beam: float,
        y_beam: float,
        theta: float = 0.0,
        color: str = "k",
    ):
        self.name = name
        self.x_pin = x_pin
        self.y_pin = y_pin
        self.x_beam = x_beam
        self.y_beam = y_beam
        self.theta = theta
        self.color = color

    def shape(self):
        raise NotImplementedError("Subclasses must implement .shape()")

    def bbox(self):
        return self.shape().bounds

    def collides(self, other: "Component") -> bool:
        return self.shape().buffer(0).intersects(other.shape().buffer(0))

    def parts_for_drawing(self):
        raise NotImplementedError("Subclasses must implement .parts_for_drawing()")
