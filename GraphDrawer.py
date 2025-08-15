import pygame
from pygame.surface import Surface
import colorsys

import DrawArrow

from Graph import *
from Input import *
from Node import *
from Vector2 import Vector2
from Camera import Camera
import GraphPhysics
import Collisions

def collides_with_any_node(x, y, graph : Graph, distance = 0):
    for node in graph.vertices:
        if Collisions.distance_btwn_points_sq(Vector2(x, y), node.pos) < distance**2:
            return node
    return None


component_colors : list[tuple[int, int, int]] = []
_hue = 0.0  # starting hue
_GOLDEN_RATIO_CONJUGATE = 0.61803398

def generate_colors(n: int = 1):
    global _hue, _GOLDEN_RATIO_CONJUGATE
    for _ in range(n):
        _hue = (_hue + _GOLDEN_RATIO_CONJUGATE) % 1.0
        r, g, b = colorsys.hsv_to_rgb(_hue, 0.65, 0.95)
        
        color = (int(r * 255), int(g * 255), int(b * 255))
        component_colors.append(color)
        
text_surfaces : dict[Node, Surface] = {}

def main(graph:Graph[Node]):
    def on_left_press():
        nonlocal graph, input, left_click_drag_node, node_radius
        
        x,y = camera.screen_to_world(input.mouse_pos)
        
        left_click_drag_node = None
        node = collides_with_any_node(x, y, graph, 1*node_radius)
        if node != None:
            left_click_drag_node = node


    def on_left_click():
        nonlocal graph, input, camera, node_radius
        x, y = camera.screen_to_world(input.mouse_pos)
        node = collides_with_any_node(x, y, graph, 2*node_radius)
        if node == None:
            graph.add(Node(len(graph.vertices), x, y))
            
    def on_right_click():
        nonlocal graph, input, camera, node_radius
        x, y = camera.screen_to_world(input.mouse_pos)
        node = collides_with_any_node(x, y, graph, node_radius)
        if node != None:
            graph.remove(node)
    
    def on_left_drag_stop(start_pos, end_pos):
        nonlocal graph, camera, node_radius, left_click_drag_node
        
        end_pos = camera.screen_to_world(end_pos)
        if left_click_drag_node != None:
            end_node = collides_with_any_node(*end_pos, graph, node_radius)
            if end_node != None and left_click_drag_node != end_node:
                graph.connect(left_click_drag_node, end_node, 1)
    
    
    # Initialize Pygame
    pygame.init()
    # Set the dimensions of the window
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    # Set the title of the window
    pygame.display.set_caption("Graph")

    # Camera
    camera = Camera()
    desired_position : Vector2 = camera.position

    # Main loop control variable
    running = True

    # Define the frames per second (FPS)
    FPS = 60
    clock = pygame.time.Clock()
    delta_time = 0

    node_radius = 20

    # Variables to track mouse events
    left_click_drag_node : Node = None

    # Input management
    LEFT_MOUSE_BUTTON = 1
    MIDDLE_MOUSE_BUTTON = 2
    RIGHT_MOUSE_BUTTON = 3
    input = Input()

    input.add_mouse_button(LEFT_MOUSE_BUTTON, short_press_threshold=0.2)
    input.add_mouse_button(MIDDLE_MOUSE_BUTTON, 0.2)
    input.add_mouse_button(RIGHT_MOUSE_BUTTON, 0.2)

    input.add_press_function(LEFT_MOUSE_BUTTON, on_left_press)
    input.add_short_release_function(LEFT_MOUSE_BUTTON, on_left_click)
    input.add_long_release_function(LEFT_MOUSE_BUTTON, on_left_drag_stop)

    input.add_short_release_function(RIGHT_MOUSE_BUTTON, on_right_click)

    # Main game loop
    while running:
        events = pygame.event.get()

        # Updates the input class
        input.update(delta_time, events)
        
        # Event handling
        for event in events:
            if event.type == pygame.QUIT:  # User closes the window
                running = False
            
            if event.type == pygame.MOUSEMOTION:
                # Camera movement
                if input.is_pressed(MIDDLE_MOUSE_BUTTON):
                    mouse_pos_delta : Vector2 = (input.mouse_pos - input.last_mouse_pos) / camera.zoom_level

                    # Limit the max speed of camera movement to prevent large jumps
                    max_speed = 20 / camera.zoom_level
                    mouse_pos_delta.clamp_magnitude(max_speed)

                    # Set the desired camera position
                    desired_position -=  mouse_pos_delta

                # Checks if the right mouse button is pressed and the mouse is moving, to break any edge the mouse crosses
                if input.is_pressed(RIGHT_MOUSE_BUTTON):
                    for n1 in graph.vertices:
                        for n2 in list(graph.adjacent_vertices(n1)):
                            cut_edge = Collisions.lines_intersect(camera.screen_to_world(input.last_mouse_pos),
                                                       camera.screen_to_world(input.mouse_pos),
                                                       n1.pos, n2.pos)
                            if cut_edge:
                                graph.disconnect(n1, n2)
                
            elif event.type == pygame.MOUSEWHEEL:
                camera.zoom_level += event.y * 3 * delta_time
        
        # Smoothly move the camera towards the desired position using linear interpolation (lerp)
        lerp_speed = 20
        t = lerp_speed * delta_time
        camera.position += (desired_position - camera.position) * min(t, 1)
        
        GraphPhysics.apply_node_forces(graph, input, camera, left_click_drag_node, delta_time)

        draw_graph(screen, graph, camera, input, node_radius, left_click_drag_node)
        
        # Cap the frame rate and get the time in seconds between frames
        delta_time = clock.tick(FPS) / 1000

    # Clean up Pygame resources
    pygame.quit()


def draw_graph(screen, graph:Graph[Node], camera:Camera, input:Input, node_radius:int, left_drag_start_node:Node):
    # Define colors (RGB)
    WHITE = (255, 255, 255)
    RED = (255, 40, 40)
    BLUE = (40, 40, 255)

    # Initialize font (using default font with size 24)
    font_size = 24

    # Fill the screen with white color (clears previous frame)
    screen.fill(WHITE)    
    
    node_radius_pixels = node_radius * camera.zoom_level
    arrow_head_length_pixels = 15 * camera.zoom_level
    
    # Update the start of the dragging line point if it's dragging a node and draw said line
    if input.is_long_pressed(1):
        if left_drag_start_node != None:
            start_pos = camera.world_to_screen(left_drag_start_node.pos)
        else:
            start_pos = input.get_button(1).start_mouse_pos
        
        DrawArrow.draw_arrow(screen, start_pos, input.mouse_pos, BLUE, width=2, head_length=arrow_head_length_pixels)
        
    
    # Find cut vertices to draw them on a different color
    if len(graph.vertices) > 0:
        cut_vertices = graph.cut_vertices
    
    
    # Draw edges
    is_directed = graph.is_directed
    for n1 in graph.vertices:
        for n2 in graph.adjacent_vertices(n1):
            start = camera.world_to_screen(n1.pos)
            end = camera.world_to_screen(n2.pos)
            
            if is_directed:
                diff = end-start
                dist = diff.magnitude
                
                if dist <= 0.001:
                    continue
                dir_vec = diff / dist

                # We end the arrow at the circunference of each node
                length = max(0.0, dist - node_radius_pixels)
                
                end = start + dir_vec * length
                
                DrawArrow.draw_arrow(screen, start, end,
                    BLUE, width=2, head_length=arrow_head_length_pixels)
            else:
                pygame.draw.line(screen, BLUE, tuple(start), tuple(end), width=2)
    
    # Draw every component. This will let you draw each component in a different color
    components = graph.connected_components
    n_components = len(components)
    if n_components > len(component_colors):
        generate_colors(n_components - len(component_colors))
    
    for i in range(len(components)):
        for n1 in components[i]:       
            if n1 in cut_vertices:
                pygame.draw.circle(screen, RED, tuple(camera.world_to_screen(n1.pos)), 1.1 * node_radius_pixels)
                pygame.draw.circle(screen, component_colors[i], tuple(camera.world_to_screen(n1.pos)), 0.85 * node_radius_pixels)
            else:
                pygame.draw.circle(screen, component_colors[i], tuple(camera.world_to_screen(n1.pos)), node_radius_pixels)
            
            # If zoomed out skip text
            if camera.zoom_level < 0.5:
                continue
            
            if n1 not in text_surfaces:
                 # Render the text for each node
                font = pygame.font.Font(None, int(font_size * camera.zoom_level))
                text_surface = font.render(str(n1.value), True, (0, 0, 0))
                text_surfaces[n1] = text_surface
            else:
                text_surface = text_surfaces[n1]
                
            # Calculate the position to center the text on the node
            text_rect = text_surface.get_rect(center=tuple(camera.world_to_screen(n1.pos)))
            
            # Blit (draw) the text surface on the screen
            screen.blit(text_surface, text_rect)

    
    # Update the display
    pygame.display.flip()

if __name__ == "__main__":
    main(Graph())