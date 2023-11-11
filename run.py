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
        self.visible_board = [["  |" for i in range(self.size)]
                              for i in range(self.size)]
        self.plant_bombs()
        self.add_bomb_number()

    def print_board(self):
        """ Create a representation of the board with squares"""

        # print the column number
        col_no = "  "
        for i in range(self.size):
            col_no = col_no + "   " + str(i)
        print(col_no)

        print("    " + "----" * self.size)

        # add the rows with row numbers and the delimitation between them
        for i in range(self.size):  
            print(f"{i:2} | " + " ".join(self.visible_board[i]))
            print("    " + "----" * self.size)

    def plant_bombs(self):
        """Plant the bombs at a random location """

        planted_bombs = 0

        while planted_bombs < self.bombs:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)

            if self.board[row][col] == "  |":
                self.board[row][col] = "* |"
                planted_bombs += 1

    def neighboring_bombs(self, row, col):
        """ Identify number of neighboring bombs """

        bomb_no = 0
        for x in range(max(0, row - 1), min(self.size-1, row + 2)):
            for y in range(max(0, col - 1), min(self.size-1, col + 2)):
                if x == row and y == col:
                    continue
                if self.board[x][y] == "* |":
                    bomb_no += 1

        return bomb_no

    def add_bomb_number(self):
        """
            Add number of bombs to all the cells near a bomb.
            If there is no bomb around, the cell remains empty.
        """

        bomb_no = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == "* |":
                    continue
                bomb_no = self.neighboring_bombs(x, y)

                if bomb_no > 0:
                    self.board[x][y] = f"{ bomb_no}"
                else:
                    self.board[x][y] = "0"

    def handle_cell(self, row, col):
        """
        Checks the content of cells. Returns False if the content
        is a bomb and show all the bombs. Return True if the cell is not a bomb
        (if it's a number or an empty cell) and reveal the cell. If the cell is
        empty, neighboring cells are recursively checked.
        """   
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        if self.board[row][col] == "* |":
            self.show_bombs()
            return False

        elif self.board[row][col] == "  |":
            self.visible_board[row][col] = f"{self.neighboring_bombs(row, col)}"
            if self.neighboring_bombs(row, col) == "0":
                for x in range(max(0, row - 1), min(self.size-1, row+2)):
                    for y in range(max(0, col - 1), min(self.size-1, col+2)):
                        self.handle_cell(x, y)
                return True

        else:
            # the cell contains a number
            # reveal that cell
            self.visible_board[row][col] = f"{self.board[row][col]} |"
            return True

    def show_bombs(self):
        """
        Show all bombs if the user hit a bomb.
        """
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == "* |":
                    self.visible_board[r][c] = "* |"
                else:
                    self.visible_board[r][c] = f"{self.neighboring_bombs(r, c)} |"

    def check_winning(self):

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != "* |" and self.visible_board[r][c] == "  |":
                    return False          
        return True


def user_input(board):
    """
    Get the user input and validate the data. If the data can not be converted
    into an integer or if the data is outside the game board's boundaries an 
    error is raised. If the input is valid, the function returns the data.
    """
    while True:
        try:
            user_row = int(input('Select a row (a number from 0 to 9):\n'))
            if 0 < user_row and user_row > board.size:
                print('Invalid input. Row must be a number between 0 and 9.\n')
                continue

            while True:
                try:
                    user_col = int(input('Select a column (a number from 0 to 9):\n'))
                    if 0 < user_col and user_col > board.size:
                        print('Invalid input. Column must be a number between 0 and 9.\n')
                        continue

                    return user_row, user_col

                except ValueError as e:
                    print(f'Invalid data: {e}, please try again.\n')
                    continue

        except ValueError as e:
            print(f'Invalid data: {e}, please try again.\n')
            continue


def play_game(board):

    while True:
        board.print_board()
        row, col = user_input(board)

        if not board.handle_cell(row, col):
            board.print_board()
            print('Sorry! You Lost')
            break
        elif board.check_winning():
            print('Congratulations')
            break


game = GameBoard(9, 9)
play_game(game)