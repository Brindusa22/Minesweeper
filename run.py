
class GameBoard:
    """
    Main game board class. Sets the board size, plants random bombs,
    prints the game instructions. Has methods to uncover the cells,
    to calculate the neighbour cells and to check if the game is won or lost
    """

    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.board = [["." for x in range(size)] for y in range(size)]
        
    def print_board(self):
        for row in self.board:
            print(" ".join(row))
            

game = GameBoard(8, 4)
game.print_board()