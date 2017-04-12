import math
import os.path
import operator

import matplotlib.pyplot as plt
import networkx as nx

from utils import GraphUtils

class GraphMap:
    def __init__(self, nodes, triangles, cache=False):
        """
        nodes represent the (x, y) address of nodes in the graph.
        triangles give the 3 positions in nodes array to form a triangle.
        """
        self._cache = cache
        self._cache_path = '/tmp/graphmap.data'

        # Remove nodes and edges to simulate obstacles.
        self._obstacles_cache = {'nodes': [], 'edges': []}

        self._graph = None
        if self._cache and os.path.exists(self._cache_path):
            self._graph = self.__read_cache()
        else:
            self.__build_graph_from_mesh(nodes, triangles)

    def get_path(self, robot_pos, target, display=False):
        # Give ID to the start node and end node.
        START_NODE_ID = 1000
        END_NODE_ID = 1001

        # Get the neirest node from the robot position and the target position.
        # The direction is of start_node is the target (make sense) and vise-versa.
        start_node = self.get_neirest_node_pos(robot_pos['point'], target['point'])
        end_node = self.get_neirest_node_pos(target['point'], robot_pos['point'])

        # Remove edge added to the process before looking for the shortest path.
        # This could give unvalid result.
        nodes = self._graph.nodes()
        if START_NODE_ID in nodes and END_NODE_ID in nodes:
            self._graph.remove_node(START_NODE_ID, END_NODE_ID)

        path = nx.shortest_path(self._graph, source=start_node, target=end_node, weight='weight')

        self._graph.add_node(START_NODE_ID, pos=robot_pos['point'], color='green')
        self._graph.add_node(END_NODE_ID, pos=target['point'], color='green')

        # If we display the graph map, color the path that the robot should have taken.
        if display:
            self._graph.add_edge(START_NODE_ID, path[0], color='green')
            self._graph.add_edge(path[-1], END_NODE_ID, color='green')
            for i in range(len(path) - 1):
                self._graph.edge[path[i]][path[i+1]]['color'] = 'green'

        path = [START_NODE_ID] + path
        path.append(END_NODE_ID)

        return self.__convert_nodelist_to_instruction(path, robot_pos['angle'], target['angle'])

    def add_obstacle(self, robot_pos, robot_dim, obstacle_dim, obstacle_position, obstacle_distance):
        obstacle_points = self.__create_obstacle_rectangle(robot_pos, robot_dim, obstacle_dim, obstacle_position,
                obstacle_distance)
        (minx, miny, maxx, maxy) = GraphUtils.get_min_max_points(obstacle_points)

        for n in self._graph.nodes():
            p = self._graph.node[n]['pos']
            if GraphUtils.is_point_in_rectangle(minx, miny, maxx, maxy, p[0], p[1]):
                # Remove nodes and every edges in it.
                self._obstacles_cache['nodes'].append({'id': n, 'attr': self._graph.node[n]})

                for neighbor in self._graph.neighbors(n):
                    self._obstacles_cache['edges'].append({'id': (n, neighbor),
                        'attr': self._graph.edge[n][neighbor]})
                self._graph.remove_node(n)

        for edge in self._graph.edges():
            p1 = self._graph.node[edge[0]]['pos']
            p2 = self._graph.node[edge[1]]['pos']

            if GraphUtils.is_line_cross_rectangle(minx, miny, maxx, maxy, p1[0], p1[1], p2[0], p2[1]):
                # We can remove the edge.
                self._obstacles_cache['edges'].append({'id': edge,
                    'attr': self._graph.edge[edge[0]][edge[1]]})
                self._graph.remove_edge(edge[0], edge[1])

    def reset_obstacles(self):
        # Add back the nodes.
        for node in self._obstacles_cache['nodes']:
            self._graph.add_node(node['id'], attr_dict=node['attr'])

        # Add back the edges.
        for edge in self._obstacles_cache['edges']:
            self._graph.add_edge(edge['id'][0], edge['id'][1], attr_dict=edge['attr'])

    def display(self):
        """
        Use matplotlib to display graph.
        """
        node_color = list(nx.get_node_attributes(self._graph, 'color').values())
        edge_color = list(nx.get_edge_attributes(self._graph, 'color').values())
        nx.draw_networkx(self._graph, nx.get_node_attributes(self._graph, 'pos'),
                         node_size=20, with_labels=True, edge_color=edge_color,
                         node_color=node_color)
        plt.show()

    def save(self):
        nx.write_gpickle(self._graph, self._cache_path)

    def __read_cache(self):
        return nx.read_gpickle(self._cache_path)

    def get_neirest_node_pos(self, point, direction):
        """
        Get the neirest node position according to the direction.
        Takes 2 nodes ID and return another one.
        """
        best_matches = []
        # Get the neirest points.
        for node in self._graph.nodes():
            node_pos = self._graph.node[node]['pos']
            dist_point = self.__distance_btw_points(point, node_pos)
            dist_dest = self.__distance_btw_points(direction, node_pos)
            if dist_point < 30:
                best_matches.append({'dist_point': dist_point,
                                     'dist_dest': dist_dest,
                                     'node': node})
        # Get the point which is the closest to the direction we need to go to.
        return sorted(best_matches, key=operator.itemgetter('dist_dest'))[0]['node']

    def __simplify_turn_angle(self, angle):
        """
        Convert angle [0; 360] to [-180: 180] degrees to simplify the rotation of the
        robot.
        """
        if abs(angle) > 180:
            sign = 1 if angle > 0 else -1
            angle = -sign*(360 - abs(angle))
        return round(angle)

    def __convert_nodelist_to_instruction(self, path, robot_angle, target_angle):
        """
        Convert the node id list to instruction easily understandable for the robot control.
        Return a list of dict() with a key giving the movement ("move" or "turn") and a key giving
        a value (distance in cm for "move" or turning degrees for "turn"). The value can be positive
        or negative.

        value/movement|  "move"    |    "turn"
        ----------------------------------------
        positive      |  forward   |    right
        ----------------------------------------
        negative      |  backward  |    left
        ----------------------------------------
        """
        actions = []

        # First turn is a bit specific so we don't do it in the for loop.
        start_angle_constrain = self.__get_node_angle(path[0], path[1])
        actions.append({'action': 'turn', 'value': self.__simplify_turn_angle(start_angle_constrain - robot_angle)})

        for i in range(len(path) - 2):
            # Add the distance actions
            distance = self.__distance_btw_points(
                    self._graph.node[path[i]]['pos'],
                    self._graph.node[path[i+1]]['pos']
            )
            # Check if have 2 moves actions successively.
            if actions[-1]['action'] == 'move':
                actions[-1]['value'] += distance
            else:
                actions.append({'action': 'move', 'value': round(distance)})

            # Try to simplify the actions by removing actions making a triangle.
            # A triangle means that the actions could be made by a straight line.
            if (i > 2) and (actions[-2]['action'] == 'turn') and (abs(actions[-2]['value']) < 26):
                    # Begin the simplication.
                    # Calculate the new distance
                    a = actions[-3]['value']
                    b = actions[-1]['value']
                    triange_angle = 180 - actions[-2]['value']
                    new_distance = a**2 + b**2 - 2*a*b*math.cos(math.radians(triange_angle))
                    actions[-1]['value'] = round(math.sqrt(new_distance))

                    del actions[-3]

                    # Correct the angle
                    node_pos = self._graph.node[path[i-3]]['pos']
                    center_pos = self._graph.node[path[i-2]]['pos']
                    next_node_pos = self._graph.node[path[i]]['pos']

                    turn_angle = self.__calculate_turn_angle(node_pos, center_pos, next_node_pos)
                    if turn_angle != 0:
                        if actions[-3]['action'] == 'turn':
                            actions[-3]['value'] += turn_angle
                            del actions[-2]
                        else:
                            actions[-2] = {'action': 'turn', 'value': turn_angle}

            # Add the turn actions.
            node_pos = self._graph.node[path[i]]['pos']
            center_pos = self._graph.node[path[i+1]]['pos']
            next_node_pos = self._graph.node[path[i+2]]['pos']

            turn_angle = self.__calculate_turn_angle(node_pos, center_pos, next_node_pos)
            if turn_angle != 0:
                actions.append({'action': 'turn', 'value': turn_angle})

        # Finalize the last moving and turning.
        distance = self.__distance_btw_points(
            self._graph.node[path[-2]]['pos'],
            self._graph.node[path[-1]]['pos']
        )
        actions.append({'action': 'move', 'value': int(distance)})

        end_robot_angle = self.__get_node_angle(path[-1], path[-2])
        actions.append({'action': 'turn', 'value':
                        self.__simplify_turn_angle(end_robot_angle - target_angle)})

        return actions

    def __calculate_turn_angle(self, node, center, next_node):
        opposite_pos = (center[0]+(center[0]-node[0]),
                        center[1] + (center[1]-node[1]))
        # Calculate the 2 angles needed to get the turn angle.
        angle1 = self.__get_pos_angle(center, opposite_pos)
        angle2 = self.__get_pos_angle(center, next_node)

        return self.__simplify_turn_angle(angle2 - angle1)

    def __build_graph_from_mesh(self, nodes, triangle_cells):
        """
        nodes: position of each nodes in the mesh.
        triangle_cells: list of triangle cells list
        A triangle cell is a 3 items lists with each items is a vertice
        of a triangle.
        """
        graph = nx.Graph()
        for i, n in enumerate(nodes):
            graph.add_node(i, pos=n, color='red')

        for conns in triangle_cells:
            for i, c in enumerate(conns):
                p1 = c
                p2 = conns[(i+1) % 3]

                weight = self.__distance_btw_points(
                        graph.node[p1]['pos'],
                        graph.node[p2]['pos']
                )
                graph.add_edge(p1, p2, weight=weight, color='black')

        self._graph = graph
        # Not useful but could be.
        self.__mark_nodes_as_border()
        self.__clean()

        if self._cache:
            self.save()

    def __distance_btw_points(self, p1, p2):
        x = (p1[0] - p2[0])**2
        y = (p1[1] - p2[1])**2
        return math.sqrt(x + y)

    def __clean(self):
        """
        Merges useless nodes according to the distance between 2 nodes.
        """
        for i in range(300):
            for e in self._graph.edges():
                if e[0] == e[1]:
                    continue
                if self._graph[e[0]][e[1]]['weight'] < 7:
                    self.__merge_nodes(e[0], e[1])
                    break

    def __merge_nodes(self, node, old_node):
        """
        Takes 2 node ids. One will stay, one will be eaten.
        Obvioulsy, the first will eat the second.
        """
        if node == old_node:
            return
        out_edge_node = self._graph.neighbors(node)
        out_edge_old_node = self._graph.neighbors(old_node)

        for edge in out_edge_old_node:
            if edge not in out_edge_node:
                weight = self.__distance_btw_points(
                    self._graph.node[node]['pos'],
                    self._graph.node[edge]['pos']
                )
                self._graph.add_edge(node, edge, weight=weight, color='black')

        self._graph.remove_node(old_node)

    def __mark_nodes_as_border(self):
        """
        Flag nodes when they are in the borders.
        Moslty works.

        Works by checking the biggest opening angle between 2 triangles.
        """
        for node in self._graph.nodes():
            out_edges = self._graph.neighbors(node)
            if len(out_edges) == 2 or len(out_edges) == 1:
                self._graph.node[node]['color'] = 'blue'
                self._graph.node[node]['mesh_edge'] = True
                continue

            angles = sorted(self.__get_neighbors_angle(node),
                            key=lambda k: k['angle'])

            biggest_angle = 0
            for i in range(len(angles)):
                a1 = angles[i]['angle']
                a2 = angles[(i+1) % len(angles)]['angle']

                a_diff = (a2 - a1)
                if a_diff < 0:
                    a_diff += 360
                if abs(a_diff) > biggest_angle:
                    biggest_angle = abs(a_diff)
            if biggest_angle > 105:
                self._graph.node[node]['color'] = 'blue'
                self._graph.node[node]['mesh_edge'] = True

    def __get_neighbors_angle(self, node_id):
        neighbors = self._graph.neighbors(node_id)

        data = []
        for i in neighbors:
            data.append({'neighbor': i, 'angle': self.__get_node_angle(node_id, i)})

        return data

    def __get_pos_angle(self, center, node, upper=(0, 0)):
        """
        Calculate an angle between 3 points using the law of cosine.
        """
        # Little hack allows to create a fake x axis.
        if upper == (0, 0):
            upper = (2000, center[1])

        a = self.__distance_btw_points(center, node)
        b = self.__distance_btw_points(center, upper)
        c = self.__distance_btw_points(node, upper)

        # Law of cosine
        cosinelaw = (a**2 + b**2 - c**2) / (2*a*b)
        # Clamp the value between [-1; 1] because of inaccuracy in
        # floating point numbers.
        cosinelaw = max(min(cosinelaw, 1.0), -1.0)
        angle = math.degrees(math.acos(cosinelaw))
        # Check if we have passed the 180 degrees or not.
        xpos1 = node[1] - center[1]
        if xpos1 > 0:
            angle = 360 - angle

        return angle

    def __get_node_angle(self, center, node):
        """
        The angle is the absolute angle relative to the X axis.
        """
        center_pos = self._graph.node[center]['pos']
        point_pos = self._graph.node[node]['pos']
        return self.__get_pos_angle(center_pos, point_pos)

    def __create_obstacle_rectangle(self, robot_pos, robot_dim, obstacle_dim, obstacle_pos, obstacle_distance):
        direction = 1
        if robot_pos['angle'] > 180:
            direction = -1
        if obstacle_pos == 'front':
            return GraphUtils.generate_translated_rectangle(robot_pos['point'], robot_pos['angle'],
                    robot_dim['length']/2, robot_dim['width']/2,
                    obstacle_distance+obstacle_dim, 1)
        elif obstacle_pos == 'left':
            return GraphUtils.generate_translated_rectangle(robot_pos['point'], robot_pos['angle']+direction*90,
                    robot_dim['length']/2, robot_dim['width']/2,
                    obstacle_distance+obstacle_dim, direction)
        elif obstacle_pos == 'right':
            return GraphUtils.generate_translated_rectangle(robot_pos['point'], robot_pos['angle']-direction*90,
                    robot_dim['length']/2, robot_dim['width']/2,
                    obstacle_distance+obstacle_dim, direction)
        elif obstacle_pos == 'back':
            return GraphUtils.generate_translated_rectangle(robot_pos['point'], robot_pos['angle'] + 180,
                    robot_dim['length']/2, robot_dim['width']/2,
                    obstacle_distance+obstacle_dim, 1)
        return None
