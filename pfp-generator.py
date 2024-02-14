import pygame
from random import randint, choice

WIDTH = HEIGHT = 256 # you can change this, doesn't have to be a perfect square'
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def is_prime(n):
    for i in range(2,n):
        if n % i == 0:
            return False
    return True

def point_distance(point1, point2):
    x1, y1, *_ = point1
    x2, y2, *_ = point2
    return ((x2-x1)**2 + (y2-y1)**2) ** .5

def closest_point(point: tuple, points: list):
    points = points.copy()
    if len(points) == 1:
        return points[0]
    if point in points:
        points.remove(point)
    minimum = points[0]
    for pt in points:
        if point_distance(point, pt) < point_distance(point, minimum):
            minimum = pt
    return pt

def closest_points(point: tuple, points: list, dist: int) -> list:
    points = points.copy()
    if point in points:
        points.remove(point)
    closest = []
    for pt in points:
        if point_distance(point, pt) <= dist:
            closest.append(pt)
    return closest


# here starts the good stuff
def wb_gradient():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if x % 2:
                t = (choice((x, y)) % 256)
            else:
                t = randint(0, 255)
            screen.set_at((x, y), (t, t, t))

def gradient():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if x % 2:
                r, g, b = (choice((x, y)) % 256), (choice((x, y)) % 256), (choice((x, y)) % 256)
            else:
                r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
            screen.set_at((x, y), (r, g, b))

def wb_starrysky():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            t = (choice((x, y)) / randint(1, 255)) % 256
            screen.set_at((x, y), (t, t, t))

def starrysky(R = True, G = True, B = True):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            r, g, b = (choice((x, y)) / randint(1, 255)) % 256 if R else 0, (choice((x, y)) / randint(1, 255)) % 256 if G else 0, (choice((x, y)) / randint(1, 255)) % 256 if B else 0
            screen.set_at((x, y), (r, g, b))

def less_starrysky(amount=50):
    for i in range(amount):
        x, y, = randint(0, WIDTH), randint(0, HEIGHT)
        size = randint(1, 5)
        pygame.draw.rect(screen, (((size/5)*255),)*3, pygame.Rect(x, y, size, size))

def wb_prime(inverted = False):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if is_prime(x) or is_prime(y):
                t = randint(0, 255) if not inverted else 255
            else:
                t = 255 if not inverted else randint(0, 255)
            screen.set_at((x, y), (t, t, t)) 

def prime(inverted = False):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if is_prime(x) or is_prime(y):
                r, g, b = (randint(0, 255), randint(0, 255), randint(0, 255)) if not inverted else (255, 255, 255)
            else:
                r, g, b = (255, 255, 255) if not inverted else (randint(0, 255), randint(0, 255), randint(0, 255))
            screen.set_at((x, y), (r, g, b))

def rays(density=50):
    points = []
    for i in range(density):
        points.append((randint(0, WIDTH), randint(0, HEIGHT)))

    while points:
        for point in points.copy():
            screen.set_at(point, "black")
            closest = closest_point(point, points)
            pygame.draw.aaline(screen, (randint(0, 255), randint(0, 255), randint(0, 255)), point, closest)
            points.remove(point)

def skribl(density=50):
    points = []
    for i in range(density):
        points.append((randint(0, WIDTH), randint(0, HEIGHT)))

    for ind in range(1, len(points)):
        p1, p2 = points[ind-1], points[ind]
        screen.set_at(p1, "black")
        screen.set_at(p2, "black")
        pygame.draw.aaline(screen, (randint(0, 255), randint(0, 255), randint(0, 255)), p1, p2)

def paper_shapes(density=50):
    points = []
    for i in range(density):
        points.append((randint(0, WIDTH), randint(0, HEIGHT)))

    radius = 5
    point = choice(points)
    while points:
        closest = closest_points(point, points, radius)
        for pt in closest:
            pygame.draw.aaline(screen, (randint(0, 255), randint(0, 255), randint(0, 255)), point, pt)
        point = closest_point(point, points)
        radius += 5
        points.remove(point)

def paths(density=100):
    points = []
    for i in range(density):
        points.append((randint(0, WIDTH), randint(0, HEIGHT)))

    radius = 25
    point = choice(points)
    while points:
        closest = closest_points(point, points, radius)
        for pt in closest:
            pygame.draw.aaline(screen, "gray", point, pt)
        point = closest_point(point, points)
        points.remove(point)

def labyrinth(pointsPerLine=50, background_color="black", lines_color="white"):
    screen.fill(background_color)
    stepx = stepy = int(WIDTH / pointsPerLine)
    points = []
    for x in range(0, WIDTH, stepx):
        for y in range(0, HEIGHT, stepy):
            points.append((x, y))

    point1 = choice(points)
    while True:
        closest = closest_points(point1, points, stepx+1)
        while not closest:
            points.remove(point1)
            if points:
                point1 = choice(points)
                closest = closest_points(point1, points, stepx+1)
            else:
                return
        point2 = choice(closest)
        closest.remove(point2)
        pygame.draw.aaline(screen, lines_color, point1, point2)
        for point in closest:
            points.remove(point)
        points.remove(point1)
        point1 = point2

#labyrinth(50, "white", "red")
#pygame.image.save(screen, "pfp.png") # you can use this to save it, or take a screenshot I guess
