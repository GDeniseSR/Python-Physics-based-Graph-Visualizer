import pygame
from visualizer.Vector2 import Vector2

class Camera:
    def __init__(self):
        self.__offset : Vector2 = Vector2.ZERO  # Camera position offset
        self._zoom_level = 1.0  # Default zoom level

    # Getter and setter for position
    @property
    def position(self) -> Vector2:
        return Vector2(*self.__offset)
    @position.setter
    def position(self, new_position : Vector2):
        self.__offset = new_position

    # Getter and setter for zoom level
    @property
    def zoom_level(self):
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, new_zoom_level):
        self._zoom_level = max(new_zoom_level, 0.1)  # Prevent zoom from going below 0.1

    def world_to_screen(self, pos:Vector2) -> Vector2:
        """Transform a world position to a screen position based on camera offset and zoom."""
        window_size = Vector2(*pygame.display.get_window_size())
        
        screen_pos : Vector2 = (pos - self.__offset) * self.zoom_level + window_size / 2
        return screen_pos
    
    def screen_to_world(self, screen_pos : Vector2) -> Vector2:
        """Convert a screen position to a world position based on the camera."""
        window_size = Vector2(*pygame.display.get_window_size())
        
        world_pos : Vector2 = (screen_pos - window_size / 2) / self.zoom_level + self.__offset
        return world_pos
    
    