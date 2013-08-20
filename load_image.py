import pygame, sys, json

img = pygame.image.load(sys.argv[1])

print json.dumps({"data": pygame.image.tostring(img, 'RGB').encode('base64'), "size": img.get_size()})
