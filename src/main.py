import pygame
import os
import utils
import controller

pygame.init()

# Opening the `parameters.json` file.
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_path = os.path.join(root_dir, 'assets', 'data', 'parameters.json')
params = utils.load_parameters(config_file_path)

# Screen resolution.
ratio_w, ratio_h = map(int, params["aspect_ratio"].split("-"))
screen_width, screen_height = utils.calculate_screen_dimensions(ratio_w, ratio_h)

# Screen setup and caption.
screen = utils.setup_screen_and_caption(screen_width, screen_height, params["caption"])

# Caption.
pygame.display.set_caption(params["caption"])

# Colors.
c_BACKGROUND = params["colors"]["background"]
c_POINT = params["colors"]["point"]

# fps and timer.
fps = params["fps"]
timer = pygame.time.Clock()

# Controller.
my_controller = controller.Controller(params["radius"], c_POINT, params["width"], screen_width, screen_height, params["algorithm"]["current"])

running = True
while running:
    timer.tick(fps)
    screen.fill(c_BACKGROUND)

    mouse_coords = pygame.mouse.get_pos()

    my_controller.draw_points(screen)
    if my_controller.dragging:
        my_controller.update_dragging(mouse_coords)
        my_controller.update_edges()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    else:
        my_controller.update_hovering(mouse_coords)
        if my_controller.hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    my_controller.draw_edges(screen)

    my_controller.draw_text(screen)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            my_controller.handle_mouse_event(event.button, event.pos, event.type)
            my_controller.update_edges()

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()