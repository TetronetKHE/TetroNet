class gamestate:
    def __init__(self, staticMatrix, pieceID, rotation, position):
        self.static = staticMatrix  #10x20 matrix
        self.piece = pieceID        #0-6
        self.rotation = rotation    #r 0-3
        self.pos = position         #[x,y] x 0-9 y 0-19
