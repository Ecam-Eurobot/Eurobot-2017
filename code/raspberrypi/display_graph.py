from graphmap.map_generator import build_graph

if __name__ == '__main__':
    #  robot_pos = {'point': [ 87, 17.45 ], 'angle': 0}
    #  target_pos = {'point': (148, 16), 'angle': 0}
    robot_pos = { 'point': [ 211.5, 25.75], 'angle': 180 }
    target_pos = { 'point': (221.35, 103.9), 'angle': 135}

    g = build_graph(17.8, cache=True)
    print(g.get_path(robot_pos, target_pos, display=True))
    g.display()
