from scene import *
from draw import draw

def main():
    scene = Scene()

    # ... set up the scene ...

    draw(scene.get_pixel, 'test', 640, 480)

if __name__ == '__main__':
    main()
