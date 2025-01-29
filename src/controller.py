import pygame
import pygame.gfxdraw
import time
from alg import jarvis_march
from alg import grahams_scan

def drawAACircle(surf, color, center, radius, width):
    pygame.gfxdraw.aacircle(surf, *center, radius, color)  
    pygame.gfxdraw.aacircle(surf, *center, radius-width, color)  
    pygame.draw.circle(surf, color, center, radius, width) 

def square_distance(P, Q):
    return (P[0]-Q[0])**2 + (P[1]-Q[1])**2

class Controller():
    def __init__(self, radius, color, width, algorithm):
        self.point_list = []
        self.radius = radius
        self.color = color
        self.update = False
        self.edges = []
        self.width = width
        self.dragging = False
        self.dragging_point = None
        self.hovering = False
        self.algorithm = algorithm
        self.font = pygame.font.Font(None, 36)
        self.execution_time_text_surface = self.font.render(f"Computation Time: N/A", True, self.color)
        self.execution_time_text_rect = self.execution_time_text_surface.get_rect(topleft=(10, 10))

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
        if self.algorithm == "Jarvis March":
            for edge in self.edges: # Edges are given here
                pygame.draw.aaline(screen, self.color, *edge)
        elif self.algorithm == "Graham-s Scan":
            for i in range(0, len(self.edges)-1): # Circular set of points are given here
                pygame.draw.aaline(screen, self.color, self.edges[i], self.edges[i+1])
            
            # pygame.draw.aaline(screen, self.color, self.edges[0], self.edges[-1])

    def draw_text(self, screen):
        screen.blit(self.execution_time_text_surface, self.execution_time_text_rect)

    def update_hovering(self, mouse_coords):
        hovering = False
        for point in self.point_list:
            if square_distance(point, mouse_coords) < self.radius**2:
                hovering = True
                break
        self.hovering = hovering


    def update_dragging(self, mouse_coords):
        if self.dragging_point is not None:
            self.update = True
            self.point_list.remove(self.dragging_point)
            
            self.point_list.append(mouse_coords)
            self.dragging_point = mouse_coords

    def update_edges(self):
        if self.update:
            start_time = time.time()
            if self.algorithm == "Jarvis March":
                self.edges = jarvis_march.ConvexHull(self.point_list)
            elif self.algorithm == "Graham-s Scan":
                self.edges = grahams_scan.ConvexHull(self.point_list)
            end_time = time.time()
            
            self.execution_time_text_surface = self.font.render(f"Computation Time: {end_time - start_time:.6f} seconds", True, self.color)
            self.execution_time_text_rect = self.execution_time_text_surface.get_rect(topleft=(10, 10))
            self.update = False