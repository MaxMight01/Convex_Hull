import pygame
import pygame.gfxdraw
from alg import jarvis_march

def drawAACircle(surf, color, center, radius, width):
    pygame.gfxdraw.aacircle(surf, *center, radius, color)  
    pygame.gfxdraw.aacircle(surf, *center, radius-width, color)  
    pygame.draw.circle(surf, color, center, radius, width) 

def square_distance(P, Q):
    return (P[0]-Q[0])**2 + (P[1]-Q[1])**2

class Controller():
    def __init__(self, radius, color, width):
        self.point_list = []
        self.radius = radius
        self.color = color
        self.update = False
        self.edges = []
        self.width = width
        self.dragging = False
        self.dragging_point = None

    def handle_mouse_event(self, button, position, type):
        if button == 1:
            if type == pygame.MOUSEBUTTONDOWN:
                in_range = False
                for point in self.point_list:
                    if square_distance(point, position) < self.radius**2:
                        self.dragging_point = point
                        self.dragging = True
                        in_range = True
                        break
                if not in_range:
                    self.point_list.append(position)
                    self.update = True
            if type == pygame.MOUSEBUTTONUP:
                if self.dragging_point is not None:
                    self.dragging = False
                    self.update = True
        if button == 3:
            for point in self.point_list:
                if square_distance(point, position) < self.radius**2:
                    self.point_list.remove(point)
                    self.update = True
                    break

    def draw_points(self, screen):
        for point in self.point_list:
            #pygame.draw.circle(screen, self.color, point, self.radius)
            drawAACircle(screen, self.color, point, self.radius, self.width)

    def draw_edges(self, screen):
        for edge in self.edges:
            pygame.draw.aaline(screen, self.color, *edge)

    def update_dragging(self):
        if self.dragging_point is not None:
            self.update = True
            self.point_list.remove(self.dragging_point)

            mouse_coords = pygame.mouse.get_pos()
            self.point_list.append(mouse_coords)
            self.dragging_point = mouse_coords

    def update_edges(self):
        if self.update:
            self.edges = jarvis_march.ConvexHull(self.point_list)
            self.update = False