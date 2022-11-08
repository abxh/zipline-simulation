import pygame as pg
import zls.config as conf

from pathlib import Path
from zls.assets import Assets

from zls.scenes.introscene import introscene

class AssetManager():        
    @classmethod
    def load_assets(cls):
        Assets.font_sizes = conf.font_sizes_original
        
        for fp in conf.assets_path.rglob('*.*'):
            if fp.suffix in conf.image_types:
                cls.load_image(fp)
            elif fp.suffix in conf.font_types:
                cls.load_font(fp, conf.font_sizes_original)
                
        cls.load_colors(conf.color_hex_fp, conf.color_map_fp)
        cls.load_scenes()
    
    @classmethod
    def load_image(cls, fp: Path):
        Assets.image_dict[fp.stem] = pg.image.load(fp).convert_alpha()
    
    @classmethod
    def load_font(cls, fp: Path, font_sizes: tuple[int]):
        for size in font_sizes:
            Assets.font_dict[f'{fp.stem} {str(size)}'] = pg.font.Font(fp, size)
    
    @classmethod
    def reload_asset_fonts(cls, font_sizes: tuple[int]):
        Assets.font_dict.clear()
        Assets.font_sizes = font_sizes
        
        for font_type in conf.font_types:
            for fp in conf.assets_path.rglob(f'*{font_type}'):
                cls.load_font(fp, font_sizes)
    
    @classmethod
    def load_colors(cls, hex_fp: Path, map_fp: Path):
        with open(hex_fp) as hf, open(map_fp) as mf:
            mapping = [l.strip() for l in mf]
            
            for i, l in enumerate(hf):
                hex_val = l.strip()
                rgb_val = tuple(int(hex_val[j:j+2], 16) for j in (0, 2, 4))
                
                Assets.color_dict[mapping[i]] = pg.color.Color(*rgb_val)

    @classmethod
    def load_scenes(cls):
        Assets.scene_dict[introscene.name] = introscene
    