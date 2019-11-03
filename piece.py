class Piece:
    def __init__(self, color):
        try:
            self.color = color
        except color not in ['w', 'b', '0']:
            print('invalid color')
        self.name = '0'
        self.value = 0

    def __repr__(self):
        return self.color + self.name


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = 'p'
        self.value = 1


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = 'r'
        self.value = 5


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = 'c'
        self.value = 3


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = 'b'
        self.value = 3.5


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = 'q'
        self.value = 10


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.name = 'k'
        self.value = 255
