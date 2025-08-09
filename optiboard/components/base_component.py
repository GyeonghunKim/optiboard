class BaseComponent:
    def __init__(
        self,
        name: str,
        x_pin: float,
        y_pin: float,
        x_beam: float,
        y_beam: float,
        theta: float = 0.0,
    ):
        # for component level, normal vector is towards upwards
        self.normal_vector = np.array([0, 1])
        self.name = name
        self.x_pin = x_pin
        self.y_pin = y_pin
        self.x_beam = x_beam
        self.y_beam = y_beam
        self.theta = theta

    def shape(self):
        raise NotImplementedError("Subclasses must implement .shape()")
