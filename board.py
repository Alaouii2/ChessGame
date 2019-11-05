import move
import square
import piece
from copy import copy

placeholder = piece.Piece('0')


def opposite_color(color):
    if color == 'b':
        opp = 'w'
    elif color == 'w':
        opp = 'b'
    else:
        opp = '0'
    return opp


class Board:
    def __init__(self):
        self.squares = [[square.Square((i, j), placeholder) for j in range(8)] for i in range(8)]
        self.taken_p = {
            'w': [],
            'b': [],
            '0': []
        }
        self.last_move = None
        self.did_king_move = {
            'w': False, 'b': False
        }
        self.did_rook_move = {
            'w': [False, False], 'b': [False, False]
        }
        self.promotion = False

    def append_piece(self, p, i, j):
        self.squares[i][j].p = p

    def initiate(self):
        self.append_piece(piece.Rook('b'), 0, 0)
        self.append_piece(piece.Knight('b'), 0, 1)
        self.append_piece(piece.Bishop('b'), 0, 2)
        self.append_piece(piece.Queen('b'), 0, 3)
        self.append_piece(piece.King('b'), 0, 4)
        self.append_piece(piece.Bishop('b'), 0, 5)
        self.append_piece(piece.Knight('b'), 0, 6)
        self.append_piece(piece.Rook('b'), 0, 7)
        self.append_piece(piece.Pawn('b'), 1, 0)
        self.append_piece(piece.Pawn('b'), 1, 1)
        self.append_piece(piece.Pawn('b'), 1, 2)
        self.append_piece(piece.Pawn('b'), 1, 3)
        self.append_piece(piece.Pawn('b'), 1, 4)
        self.append_piece(piece.Pawn('b'), 1, 5)
        self.append_piece(piece.Pawn('b'), 1, 6)
        self.append_piece(piece.Pawn('b'), 1, 7)
        self.append_piece(piece.Rook('w'), 7, 0)
        self.append_piece(piece.Knight('w'), 7, 1)
        self.append_piece(piece.Bishop('w'), 7, 2)
        self.append_piece(piece.Queen('w'), 7, 3)
        self.append_piece(piece.King('w'), 7, 4)
        self.append_piece(piece.Bishop('w'), 7, 5)
        self.append_piece(piece.Knight('w'), 7, 6)
        self.append_piece(piece.Rook('w'), 7, 7)
        self.append_piece(piece.Pawn('w'), 6, 0)
        self.append_piece(piece.Pawn('w'), 6, 1)
        self.append_piece(piece.Pawn('w'), 6, 2)
        self.append_piece(piece.Pawn('w'), 6, 3)
        self.append_piece(piece.Pawn('w'), 6, 4)
        self.append_piece(piece.Pawn('w'), 6, 5)
        self.append_piece(piece.Pawn('w'), 6, 6)
        self.append_piece(piece.Pawn('w'), 6, 7)

    def execute(self, m):
        start = copy(m.start)
        finish = copy(m.finish)
        kingside = m.king_side_castling()
        queenside = m.queen_side_castling()
        self.taken_p.get(opposite_color(finish.p.color)).append(finish.p)
        self.append_piece(start.p, *finish.coord)
        self.append_piece(placeholder, *start.coord)
        if m.en_passant:
            if finish.p.color == 'w':
                self.taken_p[finish.p.color].append(self.squares[finish.x + 1][finish.y].p)
                self.append_piece(placeholder, finish.x + 1, finish.y)
            else:
                self.taken_p.get(opposite_color(finish.p.color)).append(self.squares[finish.x - 1][finish.y].p)
                self.append_piece(placeholder, finish.x - 1, finish.y)
        if start.p.name == 'p':
            if (start.x == 6 and finish.x == 7) or (start.x == 1 and finish.x == 0):
                self.promotion = True
        if kingside:
            sqs = copy(self.squares[m.start.x][7])
            sqf = copy(self.squares[m.start.x][5])
            self.append_piece(sqs.p, *sqf.coord)
            self.append_piece(placeholder, *sqs.coord)
            self.last_move = [start, finish, sqs, sqf]
        elif queenside:
            sqs = copy(self.squares[m.start.x][0])
            sqf = copy(self.squares[m.start.x][3])
            self.append_piece(sqs.p, *sqf.coord)
            self.append_piece(placeholder, *sqs.coord)
            self.last_move = [start, finish, sqs, sqf]
        else:
            self.last_move = [start, finish]
        if start.p.name == 'k':
            if start.p.color == 'w':
                self.did_king_move['w'] = True
            else:
                self.did_king_move['b'] = True
        if start.p.name == 'r':
            if start.p.color == 'w':
                if start.y < 3:
                    self.did_rook_move['w'][0] = True
                else:
                    self.did_rook_move['w'][1] = True
            else:
                if start.y < 3:
                    self.did_rook_move['b'][0] = True
                else:
                    self.did_rook_move['b'][1] = True

    def update(self, m):
        self.execute(m)
        if self.promotion:
            p = piece.Queen(m.finish.p.color)
            self.last_move.append(p.color)
            self.append_piece(p, *m.finish.coord)
            self.promotion = False
        print(self)
        print(len(self.last_move))

    def allmoves(self, color, pos=None):
        l = []
        if not pos:
            for row in self.squares:
                for s in row:
                    if s.p.color == color:
                        for li in self.squares:
                            for e in li:
                                m = move.Move(self, s.coord, e.coord)
                                if m.is_legal():
                                    l.append(m)
        else:
            s = self.squares[pos[0]][pos[1]]
            for li in self.squares:
                for e in li:
                    m = move.Move(self, s.coord, e.coord)
                    if m.is_legal():
                        l.append(m)
        return l

    def range(self, color):
        l = set()
        for row in self.squares:
            for s in row:
                if s.p.color == color:
                    for li in self.squares:
                        for e in li:
                            m = move.Move(self, s.coord, e.coord)
                            m.is_possible()
                            if m.taking:
                                l.add(m.finish)
        return l

    def track_king(self, color):
        for row in self.squares:
            for s in row:
                if s.p.name == 'k' and s.p.color == color:
                    return s

    def check(self, color):
        if self.track_king(color) in self.range(opposite_color(color)):
            return True
        return False

    def stalemate(self, color):
        if (not self.check(color)) and self.allmoves(color) == []:
            return True
        return False

    def checkmate(self, color):
        if self.check(color) and self.allmoves(color) == []:
            return True
        return False

    def __repr__(self):
        look = ''
        for row in self.squares:
            for square in row:
                look += str(square.p) + '\t'
            look += '\n'

        return look
