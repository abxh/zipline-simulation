from core import assets
from core import simulation as s
from core.api import Renderer
from core.types import Object


class IntroText(Object):
    def __init__(self):
        name = "introtext"
        super().__init__(name)
        self.time_elapsed = 0.0

    def update(self, dt: float):
        self.time_elapsed += dt

        if self.time_elapsed > 6:
            s.Simulation().next_state_name = "visual"

    def draw(self, renderer: Renderer):
        renderer = Renderer()

        if self.time_elapsed <= 1:
            alpha_val = 255 * self.time_elapsed
            self.draw_title(renderer, alpha_val)

        elif self.time_elapsed <= 2:
            alpha_val = 255 * (self.time_elapsed - 1)
            self.draw_title(renderer, alpha_val=255)
            self.draw_author(renderer, alpha_val)

        elif self.time_elapsed <= 3:
            self.draw_title(renderer, alpha_val=255)
            self.draw_author(renderer, alpha_val=255)

        elif self.time_elapsed <= 4:
            alpha_val = 255 * (1 - (self.time_elapsed - 3))
            self.draw_title(renderer, alpha_val)
            self.draw_author(renderer, alpha_val)

        elif self.time_elapsed <= 5:
            alpha_val = 255 * (self.time_elapsed - 4)
            self.draw_license(renderer, alpha_val)
            self.draw_repo(renderer, alpha_val)

        elif self.time_elapsed <= 6:
            self.draw_license(renderer, alpha_val=255)
            self.draw_repo(renderer, alpha_val=255)

        elif self.time_elapsed <= 7:
            alpha_val = 255 * (1 - (self.time_elapsed - 6))
            self.draw_license(renderer, alpha_val)
            self.draw_repo(renderer, alpha_val)

    def draw_title(self, renderer: Renderer, alpha_val):
        text = "Zipline Simulation"
        size = 48
        offset = 10

        self.draw_text_general(renderer, alpha_val, text, size, offset)

    def draw_author(self, renderer: Renderer, alpha_val):
        text = "By Shamim Siddique"
        size = 30
        offset = -10

        self.draw_text_general(renderer, alpha_val, text, size, offset)

    def draw_license(self, renderer: Renderer, alpha_val):
        text = "Copyrighted under the GPLv3 license."
        size = 36
        offset = 10

        self.draw_text_general(renderer, alpha_val, text, size, offset)

    def draw_repo(self, renderer: Renderer, alpha_val):
        text = "(https://github.com/abxh/zipline-simulator)"
        size = 28
        offset = -10

        self.draw_text_general(renderer, alpha_val, text, size, offset)

    def draw_text_general(self, renderer: Renderer, alpha_val, text, size, offset):
        antialiased = True
        color = assets.colors.black

        font = assets.fonts.gui_regular.of_size(size).render(text, antialiased, color)

        if offset >= 0:
            pos = font.get_rect(midbottom=renderer.drect.center)
        elif offset <= 0:
            pos = font.get_rect(midtop=renderer.drect.center)

        pos = (pos.topleft[0], pos.topleft[1] - offset * renderer._h_scale)

        font.set_alpha(alpha_val)

        renderer.draw_surface(0, font, pos)
