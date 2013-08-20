import scene
from euclid import *
from scene import LightSet, Sphere, Triangle

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = LightSet()
        lights.add_diffuse(Vector3(1, 0, 0),
                           Vector3(0.5, 0., 0.1))
        lights.add_diffuse(Vector3(0, 0, 1),
                           Vector3(0, 0.6, 0))
        lights.ambient = Vector3(0, 0, 0.1)
        h = -2
        floor = Triangle(lights,
                         Vector3(-50, h, -50),
                         Vector3(50, h, -50),
                         Vector3(0, h, 50),
                         texture=lambda x: Vector3(1, 0, 0))
        self.objects += [
            Sphere(lights, Vector3(-1, 0, 8.), 0.7),
            Sphere(lights, Vector3(0.7, 0, 8.), 0.5),
            ]

        lights.shadow_objects = self.objects
