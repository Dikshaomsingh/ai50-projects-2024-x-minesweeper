import itertools
import random


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

    def nearby_cells(self,cell):
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
                if (i, j) == cell or i<0 or j<0 or i>=self.height or j>=self.width:
                    continue

                # Update neigh_cells 
                neigh_cells.append((i,j))
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
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe_cells = set()
        if self.count == 0 :
            for cell in self.cells:
                safe_cells.add(cell)
        return safe_cells
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
        
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        #raise NotImplementedError


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
        neigh_cells = set(Minesweeper(self.height,self.width).nearby_cells(cell))
        for sentence in self.knowledge:
            for sf in sentence.known_safes():
                print("level2.1: sf:",sf)
                self.mark_safe(sf)
            for mn in sentence.known_mines():
                print("level2.2: mn:",mn)
                self.mark_mine(mn)  


            # if sentence.count == 0:
            #     for cells in sentence.cells:
            #         self.safes.add(cells)
            # elif sentence.count == len(sentence.cells):
            #     for cells in sentence.cells:
            #         self.mines.add(cells)


            # if cell in sentence.cells:
            #     sent = sentence.cells.remove(cell)
            #     print("         ")
            #     print("level2: current cell in sentence.cells removed: new sent:",sent,"cell",cell,sentence.cells)
            #     print("         ")
            #     for sf in sentence.known_safes():
            #         print("level2.1: sf:",sf)
            #         self.mark_safe(sf)
            #     for mn in sentence.known_mines():
            #         print("level2.2: mn:",mn)
            #         self.mark_mine(mn)       
        

        for sentence in self.knowledge:
            if neigh_cells.issubset(sentence.cells) or neigh_cells.issuperset(sentence.cells): 
                newCells = neigh_cells.difference(sentence.cells)
                if len(newCells):
                    newCount = abs(count - sentence.count)
                    newSelf_knowledge.append(Sentence(newCells,newCount)) 
        self.knowledge.append(Sentence(neigh_cells,count))
        
        if len(newSelf_knowledge): 
            self.knowledge += newSelf_knowledge

        #self.knowledge.append(Sentence(newCells,newCount))
        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes.difference(self.moves_made)
        if len(safe_moves):
            move = safe_moves.pop()
            print("         ")
            print("level n: safe move:",move)
            print("         ")
            return move
        else:
            return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i,j) not in self.moves_made and (i,j) not in self.mines:
                return (i,j)

        #raise NotImplementedError
