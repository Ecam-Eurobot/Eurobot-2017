import math
import sys


class GraphUtils():

    @staticmethod
    def generate_translated_rectangle(robot_pos, robot_angle, robot_length,
            robot_width, obstacle_length, direction):
        obstacle_points = list()

        translated_center = (
            robot_pos[0] + direction*robot_width*math.cos(math.radians(robot_angle)),
            robot_pos[1] + direction*robot_width*math.sin(math.radians(robot_angle))
        )

        correction_angle = robot_angle - 90
        for sign in [-1, 1]:
            obstacle_points.append([
                translated_center[0] + sign*robot_length*math.cos(math.radians(correction_angle)),
                translated_center[1] + sign*robot_length*math.sin(math.radians(correction_angle))
            ])
        translated_center = (
            translated_center[0] + direction*(obstacle_length+robot_width) *
                math.cos(math.radians(robot_angle)),
            translated_center[1] + direction*(obstacle_length+robot_width) *
                math.sin(math.radians(robot_angle))
        )
        for sign in [-1, 1]:
            obstacle_points.append([
                translated_center[0] + sign*robot_length*math.cos(math.radians(correction_angle)),
                translated_center[1] + sign*robot_length*math.sin(math.radians(correction_angle))
            ])
        return obstacle_points

    @staticmethod
    def is_line_cross_rectangle(xmin, ymin, xmax, ymax, x1, y1, x2, y2):
        """
        Code taken from: https://bitbucket.org/marcusva/py-sdl2/issues/101/liangbarsky-incorrect
        Thanks @schneems.
        """
        dx = x2 - x1 * 1.0
        dy = y2 - y1 * 1.0
        t0 = 0.0
        t1 = 1.0

        checks = ((-dx, -(xmin - x1)),
                  ( dx, xmax - x1),
                  (-dy, -(ymin - y1)),
                  ( dy, ymax - y1))

        for p, q in checks:
            if p == 0 and q < 0:
                return False

            if p != 0:
                r = q / (p * 1.0)

                if p < 0:
                    if r > t1:
                        return False
                    elif r > t0:
                        t0 = r
                else:
                    if r < t0:
                        return False
                    elif r < t1:
                        t1 = r
        return True

    @staticmethod
    def is_point_in_rectangle(xmin, ymin, xmax, ymax, x, y):
        if (xmin < x < xmax) and (ymin < y < ymax):
            return True
        return False

    @staticmethod
    def get_min_max_points(points):
        """
        Get the extremity from rectangle points.
        """
        minx = sys.maxsize
        miny = minx
        maxx = - sys.maxsize
        maxy = maxx
        for p in points:
            if p[0] < minx:
                minx = p[0]
            if p[0] > maxx:
                maxx = p[0]
            if p[1] < miny:
                miny = p[1]
            if p[1] > maxy:
                maxy = p[1]
        return (minx, miny, maxx, maxy)
