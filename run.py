from random import randint


class GameBoard:
    """
    Main game board class. Sets the board size, plants random bombs,
    prints the game instructions. Has methods to uncover the cells,
    to calculate the neighbour cells and to check if the game is won or lost
    """

    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.board = [["  |" for i in range(self.size)]
                      for i in range(self.size)]

    def print_board(self):
        """ Create a representation of the board with squares"""

        # print the column number
        col_no = "  "
        for i in range(self.size):
            col_no = col_no + "   " + str(i+1)
        print(col_no)

        print("    " + "----" * self.size)

        # add the rows with row numbers and the delimitation between them
        for i in range(self.size):
            print(f"{i+1:2} | " + " ".join(self.board[i]))
            print("    " + "----" * self.size)

    def plant_bombs(self):
        """Plant the bombs at a random location """

        planted_bombs = 0

        while planted_bombs < self.bombs:
            position = randint(0, self.size**2)
            row = position // self.size
            col = position % self.size

            if self.board[row][col] == "* |":
                continue
            else:
                self.board[row][col] = "* |"
                planted_bombs += 1 


game = GameBoard(6, 9)
# game.plant_bombs()
game.print_board()
