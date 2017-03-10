import math

from dolfin import Point, plot
import mshr


class Mesh():
    def __init__(self, dimension, robot_radius):
        # Correct the map size by the robot_radius
        self.robot_radius = robot_radius
        self.dimension = list(map(lambda x: x - robot_radius, dimension))

        # Define the base rectangle.
        self._map = mshr.Rectangle(
            Point(robot_radius, robot_radius),
            Point(self.dimension[0], self.dimension[1])
        )

        self._mesh2d = None

    def add_circle_obstacle(self, p, radius, mirror=False):
        points = [Point(p[0], p[1])]

        # Replicate the circle on the other edge of the map.
        if mirror:
            points.append(Point(self.dimension[0] + self.robot_radius - p[0], p[1]))

        for point in points:
            self._map -= mshr.Circle(point, radius + self.robot_radius, 5)

    def add_rectangle_obstacle(self, p1, p2, mirror=False):
        self._map -= mshr.Rectangle(
            self.__correct_point(Point(p1[0], p1[1]), inverse=-1),
            self.__correct_point(Point(p2[0], p2[1]))
        )

        # Replicate the data the other side of the map.
        if mirror:
            p1bis = Point(
                self.dimension[0] + self.robot_radius - p1[0] + self.robot_radius,
                p1[1] - self.robot_radius
            )
            p2bis = Point(
                self.dimension[0] + self.robot_radius - p2[0] - self.robot_radius,
                p2[1] + self.robot_radius
            )

            self._map -= mshr.Rectangle(p2bis, p1bis)

    # As dolfin and mshr don't support leaning rectangle, we build the
    # rectangle giving him the point with the minimum y data,
    # the absolute y size, the width, the angle with the 0 starting
    # with the x axis.
    # The accuracy give the number of rectangles we want to cut the
    # leaning rectangle.
    def add_leaning_rectangle_obstacle(self, p, height, width, angle,
                                       mirror=False, accuracy=10):
        height_chunck_size = height / (accuracy)

        radian_angle = math.radians(angle)
        for chunck in range(accuracy):
            pos = chunck * height_chunck_size + height_chunck_size / 2
            # Get the center of the little rectangle.
            center_point = (pos * math.cos(radian_angle),
                            pos * math.sin(radian_angle))

            self.__build_rectangle_by_center(p, center_point,
                                             height_chunck_size,
                                             width, mirror)

    def __build_rectangle_by_center(self, base_point, p, height, width,
                                    mirror=False):
        p1 = (base_point[0] + p[0] + width / 2,
              base_point[1] + p[1] + height / 2)
        p2 = (base_point[0] + p[0] - width / 2,
              base_point[1] + p[1] - height / 2)
        self.add_rectangle_obstacle(p1, p2, mirror)

    def __correct_point(self, p, inverse=1):
        return Point(p.x() + self.robot_radius*inverse,
                     p.y() + self.robot_radius*inverse)

    def build(self, accuracy=10):
        self._mesh2d = mshr.generate_mesh(self._map, accuracy)

    def display(self, accuracy=10):
        if self._mesh2d is None:
            self.build(accuracy)
        plot(self._mesh2d, interactive=True)
