from src.engine.scene.camera import Camera
from src.engine.scene.scene import Scene


def create_scene_and_camera(initial_camera_pos: tuple[int, int] = (0, 0)) -> tuple[Scene, Camera]:
    space = Scene()
    return space, Camera(space, initial_camera_pos)
