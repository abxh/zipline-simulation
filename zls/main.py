import sys
import pygame as pg

from pygame.time import Clock
from pygame.event import Event

import zls.data.config as conf
import zls.data.tools as t

from zls.data.assets import Assets as a


def main():
    pg.init()

    t.set_display_mode(
        title     = conf.window_title,
        icon_path = conf.window_icon_path,
        size      = conf.window_size,
        flags     = conf.window_flags)
    
    a.image_dict, a.font_dict, a.color_dict, a.scene_dict = (
        t.get_image_dict(conf.assets_path, conf.image_types),
        t.get_font_dict(conf.assets_path, conf.font_types, conf.font_sizes),
        t.get_color_dict(conf.hex_file_path, conf.map_file_path),
        t.get_scene_dict())

    clock  = Clock()
    screen = pg.display.get_surface()
    
    current_scene = a.scene_dict[conf.initial_scene]
    current_scene.start()
    
    while True:
        def get_processed_events() -> list[Event]:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            return events

        events = get_processed_events()
        dt = clock.get_time() # in ms

        current_scene.update(dt, events)
        current_scene.draw(screen)
        current_scene = a.scene_dict[current_scene.next_scene_name]
        
        pg.display.flip()
        
        # The following statement does two things:
        # (1) ticks the clock.
        # (2) acts as a sleep statement to control fps.
        clock.tick(conf.window_fps)

