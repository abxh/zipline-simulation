from zls.data.scenes.introscene import introscene
from zls.data.types.scene import Scene

def get_scene_dict() -> dict[str, Scene]:
    d = {}
    d[introscene.name] = introscene
    
    return d