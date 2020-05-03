from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def starting_position(dir):
    opposites = {'n':'s','e':'w','s':'n','w':'e'}
    return opposites[dir]

def depth_first(current_room):
    visited = set()
    path = []

    def depth_first_recursive(current_room, previous_dir=None):
        visited.add(current_room.id)

        for exit in current_room.get_exits():
            next_room = current_room.get_room_in_direction(exit)

            if next_room.id in visited:
                continue
            else:
                visited.add(next_room.id)
                path.append(exit)

            depth_first_recursive(current_room.get_room_in_direction(exit), previous_dir=exit)
        
        if previous_dir is not None:
            original = starting_position(previous_dir)
            path.append(original)
    
    depth_first_recursive(current_room)
    return path

traversal_path = depth_first(world.starting_room)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
