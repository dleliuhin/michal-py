
class Result(object):

    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.center = (int(left + (right - left) / 2), int(top + (bottom - top) / 2))


class Group(object):

    def __init__(self, top, bottom, left, right):
        self.points = 0
        self.position = Result(top, bottom, left, right)