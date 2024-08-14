import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation.
    Handles the setup of the board, placement of mines, and
    provides methods to interact with the board.
    """

    def __init__(self, height=8, width=8, mines=8):
        """
        Initialize the Minesweeper board with the specified dimensions
        and randomly place the specified number of mines.
        """
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines (all cells set to False)
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)  # False indicates no mine at this cell
            self.board.append(row)

        # Randomly place the mines on the board
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:  # Place mine only if cell is currently empty
                self.mines.add((i, j))
                self.board[i][j] = True  # True indicates a mine at this cell

        # Initially, the player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation of the board,
        showing where the mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")  # X indicates a mine
                else:
                    print("| ", end="")  # Empty space indicates no mine
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        """
        Returns True if the given cell contains a mine, else False.
        """
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are within one row and column
        of a given cell, not including the cell itself.
        """

        # Initialize the mine count to 0
        count = 0

        # Loop over all cells within one row and column around the given cell
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Count the cell if it is within bounds and contains a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if the player has won the game by finding all mines.
        Returns True if all mines have been found, else False.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells and a count of the number of those cells that are mines.
    """

    def __init__(self, cells, count):
        """
        Initialize a new Sentence with a set of cells and a count of mines.
        """
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        """
        Compare two sentences for equality based on their cells and count.
        """
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """
        String representation of a Sentence (e.g., "{A1, A2, A3} = 2").
        """
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        If the number of cells is equal to the count, all cells must be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        If the count is zero, all cells must be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates the sentence by marking a specific cell as a mine.
        Decreases the count by 1 since one mine is identified.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates the sentence by marking a specific cell as safe.
        The cell is removed from the set but does not affect the count.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player.
    The AI keeps track of the game state and applies logic to deduce safe moves.
    """

    def __init__(self, height=8, width=8):
        """
        Initialize the AI with the size of the Minesweeper board.
        """
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine and updates all knowledge
        to reflect this fact.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe and updates all knowledge
        to reflect this fact.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given safe cell,
        how many neighboring cells have mines in them.

        This function:
            1) Marks the cell as a move that has been made.
            2) Marks the cell as safe.
            3) Adds a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`.
            4) Marks any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base.
            5) Adds any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge.
        """
        # Step 1: Mark the move as made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe
        self.mark_safe(cell)

        # Step 3: Determine which neighboring cells are unknown and how many are mines
        cells_to_check = []
        count_mines = 0

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # If this neighboring cell is a known mine, adjust the mine count
                if (i, j) in self.mines:
                    count_mines += 1
                # If the cell is within bounds, not known to be safe or a mine, add it to cells_to_check
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) not in self.safes and (
                i, j) not in self.mines:
                    cells_to_check.append((i, j))

        # Create a new sentence from the cells to check and the number of mines around the original cell
        new_sentence = Sentence(cells_to_check, count - count_mines)
        self.knowledge.append(new_sentence)

        # Step 4: Update knowledge with any new information about mines or safe cells
        for sentence in self.knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

        # Step 5: Infer new sentences based on the current knowledge base
        for sentence in self.knowledge:
            # If new_sentence is a subset of an existing sentence, create a new sentence based on the difference
            if new_sentence.cells.issubset(
                    sentence.cells) and sentence.count > 0 and new_sentence.count > 0 and new_sentence != sentence:
                new_subset = sentence.cells.difference(new_sentence.cells)
                new_sentence_subset = Sentence(list(new_subset), sentence.count - new_sentence.count)
                self.knowledge.append(new_sentence_subset)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already made.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None  # No safe move found

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board by choosing randomly
        among cells that have not been chosen and are not known to be mines.
        """
        possible_moves = []
        for i in range(self.width):
            for j in range(self.height):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))

        if possible_moves:
            return random.choice(possible_moves)
        else:
            return None  # No moves available
