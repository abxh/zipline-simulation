from core.assets import colors
from core.objects import AnimateButton, Layer
from core.types import State


class VisualState(State):
    def __init__(self):
        name = "visual"
        super().__init__(name)

    def start(self):
        global_border_args = {
            "line_color": colors.black.correct_gamma(1.1),
            "line_thickness": 2,
            "border_height": 30,
            "border_color": colors.black,
            "text_size": 20,
            "text_x_offset": 5,
            "text_color": colors.white,
        }
        layer1 = Layer(
            "visual",
            (0, 0),
            (0.66, 0.66),
            "Visualization",
            colors.light_gray,
            **global_border_args
        )
        layer2 = Layer(
            "graph", (0, 0.66), (0.66, 1), "Graphs", colors.gray, **global_border_args
        )
        layer3 = Layer(
            "param",
            (0.66, 0),
            (1, 1),
            "Parameters",
            colors.dark_gray,
            **global_border_args
        )
        self.set_objects((layer1, layer2, layer3))
        super().start()
