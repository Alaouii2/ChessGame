class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.type = 'human'

    def getcolor(self):
        return self.color

    def score(self, board):
        return board.taken_p[self.color]
