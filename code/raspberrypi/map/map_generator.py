from mesh import Mesh

def build_map(removable=False):
    m = Mesh((300, 200), 17)

    # Define the start area.
    m.add_rectangle_obstacle((0, 36), (71, 38.2), mirror=True)

    # Define the rockets distributor near the start area.
    m.add_circle_obstacle((115, 4), 4, mirror=True)

    # Define the rocket on the map side.
    m.add_circle_obstacle((4, 135), 4, mirror=True)

    # Define the little lunar rock reservoir.
    m.add_circle_obstacle((71, 54), 8.5, mirror=True)

    # Define the other little lunar rock reservoir.
    m.add_circle_obstacle((115, 187), 8.5, mirror=True)

    # Define the big lunar rock reservoir.
    m.add_circle_obstacle((0, 200), 51, mirror=True)

    # Define the side module collector.
    m.add_rectangle_obstacle((0, 70), (8, 115), mirror=True)

    # Define the big module collector:
    # - the centrum
    m.add_rectangle_obstacle((150, 115), (146, 200), mirror=True)
    # - the side
    m.add_leaning_rectangle_obstacle((93.44, 143.43), 80, 8, 45, mirror=True)
    # - the circle connecting the module connector
    m.add_circle_obstacle((150, 200), 20)

    # The removable lunar module.
    # The lunar module in the start is considered not here
    # as we will obsiously take it.
    if removable:
        m.add_circle_obstacle((20, 60), 6.3, mirror=True)
        m.add_circle_obstacle((100, 60), 6.3, mirror=True)
        m.add_circle_obstacle((50, 110), 6.3, mirror=True)
        m.add_circle_obstacle((90, 140), 6.3, mirror=True)
        m.add_circle_obstacle((80, 1850), 6.3, mirror=True)

    return m

if __name__ == '__main__':
    m = build_map(removable=True)
    m.display(accuracy=5)
