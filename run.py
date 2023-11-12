from random import randint


class GameBoard:
    """
    Main game board class. Sets the board size, plants random bombs.
    Has methods to uncover the cells,
    to calculate the neighbouring cells and to check if the game is won or lost
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
        """ Create a representation of the board with squares"""

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
        for x in range(max(0, row - 1), min(self.size-1, row + 1)+1):
            for y in range(max(0, col - 1), min(self.size-1, col + 1)+1):
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
        (if it's a number) and reveal the cell. If the number of the cell is 0,
        neighboring cells are recursively checked. The cell that has already 
        been opened is stored into a set to check and prevent the loop to recur
        on itself
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


def choose_level():
    """
    Ask the user to select a number corresponding to a level. Set the size
    of the board and the number of bombs accordingly. Validate the
    user input.
    """

    while True:
        try:
            level = int(input("Select a level: 1.Beginner or 2.Exepert\n"
                              "Type 1 or 2:\n"))
            if level == 1:
                GameBoard.size = 9
                GameBoard.bombs = 9
                return GameBoard.size, GameBoard.bombs

            elif level == 2:
                GameBoard.size = 15
                GameBoard.bombs = 15
                return GameBoard.size, GameBoard.bombs

            else:
                print("Invalid level! Type 1 or 2!")

        except ValueError:
            print("Invalid data! You must select a number: 1 or 2") 


def user_input(board):
    """
    Get the user input and validate the data. If the data can not be converted
    into an integer(it is not a number), or if the same data(coordinates) have
    already been used, or if the data is outside the game board's boundaries an
    error is raised. If the input is valid, the function returns the data.
    """

    while True:
        try:
            user_row = int(input(f'Select a row (a number from 0 to '
                                 f'{board.size - 1}):\n'))
            if 0 < user_row and user_row >= board.size:
                print(f'Invalid input. Row must be a number between 0 '
                      f'and {board.size - 1}.\n')
                continue

            while True:
                try:
                    user_col = int(input(f'Select a column(a number from 0 to '
                                         f'{board.size - 1}): \n'))
                    if 0 < user_col and user_col >= board.size:
                        print(f'Invalid input. Column must be a number between'
                              f'0 and {board.size - 1}.\n')
                        continue

                    if (user_row, user_col) in board.selected_numbers:
                        print('You have already selected these coordinates!\n'
                              'Please select new ones!')
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
            print('Oh nooo! You hit a bomb!:( Better luck next time!')
            print()
            break
        elif board.check_winning():
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
              '(15x15 board, 15 bombs)')
        print()

        size, bombs = choose_level()
        game = GameBoard(size, bombs)
        play_game(game)


new_game()