class Result(object):

    def __init__(self, top=None, bottom=None, left=None, right=None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        if not(top is None & bottom is None & left is None & right is None):
            self.center = (int(left + (right - left) / 2), int(top + (bottom - top) / 2))

    def __eq__(self, other):
        return self.top == other & self.bottom == other & self.left == other & self.right == other & self.center == other


class Group(object):

    def __init__(self, top=None, bottom=None, left=None, right=None):
        self.points = 0
        self.position = Result(top, bottom, left, right)

    def __eq__(self, other):
        return self.position == other


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
