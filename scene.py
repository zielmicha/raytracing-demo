from euclid import *

PLANE_DIST = 1
CENTER = Vector3(0.5, 0.5, 0)

class Scene(object):
    def __init__(self):
        #lights.ambient = Vector3(0.03, 0.03, 0.03)
        self.camera = Vector3(0, 0, -3.)

        lights = LightSet()
        lights.ambient = Vector3(0.01, 0.01, 0.01)
        lights.add_point(Vector3(10, 10, -3.), Vector3(1, 1, 1))
        lights.add_point(self.camera, Vector3(0., 0., 0.1))

        lights.add_diffuse(Vector3(0.5, -1, 1).normalized(),
                           Vector3(0.5, 0.1, 0.))

        self.objects = [
            Sphere(lights, Vector3(0, 0, 8.), 1)]
        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            self.objects.append(
                Sphere(lights, Vector3(y, x, 7.7), 0.3))
        self.objects.reverse()

    def get_pixel(self, x, y):
        v = Vector3()
        dist = None
        for obj in self.objects:
            color, pos = obj.draw(self.camera, x, y)
            if color:
                mdist = abs(pos - self.camera)
                if not dist or mdist < dist:
                    dist = mdist
                    v = color

        v.x = min(max(v.x, 0), 1)
        v.y = min(max(v.y, 0), 1)
        v.z = min(max(v.z, 0), 1)

        return v

class LightSet(object):
    def __init__(self):
        self.point = []
        self.diffuse = []
        self.ambient = Vector3()

    def add_point(self, src, color=Vector3(1, 1, 1)):
        self.point.append((src, color))

    def add_diffuse(self, src, color=Vector3(1, 1, 1)):
        self.diffuse.append((src, color))

class Sphere(object):
    def __init__(self, lightset, center, r):
        self.c = center
        self.r = r
        self.lightset = lightset

    def draw(self, a, x, y):
        b = Vector3(x, y, 0)
        c = self.c
        r = self.r

        A = (b - a).magnitude_squared()
        B = (b - a).dot(a - c) * 2
        C = (a - c).magnitude_squared() - r ** 2

        delta = B ** 2 - 4 * A * C

        if delta >= 0:
            t = (-delta ** 0.5 - B) / (2 * A)
            x = (b - a) * t + a
            normal = (x - c).normalized()
            color = Vector3()
            for light_src, light_color in self.lightset.point:
                light = max(-(x - light_src).normalized().dot(normal), 0)
                color += light_color * light

            for light_src, light_color in self.lightset.diffuse:
                light = max((light_src).dot(normal), 0)
                color += light_color * light

            color += self.lightset.ambient
            return color, x
        else:
            return None, None
