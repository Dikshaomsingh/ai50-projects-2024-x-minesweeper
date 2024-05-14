import itertools
import random
import time


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def nearby_cells(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        neigh_cells = []
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell or i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue

                # Update neigh_cells 
                neigh_cells.append((i, j))
        return neigh_cells

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mine_cells = set()
        if self.count == len(self.cells):
            for cell in self.cells:
                mine_cells.add(cell)

        return mine_cells
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe_cells = set()
        if self.count == 0:
            for cell in self.cells:
                safe_cells.add(cell)
        return safe_cells
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
        
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

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
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        newSelf_knowledge = []
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neigh_cells = Minesweeper(self.height, self.width).nearby_cells(cell)
        neigh_set = set()
        neigh_count = count

        empty_sets = []

        if count == 0:
            for neigh in neigh_cells:
                self.mark_safe(neigh)
        elif len(neigh_cells) == count:
            for neigh in neigh_cells:
                self.mark_mine(neigh)
        else:
            for neigh in neigh_cells:
                if neigh in self.mines:
                    neigh_count = neigh_count - 1
                    continue
                if neigh in self.moves_made or neigh in self.safes:
                    continue
                neigh_set.add(neigh)
            self.knowledge.append(Sentence(neigh_set, neigh_count))
        
        if len(neigh_set):
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:  
                    empty_sets.append(sentence)
                    continue
                if sentence.count == 0 or len(sentence.cells) == sentence.count:
                    for sf in sentence.known_safes():
                        self.mark_safe(sf)
                    for mn in sentence.known_mines():
                        self.mark_mine(mn)  
                    empty_sets.append(sentence)
                else:
                    if neigh_set.issubset(sentence.cells) or neigh_set.issuperset(sentence.cells):
                        newCells = set()
                        if neigh_set.issubset(sentence.cells):
                            newCells = sentence.cells.difference(neigh_set)
                        else:
                            newCells = neigh_set.difference(sentence.cells)
                        if len(newCells):
                            newCount = abs(neigh_count - sentence.count)
                            newSentence = Sentence(newCells, newCount)
                            if len(newCells) == newCount or newCount == 0:
                                for sf in newSentence.known_safes():
                                    self.mark_safe(sf)
                                for mn in newSentence.known_mines():
                                    self.mark_mine(mn)  
                            else:
                                newSelf_knowledge.append(newSentence) 

        
        for sent in empty_sets:
            self.knowledge.remove(sent)
        if len(newSelf_knowledge): 
            self.knowledge += newSelf_knowledge

        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes.difference(self.moves_made):
            if move not in self.mines and move not in self.moves_made:
                return move
            
        return None
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        while len(self.mines) < len(Minesweeper().mines):
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            move = (i, j)
            if move not in self.mines and move not in self.moves_made:
                return move

        return None
        # raise NotImplementedError
