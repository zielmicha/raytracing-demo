import scene
from euclid import *
from scene import LightSet, Sphere, Triangle

class Scene(scene.Scene):
    def __init__(self):
        super(Scene, self).__init__()
        lights = LightSet()
        lights.ambient = Vector3(0.2, 0.2, 0.2)
        lights.add_point(self.camera,
                         Vector3(0, 0.9, 0))

        depth = 100

        verts = []
        for line in open('teapot_simple.obj'):
            if not line.strip(): continue
            if line.startswith('g '): continue
            m, x, y, z = line.split()
            if m == 'v':
                verts.append(Vector3(float(x), float(y),
                                     float(z) + depth))
            elif m == 'f':
                x, y, z = map(int, [x, y, z])
                self.objects.append(Triangle(lights,
                                             verts[x-1],
                                             verts[y-1],
                                             verts[z-1]))
