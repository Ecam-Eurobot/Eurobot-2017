import os.path

from .mesh import Mesh
from .graphmap import GraphMap


def build_mesh(robot_diagonal, removable=False, cache=True):
    m = Mesh((300, 200), robot_diagonal)

    # Define the start area.
    m.add_rectangle_obstacle((0, 36), (71, 38.2), mirror=True)

    # Define the rockets distributor near the start area.
    m.add_circle_obstacle((115, 4), 4+3, mirror=True)

    # Define the rocket on the map side.
    m.add_circle_obstacle((4, 135), 4+3, mirror=True)

    # Define the little lunar rock reservoir.
    m.add_circle_obstacle((65, 54), 13+5, mirror=True)

    # Define the other little lunar rock reservoir.
    m.add_circle_obstacle((115, 187), 13+3, mirror=True)

    # Define the big lunar rock reservoir.
    m.add_circle_obstacle((0, 200), 51+25, mirror=True, accuracy=20)

    # Define the side module collector.
    m.add_rectangle_obstacle((0, 70), (8, 115), mirror=True)

    # Define the big module collector:
    # - the centrum
    m.add_rectangle_obstacle((150, 115), (146, 200), mirror=True)
    # - the side
    m.add_leaning_rectangle_obstacle((86.36, 113.63), 90, 8 + 5, 45, mirror=True)
    # - the circle connecting the module connector
    m.add_circle_obstacle((150, 200), 20)

    # The removable lunar module.
    # The lunar module in the start is considered not here
    # as we will obsiously take them.
    if removable:
        m.add_circle_obstacle((20, 60), 6.3, mirror=True)
        m.add_circle_obstacle((100, 60), 6.3, mirror=True)
        m.add_circle_obstacle((50, 110), 6.3, mirror=True)
        m.add_circle_obstacle((90, 140), 6.3, mirror=True)
        m.add_circle_obstacle((80, 1850), 6.3, mirror=True)

    m.build(cache=cache)
    return m


def build_graph(robot_diagonal, cache=True):
    if os.path.exists(GraphMap.CACHE_PATH) and cache:
        return GraphMap(None, None)

    mesh = build_mesh(robot_diagonal, removable=False, cache=False)

    graph = GraphMap(mesh.get_nodes(), mesh.get_connectivity_cells(), cache=False)
    return graph


if __name__ == '__main__':
    graph = build_graph(17.8, cache=False)
    #  graph = GraphMap(cache=True).build_graph_from_mesh(m.get_nodes(), m.get_connectivity_cells())
    #  graph.display()
    #  graph.add_obstacle({'point': (150, 100), 'angle': 90}, {'length': 30, 'width': 20}, 25, 'front', 10)
    #  graph.reset_obstacles()
    #  graph.get_neirest_node_pos((56, 120), (200, 100))
    #  path = graph.get_path({'point': (17, 18), 'angle': 0}, {'point': (274, 132), 'angle': 0}, display=True)
    #  print(path, len(path))
    graph.display()
