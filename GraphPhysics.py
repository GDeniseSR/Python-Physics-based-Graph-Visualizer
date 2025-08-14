from Graph import Graph
from Node import Node
from Input import Input
from Camera import Camera

def apply_node_forces(graph : Graph[Node], input : Input, camera : Camera, selected_node : Node, delta_time : float):
    spring_length = 100
    spring_force = 0.4
    repulsion_strength = 12000
    follow_mouse_strenght = 3
    follow_mouse_max_distance = 50
    
    for n1 in graph.vertices:
        # The node we're selecting will move towards the mouse
        if input.is_long_pressed(1) and selected_node == n1:            
            world_mouse_pos = camera.screen_to_world(input.mouse_pos)
            
            diff = world_mouse_pos - n1.pos
            dist = diff.magnitude
            
            force = dist * follow_mouse_strenght
            
            if dist > follow_mouse_max_distance:
                x = (dist - follow_mouse_max_distance)
                force /= 1 + x*x * 0.0001
            
            force = min(force, 1000)
            if dist > 0:
                force_vector = force * diff / dist
                n1.pos += force_vector * delta_time
        
        for n2 in graph.adjacent_vertices(n1):
            diff = n2.pos - n1.pos
            dist = diff.magnitude
            
            force = (diff.magnitude - spring_length) * 2 * spring_force # Spring force
            force = min(force, 1000)
            
            if diff.magnitude > spring_length:
                force_vector = force * diff / diff.magnitude
                
                n1.pos += force_vector * delta_time
                n2.pos -= force_vector * delta_time
                
        for n2 in graph.vertices:
            diff = n2.pos - n1.pos
            dist = diff.magnitude

            # Repulsion between all nodes            
            if dist > 0 and dist < 200:  # Only apply repulsion within a certain range
                force = repulsion_strength / (dist * dist) # Repulsion force
                force = min(force, 1000)
                
                force_vector = - force * diff / dist
                
                n1.pos += force_vector * delta_time
                n2.pos -= force_vector * delta_time