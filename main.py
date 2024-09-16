import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import random
import heapq
from ordered_set import OrderedSet


#Setup
dpg.create_context()
dpg.create_viewport(title="Algorithm Visualizer", width =600, height=350)
dpg.setup_dearpygui()


#example graph

graph = {
    #graph with 10 vertexes
    'A': [('B', 1), ('C', 2), ('D', 0)],
    'B': [('A', 1), ('C', 4)],
    'C': [('A', 2), ('B', 4) ],
    'D': [('A', 0)]
    
}

draw_height = 250
draw_width = 500

def run_search_algorithm(sender, app_data):
    start = dpg.get_value("start_node")
    goal = dpg.get_value("goal_node")
    
    if dpg.get_value("search_algorithm") == "Uniform Cost Search":
        make_ucs_search(goal, start)
    
def make_ucs_search(goal, start):
     with dpg.window():
                with dpg.drawlist(width=draw_width, height=draw_height):
        
                    dpg.draw_rectangle((0, 0), (draw_width, draw_height), color=(255, 255, 255, 255), fill=(255, 255, 255, 255))
                    
                    circle_radius = 10

                    elem_coords = {}
                    for elem in graph:

                        x_rand = random.randint(50,draw_width - 50)
                        y_rand = random.randint(50,draw_height - 50)
                                    
                        
                        elem_coords[elem] = (x_rand, y_rand )

                    for neighbor in graph:
                        for node in graph[neighbor]:
                            dpg.draw_arrow(elem_coords[neighbor], elem_coords[node[0]], color=(0, 0, 0, 255), thickness=2)
                            dpg.draw_text(((elem_coords[neighbor][0] + elem_coords[node[0]][0]) / 2, (elem_coords[neighbor][1] + elem_coords[node[0]][1]) / 2), str(node[1]), color=(255, 0, 0, 255), size=20)
                    
                    for elem in graph:
                        dpg.draw_circle(elem_coords[elem], circle_radius, color=(0, 0, 0, 255), fill=(255, 255, 255, 255))
                        dpg.draw_text(elem_coords[elem], elem, color=(0, 0, 0, 255))
        
                visited = OrderedSet()
                queue = []
                heapq.heappush(queue, (0, start))
                while queue:
                    cost, node = heapq.heappop(queue)
                    if node in visited:
                        continue
                    visited.add(node)
                    
                    dpg.draw_circle(elem_coords[node], circle_radius, color=(0, 255, 0, 255), fill=(0, 0, 0, 0))
                    try:
                        dpg.draw_arrow(elem_coords[node], elem_coords[visited[1]], color=(0, 255, 0, 255), thickness=2)
                    except:
                        pass
                    print(f"Goal: {goal}, Node: {node}")
                    if node == goal:
                        return
                    for neighbor, neighbor_cost in graph[node]:
                        if neighbor not in visited:
                            heapq.heappush(queue, (cost + neighbor_cost, neighbor))
                            
                    dpg.add_text(f"Visited: {visited}, Queue: {queue}")
                return

with dpg.value_registry():
    dpg.add_string_value(default_value="Uniform Cost Search", tag="search_algorithm")
    dpg.add_string_value(default_value="A", tag="start_node")
    dpg.add_string_value(default_value="A", tag="goal_node")
    
    
#Main Content
with dpg.window(label= "Algorithm Visualizer"):
    dpg.add_text("This is an algorithm visualizer for certain informed and uninformed search algorithms")
    #Create dropdown for selecting search algorithm
    with dpg.group():
        dpg.add_text("Select Search Algorithm")
        dpg.add_listbox(label="Search Algorithm", items=["Uniform Cost Search", "A* Search[WIP]", "Greedy Best First Search[WIP]"], 
                        source= "search_algorithm", width=200, callback= lambda sender: dpg.set_value("search_algorithm", dpg.get_item_label(sender)))
    #Create dropdown for selecting start node
    with dpg.group():
        dpg.add_text("Select Start Node")
        dpg.add_listbox(label="Start Node", items= list(graph.keys()), width=200, callback= lambda sender: dpg.set_value("start_node", dpg.get_value(sender)))
    #Create dropdown for selecting goal node
    with dpg.group():
        dpg.add_text("Select Goal Node")
        dpg.add_listbox(label="Goal Node", items= list(graph.keys()), width=200, callback= lambda sender: dpg.set_value("goal_node", dpg.get_value(sender)))
            
    #Create button to run the search algorithm
    dpg.add_button(label="Run Search Algorithm", callback= run_search_algorithm)
    

    


#Render view

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()