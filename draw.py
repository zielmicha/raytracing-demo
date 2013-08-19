import struct
import sys
import os
import subprocess

def draw(get_pixel, name='test', w=640, h=480):
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((w,h))
    scale = float(max(w, h))
    for i in range(h):
        for j in range(w):
            x = (j-w/2)/scale
            y = -(i-h/2)/scale
            r, g, b = tuple(get_pixel(x, y))
            color = (int(r*255), int(g*255), int(b*255))
            screen.set_at((j, i), color)
        if i % 40 == 0:
            pygame.display.flip()
            print '%d%%' % (i/float(h)*100)

    pygame.display.flip()
    pygame.image.save(screen, name+'.png')
    print 'finished'
    while (pygame.event.wait().type != pygame.KEYDOWN):
        pass

def draw2(get_pixel, name='test', w=640, h=480):
    line = []
    scale = float(max(w, h))
    proc = subprocess.Popen('python filter.py',
                            shell=True,
                            stdin=subprocess.PIPE)
    f_out = proc.stdin
    for i in range(h):
        line = []
        for j in range(w):
            x = (j-w/2)/scale
            y = -(i-h/2)/scale
            r, g, b = tuple(get_pixel(x, y))
            line.append(struct.pack('BBB', int(r*255), int(g*255), int(b*255)))
        f_out.write(''.join(line))
    f_out.flush()
    print 'finished'
    proc.wait()

try:
    import __pypy__
except ImportError:
    pass
else:
    draw = draw2
