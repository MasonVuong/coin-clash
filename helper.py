import sys, os, math

class Helper:
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def targeting(x1, y1, x2=-1, y2=-1, speed=-1):
        if x2 == -1:
            diff_x = x1
            diff_y = y1
        else:
            diff_x = x1 - x2
            diff_y = y1 - y2
        distance = (diff_x ** 2 + diff_y ** 2) ** .5
        if speed == -1:
             return distance
        speed_x = diff_x * speed / distance
        speed_y = diff_y * speed / distance
        return [distance, speed_x, speed_y]

    @staticmethod
    def offset_targeting(speed_x, speed_y, range=-1, offset=None):
        theta = math.atan2(-speed_y, speed_x) * 180 / math.pi % 360
        if range == -1:
            return theta
        return [theta, range * math.cos((theta + offset) * math.pi / 180), -range * math.sin((theta + offset) * math.pi / 180)]
        