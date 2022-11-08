import sys
import pygame as pg
import zls.config as conf

from zls.assetmanager import AssetManager
from zls.assets       import Assets

class Window():
    @classmethod
    def start(cls):
        # Initialize pygame
        pg.init()
        
        # Set title, icon path, size and flags.
        pg.display.set_caption(conf.window_title)
        pg.display.set_icon(pg.image.load(conf.window_icon_path))
        pg.display.set_mode(conf.window_size, conf.window_flags)
        
        AssetManager.load_assets()
        
        # Set clock, screen surface and scale (which is changed in get_processed_events).
        cls.clock          = pg.time.Clock()
        cls.screen_surface = pg.display.get_surface()
        cls.scale_y        = 1.0
        
        # Get and start current scene.
        cls.current_scene = Assets.scene_dict[conf.initial_scene_name]
        cls.current_scene.start()
        
        cls.update_loop()
    
    @classmethod
    def update_loop(cls):
        while True:
            cls.update()
    
    @classmethod
    def get_processed_events(cls):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            elif event.type == pg.VIDEORESIZE:
                # Artificial scaling by scaling the font sizes with window height.
                
                # Note that this is a alternative to the more blurry method of using pg.RESIZABLE flag,
                # and that by using this, the code must be written in terms of the scale_y.
                
                # Set scale
                cls.scale_y = event.dict['size'][1] / conf.window_size[1]
                
                # Resize fonts with the scale:
                new_sizes = tuple(int(size * cls.scale_y) for size in conf.font_sizes_original)
                
                AssetManager.reload_asset_fonts(new_sizes)
        return events
    
    @classmethod       
    def update(cls):
        # Get and set events and delta time.
        cls.events = cls.get_processed_events()
        cls.dt     = cls.clock.get_time()
        
        # Pass delta time, events, screen surface and scale to current scene.
        cls.current_scene.update(cls.dt, cls.events)
        cls.current_scene.draw(cls.screen_surface, cls.scale_y)
        
        # Show the newly drawn screen surface.
        pg.display.flip()
        
        # Set current scene to new scene.
        cls.current_scene = Assets.scene_dict[cls.current_scene.next_scene_name]
               
        # Tick the clock and control fps by sleeping timely.
        cls.clock.tick(conf.window_fps)   
    