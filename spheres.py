import scene
from euclid import *
from scene import LightSet, Sphere

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = self.make_example_light()

        self.objects = [
            Sphere(lights, Vector3(0, 0, 8.), 1)]

        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            self.objects.append(
                Sphere(lights, Vector3(y, x, 7.7), 0.3))
        self.objects.reverse()
