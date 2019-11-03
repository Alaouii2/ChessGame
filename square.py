class Square:
    def __init__(self, coord, p):
        self.coord = self.x, self.y = coord
        self.p = p
        self.is_attacked = False

    def __repr__(self):
        return '{} ({}, {})'.format(self.p, self.x, self.y)