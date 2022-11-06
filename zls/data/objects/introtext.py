import pygame as pg

from math import sin, pi

import zls.data.config as conf

from zls.data.types.object import Object, Event, Surface
from zls.data.assets import Assets as a


class IntroText(Object):
    def start(self):
        self.time_elapsed = 0
        self.font_name = 'CMU Serif Roman'
        self.font_color = a.color_dict['black']
        self.antialias_enabled = True

    def update(self, dt: int, events: list[Event]):
        self.time_elapsed += dt

    def draw(self, surface: Surface):
        if self.time_elapsed <= 1000:
            alpha_val = 255 * self.time_elapsed / 1000
            self.draw_title(surface, alpha_val)
        elif self.time_elapsed <= 2000:
            alpha_val = 255 * (self.time_elapsed - 1000) / 1000
            self.draw_title(surface, 255)
            self.draw_author(surface, alpha_val)
        elif self.time_elapsed <= 3000:
            self.draw_title(surface, 255)
            self.draw_author(surface, 255)
        elif self.time_elapsed <= 4000:
            alpha_val = 255 * (1 - (self.time_elapsed - 3000) / 1000)
            self.draw_title(surface, alpha_val)
            self.draw_author(surface, alpha_val)
        elif self.time_elapsed <= 5000:
            alpha_val = 255 * (self.time_elapsed - 4000) / 1000
            self.draw_license(surface, alpha_val)
            self.draw_repo(surface, alpha_val)
        elif self.time_elapsed <= 6000:
            self.draw_license(surface, 255)
            self.draw_repo(surface, 255)
        elif self.time_elapsed <= 7000:
            alpha_val = 255 * (1 - (self.time_elapsed - 6000) / 1000)
            self.draw_license(surface, alpha_val)
            self.draw_repo(surface, alpha_val)

    def draw_title(self, screen, alpha_val):
        self.draw_text_center(
            surface=screen,
            text='Zipline Simulation',
            size=conf.font_sizes[-1],
            center_offset=50,
            alpha_val=alpha_val)

    def draw_author(self, screen, alpha_val):
        self.draw_text_center(
            surface=screen,
            text='By Shamim Siddique',
            size=conf.font_sizes[-2],
            center_offset=-20,
            alpha_val=alpha_val)

    def draw_license(self, screen, alpha_val):
        self.draw_text_center(
            surface=screen,
            text='Copyrighted under the GPLv3 license.',
            size=conf.font_sizes[-2],
            center_offset=40,
            alpha_val=alpha_val)

    def draw_repo(self, screen, alpha_val):
        self.draw_text_center(
            surface=screen,
            text='(https://github.com/abxh/zipline-simulator)',
            size=conf.font_sizes[-3],
            center_offset=-10,
            alpha_val=alpha_val)

    def draw_text_center(self, surface, text, size, center_offset, alpha_val):
        font_color = self.font_color

        fs = a.font_dict[f'{self.font_name} {size}'].render(
            text, self.antialias_enabled, font_color)

        pos = fs.get_rect(center=surface.get_rect().center)
        pos = (pos[0], pos[1] - center_offset)

        fs.set_alpha(alpha_val)

        surface.blit(fs, pos)
    
