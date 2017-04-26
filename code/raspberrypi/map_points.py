class Assets():
    POINTS ={
        'yellow': [
            {'name':'start', 'point': (9.5,16), 'angle': 0},
            {'name':'rocket', 'point': (124.5,38), 'angle': 270},
            {'name':'mono1', 'point': (58,50.5), 'angle': 180},
            {'name':'mono2', 'point': (57.7,147), 'angle': 72},
            {'name':'remove', 'point': (95,122.5), 'angle': 135},
            {'name':'discharge', 'point': (), 'angle': 0}]

        'blue': [
            {'name':'start', 'point': (290.5,16), 'angle': 180},
            {'name':'rocket', 'point': (194.5,38), 'angle': 270},
            {'name':'mono1', 'point': (58,69.5), 'angle': 0},
            {'name':'mono2', 'point': (242.3,147), 'angle': 150},
            {'name':'remove', 'point': (205,122.5), 'angle': 45},
            {'name':'discharge', 'point': (), 'angle': }]
        ]
    }

    def __init__(self, color):
        self.color = color

    def get_point(self, name):
        for point in self.POINTS[color]:
            if point['name'] == name:
                return point
        assert(False, 'Could not find point with name {}'.format(name))
