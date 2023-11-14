from random import randint


class GameBoard:
    """
    Main game board class. Sets the board size, plants random bombs.
    Has methods to calculate the number of neighbouring bombs of a cell,
    to add numbers to cells representing the number of bombs arround,
    to uncover cells, to reveal all the bombs and to check if the game is won
    or lost.
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
        self.revealed = set()
        self.selected_numbers = set()

    def print_board(self):
        """
        Creates a representation of the board with squares.
        """

        # print the column number
        col_no = "  "
        for i in range(self.size):
            col_no = col_no + '  ' + f"{str(i):>2}"
        print(col_no)

        print("    " + "----" * self.size)

        # add the rows with row numbers and the delimitation between them
        for i in range(self.size):
            print(f"{i:2} | " + " ".join(self.visible_board[i]))
            print("    " + "----" * self.size)

    def plant_bombs(self):
        """
        Plants the bombs at a random location.
        """

        planted_bombs = 0

        while planted_bombs < self.bombs:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)

            if self.board[row][col] == "  |":
                self.board[row][col] = "* |"
                planted_bombs += 1

    def neighboring_bombs(self, row, col):
        """
        Identifies number of neighboring bombs.
        """

        bomb_no = 0
        for x in range(max(0, row - 1), min(self.size-1, row + 1)+1):
            for y in range(max(0, col - 1), min(self.size-1, col + 1)+1):
                if x == row and y == col:
                    continue
                if self.board[x][y] == "* |":
                    bomb_no += 1

        return bomb_no

    def add_bomb_number(self):
        """
        Adds number of bombs to all the cells near a bomb.
        If there is no bomb around, a zero is added.
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
        is a bomb and shows all the bombs.Returns True if the cell is not a
        bomb(if it's a number) and reveals the cell. If the number of the cell
        is 0,neighboring cells are recursively checked. The cell that has
        already been opened is stored into a set to check and prevent the loop
        to recur on itself.
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        self.revealed.add((row, col))

        if self.board[row][col] == "* |":
            self.show_bombs()
            return False

        elif self.board[row][col] == "0":
            self.visible_board[row][col] = "0 |"

            # recursion loop logic was inspired from the Youtube tutorial:
            # tutorial link: https://www.youtube.com/watch?v=Fjw7Lc9zlyU
            for x in range(max(0, row - 1), min(self.size-1, row+1)+1):
                for y in range(max(0, col - 1), min(self.size-1, col+1)+1):
                    if (x, y) in self.revealed:
                        continue
                    self.handle_cell(x, y)
            return True

        else:
            # the cell contains a number
            # reveal that cell
            self.visible_board[row][col] = f"{self.board[row][col]} |"
            return True

    def show_bombs(self):
        """
        Shows all bombs if the user hits a bomb. If the cell is not a bomb,
        it updates the user's board with the number of neighbouring bombs.
        """

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == "* |":
                    self.visible_board[r][c] = "* |"
                else:
                    self.visible_board[r][c] = (
                        f"{self.neighboring_bombs(r, c)} |")

    def check_winning(self):
        """
        Checks the winning condition. If the bombs have not been revealed
        and there are no more uncovered no bomb cells on the user's board,
        returns True(the game is won).
        """
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != "* |" and self.visible_board[r][c] == (
                     "  |"):
                    return False
        return True


def choose_level():
    """
    Asks the user to select a number corresponding to a level. Set the size
    of the board and the number of bombs accordingly. Validates the
    user input.
    """

    while True:
        try:
            level = int(input("Select a level: 1.Beginner or 2.Expert\n"
                              "Type 1 or 2:\n"))
            if level == 1:
                GameBoard.size = 9
                GameBoard.bombs = 9
                return GameBoard.size, GameBoard.bombs

            elif level == 2:
                GameBoard.size = 15
                GameBoard.bombs = 35
                return GameBoard.size, GameBoard.bombs

            else:
                print("Invalid level! Type 1 or 2!")

        except ValueError:
            print("Invalid data! You must select a number: 1 or 2.")


def cell_already_revealed(board, row, col):
    """
    Returns True if a cell on the user's board is not empty.
    Helper function used at input validation(if the cell on the board
    is not empty, it means it has already been revealed and can not be
    selected again).
    """
    if board.visible_board[row][col] != "  |":
        return True


def user_input(board):
    """
    Gets the user input and validates the data.If the data can not be converted
    into an integer(it is not a number), or if the same data(coordinates) have
    already been used, or if the data is outside the game board's boundaries,
    an error is raised. If the input is valid, the function returns the data.
    """

    while True:
        try:
            user_row = int(input(f'Select a row (a number from 0 to '
                                 f'{board.size - 1}):\n'))
            if 0 < user_row and user_row >= board.size:
                print(f'Invalid input! Row must be a number between 0 '
                      f'and {board.size - 1}.\n')
                continue

            while True:
                try:
                    user_col = int(input(f'Select a column(a number from 0 to '
                                         f'{board.size - 1}):\n'))
                    if 0 < user_col and user_col >= board.size:
                        print(f'Invalid input! '
                              'Column must be a number between '
                              f'0 and {board.size - 1}.\n')
                        continue

                    if (user_row, user_col) in board.selected_numbers:
                        print('You have already selected these coordinates!\n'
                              'Please select new ones!')
                        print()
                        break

                    if cell_already_revealed(board, user_row, user_col):
                        print('Cell already uncovered!\n'
                              'Please select new cell!')
                        print()
                        break

                    board.selected_numbers.add((user_row, user_col))
                    return user_row, user_col

                except ValueError:
                    print(f'Invalid data! You must enter a number!\n')
                    continue

        except ValueError:
            print(f'Invalid data! You must enter a number!\n')
            continue


def play_game(board):
    """
    Main game loop.
    """

    while True:
        board.print_board()
        row, col = user_input(board)

        if not board.handle_cell(row, col):
            board.print_board()
            print()
            print('Oh nooo! You hit a bomb!:( Better luck next time!')
            print()
            break
        elif board.check_winning():
            print()
            print('Congratulations! You have uncovered all cells! :)')
            print()
            break


def new_game():
    """
    Starts a new game. Sets the board size and bomb numbers according to level.
    Prints the instructions.
    """
    while True:

        print()
        print("--" * 40)
        print("Welcome to MINESWEEPER!")
        print("--" * 40)
        print('Uncover all the cells on the board without hitting any bombs.')
        print()
        print('Choose your level: Beginner(9x9 board, 9 bombs) or Expert'
              '(15x15 board, 35 bombs)')
        print()

        size, bombs = choose_level()
        game = GameBoard(size, bombs)
        play_game(game)


new_game()
