import pygame as pg

import zls.config as conf

from zls.types.object import Object, Event, Surface
from zls.assets import Assets


class IntroText(Object):
    def start(self):
        self.time_elapsed = 0
        self.font_family = 'CMU Serif'
        self.font_color = Assets.color_dict['black']
        self.antialias_enabled = True
        self.orignal_center_offset = 10
        self.center_offset = self.orignal_center_offset

    def update(self, dt: int, events: list[Event]):
        self.time_elapsed += dt

    def draw(self, surface: Surface, scale_y: float):
        self.surface = surface
        self.scale_y = scale_y
        
        if self.time_elapsed <= 1000:
            alpha_val = 255 * self.time_elapsed / 1000
            self.draw_title(alpha_val)
            
        elif self.time_elapsed <= 2000:
            alpha_val = 255 * (self.time_elapsed - 1000) / 1000
            self.draw_title(255)
            self.draw_author(alpha_val)
            
        elif self.time_elapsed <= 3000:
            self.draw_title(255)
            self.draw_author(255)
            
        elif self.time_elapsed <= 4000:
            alpha_val = 255 * (1 - (self.time_elapsed - 3000) / 1000)
            self.draw_title(alpha_val)
            self.draw_author(alpha_val)
            
        elif self.time_elapsed <= 5000:
            alpha_val = 255 * (self.time_elapsed - 4000) / 1000
            self.draw_license(alpha_val)
            self.draw_repo(alpha_val)
            
        elif self.time_elapsed <= 6000:
            self.draw_license(255)
            self.draw_repo(255)
            
        elif self.time_elapsed <= 7000:
            alpha_val = 255 * (1 - (self.time_elapsed - 6000) / 1000)
            self.draw_license(alpha_val)
            self.draw_repo(alpha_val)
            
        else:
            self.time_elapsed = 0

    def draw_title(self, alpha_val):
        self.draw_text_center(
            text          = 'Zipline Simulation',
            size          = Assets.font_sizes[-1],
            center_offset = self.center_offset,
            font_type     = 'Roman',
            alpha_val     = alpha_val)

    def draw_author(self, alpha_val):
        self.draw_text_center(
            text          = 'By Shamim Siddique',
            size          = Assets.font_sizes[-2],
            center_offset = -self.center_offset,
            font_type     = 'Roman',
            alpha_val     = alpha_val)

    def draw_license(self, alpha_val):
        self.draw_text_center(
            text          = 'Copyrighted under the GPLv3 license.',
            size          = Assets.font_sizes[-2],
            center_offset = self.center_offset,
            font_type     = 'Roman',
            alpha_val     = alpha_val)

    def draw_repo(self, alpha_val):
        self.draw_text_center(
            text          = '(https://github.com/abxh/zipline-simulator)',
            size          = Assets.font_sizes[-3],
            center_offset = -self.center_offset,
            font_type     = 'Roman',
            alpha_val     = alpha_val)

    def draw_text_center(self, text, size, center_offset, font_type, alpha_val):
        font_color = self.font_color

        fs = Assets.font_dict[f'{self.font_family} {font_type} {size}'].render(
            text, self.antialias_enabled, font_color)
        
        if center_offset >= 0:
            pos = fs.get_rect(midbottom=self.surface.get_rect().center)
        else:
            pos = fs.get_rect(midtop=self.surface.get_rect().center)
        
        # Offset position
        pos = (pos[0], pos[1] - center_offset)
        
        # Set alpha value
        fs.set_alpha(alpha_val)
        
        # Blit to screen:
        self.surface.blit(fs, pos)
    