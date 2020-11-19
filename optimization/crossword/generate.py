import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()

        # print("before", self.domains)

        self.ac3()

        # print("after", self.domains)

        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for slot_variable in self.crossword.variables:
            for word_value in self.crossword.words:
                if slot_variable.length != len(word_value):
                    self.domains[slot_variable].remove(word_value)

    def revise(self, slot_variable_x, slot_varibale_y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        """ raise NotImplementedError """

        conflict_words = []

        overlap_position = self.crossword.overlaps[slot_variable_x,
                                                   slot_varibale_y]

        if overlap_position is None:
            return False
        else:
            v1th_char_pos, v2th_char_pos = overlap_position

        # loop through possible words for slot var x e.g. 1
        for x_word in self.domains[slot_variable_x]:
            overlaps = False

            # loop through possible words for slot var y e.g. 2
            for y_word in self.domains[slot_varibale_y]:
                if x_word != y_word and x_word[v1th_char_pos] == y_word[v2th_char_pos]:
                    overlaps = True
                    break

            if not overlaps:
                conflict_words.append(x_word)

        for word in conflict_words:
            self.domains[slot_variable_x].remove(word)

        return len(conflict_words) > 0

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # no args given => aggretage arcs
        if arcs is None:
            arcs = []
            for slot_variable_x in self.crossword.variables:
                # loop through neighbors
                for slot_variable_y in self.crossword.neighbors(slot_variable_x):
                    arcs.append((slot_variable_x, slot_variable_y))

        while arcs:
            arc = arcs.pop(0)
            slot_variable_x, slot_variable_y = arc[0], arc[1]

            # enforce slot_variable arc-consistency
            if self.revise(slot_variable_x, slot_variable_y):

                # no solution for empty domain
                if len(self.domains[slot_variable_x]) == 0:
                    return False

                # appending neighbor-arcs for changed domain
                for neighbor in self.crossword.neighbors(slot_variable_x) - {slot_variable_y}:
                    arcs.append((neighbor, slot_variable_x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        crossword_variables = set(self.crossword.variables)
        assignment_keys = set(assignment.keys())

        # print("assignment_complete", crossword_variables, assignment_keys)

        if assignment_keys == crossword_variables:
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        keys = assignment.keys()
        items = assignment.items()

        # print("assignment-items", items)

        # check if value mapping distinct
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2 and assignment[v1] == assignment[v2]:
                    return False

        # check for correct word length
        for variable, word in items:
            if variable.length != len(word):
                return False

        # check for neighbor conflicts
        for variable, word in items:
            for neighbor in self.crossword.neighbors(variable).intersection(keys):
                overlap = self.crossword.overlaps[variable, neighbor]
                if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        return self.domains[var]  # tbd

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # completed
        if self.assignment_complete(assignment):
            return assignment

        slot_variable = self.select_unassigned_variable(assignment)

        for word_value in self.order_domain_values(slot_variable, assignment):
            assignment_copy = copy.deepcopy(assignment)
            # assign
            assignment_copy[slot_variable] = word_value

            if self.consistent(assignment):
                assignment[slot_variable] = word_value
                result = self.backtrack(assignment)

                if result is not None:
                    return result
            assignment.pop(slot_variable, None)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
