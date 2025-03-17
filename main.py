import pygame
import math



pygame.init()

clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1600, 1000), pygame.RESIZABLE)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
G = 0.000000000066743





class Object():
    def __init__(self, x, y, x_vel, y_vel, x_acc, y_acc, colour, mass):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.colour = colour
        self.mass = mass
        
    def draw_object(self):
        pygame.draw.circle(SCREEN, self.colour, (self.x, self.y), 10)
        
a_object = Object(700, 500, 5, 0, 0, 0, RED, 500000000000000)
b_object = Object(200, 200, 10, 0, 0, 0, GREEN, 50)





def get_distance():
    distance = math.sqrt((a_object.x - b_object.x) ** 2 + (a_object.y - b_object.y) ** 2)
    
    return distance


def get_angle():
    if b_object.x - a_object.x == 0:
        a_angle = 0
    else:
        a_angle = math.atan((b_object.y - a_object.y) / (b_object.x - a_object.x))
        if a_angle < 0:
            a_angle *= -1
            
    return a_angle


def get_force():
    force = G * ((a_object.mass * b_object.mass) / (get_distance() ** 2))
    
    return force

def get_directions():
    vertical, crash = False, False
    if a_object.x < b_object.x:
        if a_object.y < b_object.y:
            directions = [1, 1, -1, -1]
        elif a_object.y == b_object.y:
            directions = [1, -1]
        else:
            directions = [1, -1, -1, 1]
    elif a_object.x == b_object.x:
        vertical = True
        if a_object.y < b_object.y:
            directions = [1, -1]
        elif a_object.y == b_object.y:
            crash = True
        else:
            directions = [-1, 1]
    else:
        if a_object.y < b_object.y:
            directions = [-1, 1, 1, -1]
        elif a_object.y == b_object.y:
            directions = [-1, 1]
        else:
            directions = [-1, -1, 1, 1]
            
    return (directions, vertical, crash)

def get_forces():
    angle = get_angle()
    force = get_force()
    x_force = math.cos(angle) * force
    y_force = math.sin(angle) * force
    
    return x_force, y_force

def get_accelerations():
    directions, vertical, crash = get_directions()
    force = get_force()
    x_force, y_force = get_forces()
    if crash:
        print('crash')
    elif len(directions) == 2:
        if vertical:
            a_x_acc = 0
            a_y_acc = force * directions[0] / a_object.mass
            b_x_acc = 0
            b_y_acc = force * directions[1] / b_object.mass
        else:
            a_x_acc = force * directions[0] / a_object.mass
            a_y_acc = 0
            b_x_acc = force * directions[1] / b_object.mass
            b_y_acc = 0
    else:
        a_x_acc = x_force * directions[0] / a_object.mass
        a_y_acc = y_force * directions[1] / a_object.mass
        b_x_acc = x_force * directions[2] / b_object.mass
        b_y_acc = y_force * directions[3] / b_object.mass
        
    return a_x_acc, a_y_acc, b_x_acc, b_y_acc

def main():
    a_x, a_y, b_x, b_y = get_accelerations()
    a_object.x_acc += a_x
    a_object.y_acc += a_y
    b_object.x_acc += b_x
    b_object.y_acc += b_y
    a_object.x_vel += a_object.x_acc
    a_object.y_vel += a_object.y_acc
    b_object.x_vel += b_object.x_acc
    b_object.y_vel += b_object.y_acc
    a_object.x += a_object.x_vel
    a_object.y += a_object.y_vel
    b_object.x += b_object.x_vel
    b_object.y += b_object.y_vel


def update_screen():
    
    SCREEN.fill(BLACK)
    a_object.draw_object()
    b_object.draw_object()
    pygame.display.flip()





running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    main()
    update_screen()
    clock.tick(30)


pygame.quit()