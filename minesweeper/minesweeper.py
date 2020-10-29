import itertools
import random
import copy
import termcolor

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
        if len(self.cells) == self.count:
            return self.cells
        return set()



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return None  #no need to update the count as safe cell does not contain mines


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
    def neighbor(self,cell):
        # Keep count of nearby mines
        count = 0
        neighbors =set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell or (i,j) in self.moves_made:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i,j) in self.mines:
                        count += 1
                    elif (i,j) in self.safes:
                        continue
                    else:
                        neighbors.add((i,j))



        return neighbors,count
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
        #1 mark as move
        self.moves_made.add(cell)
        #2 mark as safe
        self.safes.add(cell)
        #3 add a news sentence to ai's knowledge base
        #for that first explore neighbor cells and get count
        neighbor_cell,detected_mines=self.neighbor(cell)
        #update mines
        count -= detected_mines

        #create new sentence
        nw_sentence  = Sentence(neighbor_cell,count)
        if nw_sentence not in self.knowledge:
            self.knowledge.append(nw_sentence)
        #4
        for sentence in self.knowledge:
            #get known_safes cell
            safes_cell =copy.deepcopy( sentence.known_safes())
            for cell in safes_cell:
                self.mark_safe(cell)
            #get mines cell
            mines_cell =copy.deepcopy(sentence.known_mines())
            for cell in mines_cell:
                self.mark_mine(cell)
        #5
        #copying kb
        known_sentences = copy.deepcopy(self.knowledge)
        for sentenc1 in known_sentences:
            known_sentences.remove(sentenc1)
            for sentence2 in known_sentences:
                ls2 = len(sentence2.cells)
                ls1 = len(sentenc1.cells)
                if ls2==ls1 :
                    continue
                elif ls2 < ls1 and ls2 != 0 and ls1 !=0:
                    subset = sentence2.cells
                    bigset =sentenc1.cells
                    diff_set =bigset-subset
                    diff_count = sentenc1.count -sentence2.count
                    if len(diff_set) == 1:
                        if diff_count == 0: #means the cells is safe
                            cell = diff_set.pop()
                            self.mark_safe(cell)

                        if diff_count == 1: #means mines
                            cell  = diff_set.pop()
                            self.mark_mine(cell)
                    else:
                        #add new knowledge to knowledge base
                        self.knowledge.append(Sentence(diff_set,diff_count))



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move  in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        potential_move = list()
        for row in range(self.width):
            for col in range(self.height):
                if (row,col) not in  self.moves_made:
                    potential_move.append((row,col))
        if len(potential_move) == 0:
            termcolor.cprint(f"Games is over. Pressed reset button to play again","red")
        else :
            return random.choice(potential_move)
