from euclid import *

PLANE_DIST = 1
CENTER = Vector3(0.5, 0.5, 0)

class Scene(object):
    def __init__(self):
        self.objects = []
        self.camera = Vector3(0, 0, -3.)

    def make_example_light(self):
        lights = LightSet()
        lights.ambient = Vector3(0.01, 0.01, 0.01)
        lights.add_point(Vector3(10, 10, -3.), Vector3(1, 1, 1))
        lights.add_point(self.camera, Vector3(0., 0., 0.1))

        lights.add_diffuse(Vector3(0.5, -1, 1).normalized(),
                           Vector3(0.5, 0.1, 0.))
        return lights

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

    def make_light(self, x, normal):
        color = Vector3()
        for light_src, light_color in self.point:
            light = max(-(x - light_src).normalized().dot(normal), 0)
            color += light_color * light

        for light_src, light_color in self.diffuse:
            light = max((light_src).dot(normal), 0)
            color += light_color * light

        color += self.ambient
        return color

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
            color = self.lightset.make_light(x, normal)
            return color, x
        else:
            return None, None

class Triangle(object):
    def __init__(self, lightset, p1, p2, p3, texture=None):
        self.lightset = lightset
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.n = (p1 - p2).cross(p1 - p3).normalized()
        self.texture = texture

    def draw(self, a, x, y):
        b = Vector3(x, y, 0)

        p1 = self.p1
        p2 = self.p2
        p3 = self.p3
        n = self.n

        h1 = (p1 - a).dot(n)
        h2 = n.dot(b - a)
        if h2 == 0:
            return None, None

        t = h1 / h2
        if t < 0:
            return None, None

        x = (b - a) * t + a

        r0 = (p1 - x).cross(p2 - x).dot(n)
        r1 = (p2 - x).cross(p3 - x).dot(n)
        r2 = (p3 - x).cross(p1 - x).dot(n)

        if r0 < 0 or r1 < 0 or r2 < 0:
            return None, None

        color = self.lightset.make_light(x, n)
        if self.texture:
            tex_x = texture_mapping(x - a, n)
            tex_color = self.texture(tex_x)
            color = texture_mul(tex_color, color)
        return color, x

def texture_mul(a, b):
    return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)

def texture_mapping(x, n):
    return Vector2(x.x, y.y) # TODO!!!
