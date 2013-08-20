import scene
from euclid import *
from scene import LightSet, Triangle, Sphere

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = self.make_example_light()
        lights.add_diffuse(Vector3(0, 1, 0),
                           Vector3(0, 0, 1))

        d = 30
        self.objects += self.make_fancy_tetrahedron(
            lights,
            Vector3(-2, -3, d),
            Vector3(2, -3, d),
            Vector3(0, -3, d - 3),
            Vector3(0, 2, d - 1.5),
        )

        self.objects += [
            Sphere(lights, Vector3(0.5, 0, 29), 0.3)
        ]
        self.objects.reverse()

    def make_fancy_tetrahedron(self, light, a, b, c, d):
        return self.make_tetrahedron(light, a, b, c, d) \
            + [ Sphere(light, p, 0.3) for p in [a, b, c, d] ]

    def make_tetrahedron(self, light, a, b, c, d):
        return [
            Triangle(light, a, b, c),
            Triangle(light, a, b, d),
            Triangle(light, a, c, d),
            Triangle(light, b, c, d),
            ]
