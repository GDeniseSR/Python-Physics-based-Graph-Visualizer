import pygame
from typing import Union
from visualizer.Vector2 import Vector2

class Input():
    def __init__(self) -> None:
        self.buttons : dict[int, Button | MouseButton]= {}
        self.__mouse_pos : Vector2 = Vector2.ZERO
        self.__last_mouse_pos : Vector2 = Vector2.ZERO
    
    @property
    def mouse_pos(self):
        return self.__mouse_pos
    
    @property
    def last_mouse_pos(self):
        return self.__last_mouse_pos
    
    def is_pressed(self, key_code):
        if key_code in self.buttons:
            return self.buttons[key_code].pressed
    
    def is_long_pressed(self, key_code):
        if key_code in self.buttons:
            return self.buttons[key_code].long_pressed
    
    def get_button(self, key_code) -> Union["Button", "MouseButton", None]:
        if key_code in self.buttons:
            return self.buttons[key_code]
    
    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.__last_mouse_pos = self.__mouse_pos
                self.__mouse_pos = Vector2(*pygame.mouse.get_pos())
            
            elif event.type == pygame.KEYDOWN:
                key_code = event.key
                if key_code in self.buttons:
                    self.buttons[key_code].press()
                    
            elif event.type == pygame.KEYUP:
                key_code = event.key
                if key_code in self.buttons:
                    self.buttons[key_code].release()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button = event.button 
                if mouse_button in self.buttons:
                    self.buttons[mouse_button].press()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_button = event.button 
                if mouse_button in self.buttons:
                    self.buttons[mouse_button].release()
        
        
        for button in self.buttons.values():
            button.update(delta_time)
    
    def add_button(self, key_code, short_press_threshold = 0.2):
        self.buttons[key_code] = Button(self, short_press_threshold)
    def add_mouse_button(self, key_code, short_press_threshold = 0.2):
        self.buttons[key_code] = MouseButton(self, short_press_threshold)
    
    
    def add_press_function(self, key_code, func):
        if key_code in self.buttons:
            self.buttons[key_code].add_press_func(func)
    def add_short_release_function(self, key_code, func):
        if key_code in self.buttons:
            self.buttons[key_code].add_short_release_func(func)
    def add_long_release_function(self, key_code, func):
        if key_code in self.buttons:
            self.buttons[key_code].add_long_release_func(func)

class Button:
    def __init__(self, input_instance : Input, short_press_threshold = 0.2) -> None:
        self._input_instance = input_instance
        self.press_functions = []
        self.short_release_funcs = []
        self.long_release_funcs = []
        
        self.short_press_threshold = short_press_threshold
        
        self.pressed = False
        self.long_pressed = False
        self.__time_pressed = 0
    
    def update(self, delta_time):
        if self.pressed:
            self.__time_pressed += delta_time
            
            if not self.long_pressed:
                if self.__time_pressed > self.short_press_threshold:
                    self.long_pressed = True
    
    def press(self):
        self.pressed = True
        self.__time_pressed = 0
        for func in self.press_functions:
            func()
    
    def release(self):        
        if self.long_pressed:
            self.long_release()
        else:
            self.short_release()
        
        self.__time_pressed = 0
        self.pressed = False
        self.long_pressed = False
    
    def short_release(self):
        for func in self.short_release_funcs:
            func()
    def long_release(self):
        for func in self.long_release_funcs:
            func()
    
    
    def add_short_release_func(self, func):
        self.short_release_funcs.append(func)
    def add_long_release_func(self, func):
        self.long_release_funcs.append(func)
    def add_release_func(self, func):
        self.short_release_funcs.append(func)
        self.long_release_funcs.append(func)
    def add_press_func(self, func):
        self.press_functions.append(func)


class MouseButton(Button):
    def __init__(self, input_instance, short_press_threshold=0.2) -> None:
        super().__init__(input_instance, short_press_threshold)
        self.drag_funcs = []
        
        self.__start_mouse_pos : Vector2 = None
        self.current_mouse_pos : Vector2 = None

    @property
    def start_mouse_pos(self):
        return self.__start_mouse_pos
    
    def update(self, delta_time):
        if self.pressed:
            self.current_mouse_pos =  self._input_instance.mouse_pos
            
        super().update(delta_time)
        
        if self.long_pressed:           
            for func in self.drag_funcs:
                func(self.__start_mouse_pos, self.__start_mouse_pos)
    
    def press(self):
        self.__start_mouse_pos = self._input_instance.mouse_pos
        self.current_mouse_pos = self.__start_mouse_pos
        
        super().press()
    
    def long_release(self):
        for func in self.long_release_funcs:
            func(self.__start_mouse_pos, self.current_mouse_pos)