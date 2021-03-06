import numpy as np
import random


class Board:
    """Represents the tic-tac-toe board. This includes: board display,
    board state calculation, and board updates. 

    Attributes
    ----------
    dim: int
      The dimension of the board. In tic-tac-toe this is a 3x3 board.

    board_space: np.array[np.array[int]]
      The current state of the board.

    current_player: int
      The current player who can make a turn. 1 is for X and 2 is for O.
    """

    def __init__(self):
        self.dim = 3
        self.reset_board()

    def reset_board(self):
        """Resets the board and the player who's turn it is to the inital values for a new game
        """
        self.current_player = 1
        self.board_space = np.zeros((self.dim, self.dim), dtype=int)

    def play_turn(self, state):
        """Sets its board_space to the given state and updates the current player.

        Parameters
        ----------
        state: np.array[np.array[int]]
          The new board state to transition to.
        """
        self.board_space = state
        self.current_player = 1 if self.current_player is 2 else 2

    def calculate_board(self, coord):
        """From the current state and action, return the remaining state of the board
        Parameters
        ----------
        coord: tuple(int,int)
          coordinate representing a potential move of the players

        Return
        ------
        board: np.array[np.array[int]]
          Returns a copy of the board representing the possible state given the action
        """
        board = np.copy(self.board_space)
        x, y = coord
        board[x, y] = self.current_player
        return board

    def generate_slices(self, board):
        """Takes the current board space and creates all slices of rows, columns, and diagonals.

        Return
        ------
        board_slices: np.array[np.array[int]]
          Slices of the board representing rows, columns, and diagonals
        """
        row_slices = np.copy(board)
        col_slices = np.transpose(np.copy(board))
        diag_slices_one = np.diagonal(np.copy(board))
        diag_slices_two = np.diagonal(
            np.flip(np.copy(board), axis=0))

        board_slices = np.vstack(
            (row_slices, col_slices, [diag_slices_one], [diag_slices_two]))
        return board_slices

    def tie_game(self, board):
        return False if 0 in board else True

    def end_of_game(self, board):
        """Determines if the game is over whether by tie or there is a winner

        Return
        ------
        game_over: int
          int to signify if the game is still going (0) or if it is over
          (1) for X's win and (2) for O's win
        """

        def all_same_player(board_slice):
            """Determines if the slice from the board is all from the same player

                Parameters
                ----------
                board_slice: np.array[int]
                  Slice of the board that is either a row, column, or diagonal represented by integer values of
                  0, 1, or 2 depending on the player moves.
                  If they are all the same, then there is a winner.

                Return
                ------
                : int
                  Indicates if there is a winner by returning 1 for X, 2 for O, and 0 for no winner.
                """
            if np.array_equal(board_slice, [1, 1, 1]):
                return 1
            elif np.array_equal(board_slice, [2, 2, 2]):
                return 2
            else:
                return 0

        board_slices = self.generate_slices(board)
        slice_values = [all_same_player(s) for s in board_slices]
        if 1 in slice_values:
            return 1
        elif 2 in slice_values:
            return 2
        else:
            return 0

    def potential_next_states(self):
        """Determines what states can be entered next given the current state of the board
        and the current player. The states returned are represented as a board_state which
        is just a 2D np.array.

        Returns
        -------
        next_states: 3D np.array
          The potential next states we can enter from the current state. Outer dimension
          is all possible states, and the inner two dimensions are the states themselves.
        """
        x_coords, y_coords = np.where(self.board_space == 0)
        next_states = [self.calculate_board(coord)
                       for coord in zip(x_coords, y_coords)]
        return next_states

    def display(self):
        """Displays the current state of the board using ASCII art. 

        X | X | X
        - | - | -
        O | O | O
        - | - | -
        X | X | X

        Returns
        -------
        board_display: str
          The string representation of the board in the given state.
        """
        value_markers = {0: " ", 1: "X", 2: "O"}
        row_separator = "".join(["-", "|", "-", "|", "-"]) + "\n"

        def display_row(row):
            """Displays the contents of a single row separated by |

            X | X | X

            Parameters
            ----------
            row: np.array[int]
              A single row of the overall board.

            Returns
            -------
            : str
              The string representation of the row.
            """
            return "|".join([value_markers[i] for i in row]) + "\n"

        board_display = row_separator.join(
            [display_row(r) for r in self.board_space])
        return board_display
