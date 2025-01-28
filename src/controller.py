import pygame

def square_distance(P, Q):
    return (P[0]-Q[0])**2 + (P[1]-Q[1])**2

class Controller():
    def __init__(self, radius, color):
        self.point_list = []
        self.radius = radius
        self.color = color

    def handle_mouse_event(self, button, position):
        if button == 1:
            self.point_list.append(position)
        if button == 3:
            for point in self.point_list:
                if square_distance(point, position) < self.radius**2:
                    self.point_list.remove(point)
                    break
        print(self.point_list)

    def draw_points(self, screen):
        for point in self.point_list:
            pygame.draw.circle(screen, self.color, point, self.radius)
