import pygame
from Vector2 import Vector2

def draw_arrow(
    surface : pygame.Surface,
    start : Vector2,
    end : Vector2,
    color : pygame.Color,
    width : int = 2,
    head_length : float = 10,
    head_angle : float = 30  # degrees
):
    """Draw an arrow using three lines."""

    # Draw line
    pygame.draw.line(surface, color, tuple(start), tuple(end), width)

    # Arrow head
    # Direction vector from start to end
    direction = start - end
    if direction.magnitude == 0:
        return
    
    direction.normalize()

    # Rotate direction to create head lines
    left_head = direction.rotated(head_angle) * head_length
    right_head = direction.rotated(-head_angle) * head_length

    # Draw the two arrowhead lines
    pygame.draw.line(surface, color, tuple(end), tuple(end + left_head), width)
    pygame.draw.line(surface, color, tuple(end), tuple(end + right_head), width)
