class Result(object):

    def __init__(self, top=None, bottom=None, left=None, right=None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        if not(top is None and bottom is None and left is None and right is None):
            self.center = Point(float(left + (right - left) / 2), float(top + (bottom - top) / 2))
        else:
            self.center = Point(None, None)

    def __eq__(self, other):
        return self.top == other or self.bottom == other or self.left == other or self.right == other or self.center == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_none(self) -> bool:
        return self.top is None or self.bottom is None or self.left is None or self.right is None or self.center is None

    def nis_none(self) -> bool:
        return not self.is_none()

    def setPosition(self, top: float, bottom: float, left: float, right: float):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.center = Point(left + (right - left) / 2, top + (bottom - top) / 2)


class Group(object):

    def __init__(self, top=None, bottom=None, left=None, right=None):
        self.points = 0
        self.position = Result(top, bottom, left, right)

    def __eq__(self, other):
        return self.position == other

    def is_none(self) -> bool:
        return self.position.is_none()

    def nis_none(self) -> bool:
        return not self.is_none()


class Point(object):

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def is_none(self) -> bool:
        return self.x is None or self.y is None

    def nis_none(self) -> bool:
        return not self.is_none()

    def to_list(self) -> list():
        return self.x, self.y
