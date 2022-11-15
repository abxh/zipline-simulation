import sys
import pygame as pg

from submodules import conf
from submodules.assets import Assets

class Window():        
    def start(self):
        # initialize pygame modules
        pg.init()
        
        # set window parameters
        pg.display.set_caption(conf.WIN_TITLE)
        pg.display.set_icon(pg.image.load(conf.WIN_ICON_FP))
        pg.display.set_mode(conf.WIN_SIZE, conf.WIN_FLAGS)
        
        # load assets
        Assets.load_paths(
            assets_path              = conf.ASSETS_PATH,
            image_file_types         = conf.IMAGE_FILE_TYPES,
            font_file_types          = conf.FONT_FILE_TYPES,
            color_palette_file_types = conf.COLOR_PALETTE_FILE_TYPES)
        Assets.load_images()
        Assets.load_fonts(conf.FONT_SIZES)
        Assets.load_color_palette(conf.COLOR_PALETTE_NAME)
        
        self.run()
    
    def run(self):
        self.running = True
        self.surface = pg.display.get_surface()
        
        while self.running:
            events = pg.event.get()
            
            # do some event handling
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.VIDEORESIZE:
                    scale_y = event.size[1] / conf.WIN_SIZE[1]
                    
                    new_sizes = (conf.FONT_SIZES * scale_y).astype(int)
                    Assets.load_fonts(new_sizes)
                
                
            self.surface.fill(Assets.colors['white'])
            font_surface = Assets.fonts[f'CMU Serif Roman {Assets.font_sizes_scaled[2]}'].render(
                'Hello World', True, (0,0,0))
            
            self.surface.blit(font_surface, font_surface.get_rect(
                center = self.surface.get_rect().center))    
            
            # Flip to the newly drawn screen (as pygame uses double buffering)
            pg.display.flip()
        
        self.end()
            
    def end(self):
        # uninitialize pygame modules
        pg.quit()
        
        # exit program properly
        sys.exit() 