import scene
from euclid import *
from scene import LightSet, Sphere

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = LightSet()
        lights.add_diffuse(Vector3(1, 0, 0),
                           Vector3(0.5, 0., 0.1))
        lights.ambient = Vector3(0.5, 0.5, 0.5)
        self.objects += [
            Sphere(lights, Vector3(-1, 0, 8.), 0.7),
            Sphere(lights, Vector3(0.7, 0, 8.), 0.5)]

        lights.shadow_objects = self.objects
