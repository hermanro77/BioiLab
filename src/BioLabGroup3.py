from pprint import pprint

class Tile:

    def __init__(self, x, y, value, pointers=[]):
        self.x = x
        self.y = y
        self.value = value
        self.pointers = pointers

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

class Board:

    def __init__(self, string1, string2, gap_pen):
        self.string1 = string1
        self.string2 = string2
        self.gap_pen = gap_pen
        self.cols = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
        self.rows = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
        self.BLOSSUM50 = "5 -2 -1 -2 -1 -1 -1 0 -2 -1 -2 -1 -1 -3 -1 1 0 -3 -2 0 " \
                        "-2 7 -1 -2 -4 1 0 -3 0 -4 -3 3 -2 -3 -3 -1 -1 -3 -1 -3 " \
                        "-1 -1 7 2 -2 0 0 0 1 -3 -4 0 -2 -4 -2 1 0 -4 -2 -3 " \
                        "-2 -2 2 8 -4 0 2 -1 -1 -4 -4 -1 -4 -5 -1 0 -1 -5 -3 -4 " \
                        "-1 -4 -2 -4 13 -3 -3 -3 -3 -2 -2 -3 -2 -2 -4 -1 -1 -5 -3 -1 " \
                        "-1 1 0 0 -3 7 2 -2 1 -3 -2 2 0 -4 -1 0 -1 -1 -1 -3 " \
                        "-1 0 0 2 -3 2 6 -3 0 -4 -3 1 -2 -3 -1 -1 -1 -3 -2 -3 " \
                        "0 -3 0 -1 -3 -2 -3 8 -2 -4 -4 -2 -3 -4 -2 0 -2 -3 -3 -4 " \
                        "-2 0 1 -1 -3 1 0 -2 10 -4 -3 0 -1 -1 -2 -1 -2 -3 2 -4 " \
                        "-1 -4 -3 -4 -2 -3 -4 -4 -4 5 2 -3 2 0 -3 -3 -1 -3 -1 4 " \
                        "-2 -3 -4 -4 -2 -2 -3 -4 -3 2 5 -3 3 1 -4 -3 -1 -2 -1 1 " \
                        "-1 3 0 -1 -3 2 1 -2 0 -3 -3 6 -2 -4 -1 0 -1 -3 -2 -3 " \
                        "-1 -2 -2 -4 -2 0 -2 -3 -1 2 3 -2 7 0 -3 -2 -1 -1 0 1 " \
                        "-3 -3 -4 -5 -2 -4 -3 -4 -1 0 1 -4 0 8 -4 -3 -2 1 4 -1 " \
                        "-1 -3 -2 -1 -4 -1 -1 -2 -2 -3 -4 -1 -3 -4 10 -1 -1 -4 -3 -3 " \
                        "1 -1 1 0 -1 0 -1 0 -1 -3 -3 0 -2 -3 -1 5 2 -4 -2 -2 " \
                        "0 -1 0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1 2 5 -3 -2 0 " \
                        "-3 -3 -4 -5 -5 -1 -3 -3 -3 -3 -2 -3 -1 1 -4 -4 -4 15 2 -3 " \
                        "-2 -1 -2 -3 -3 -1 -2 -3 2 -1 -1 -2 0 4 -3 -2 -2 2 8 -1 " \
                        "0 -3 -3 -4 -1 -3 -3 -4 -4 4 1 -3 1 -1 -3 -2 0 -3 -1 5"
        self.BLOSSUM50_MATRIX = list(map(int, self.BLOSSUM50.split(" ")))

    #makes the board and calculates scores based on BLOSSUM50, input strings and gap penalty
    def makeboard(self):
        board = []

        for i in range(len(self.string2) + 1):
            row = []
            for j in range(len(self.string1) + 1):

                if j == 0 or i == 0:
                    row.append(Tile(i, j, 0))
                else:
                    sum1 = self.get_score_from_matrix(self.string1[j-1], self.string2[i-1]) + board[i-1][j-1].value
                    sum2 = board[i-1][j].value + self.gap_pen
                    sum3 = row[j-1].value + self.gap_pen

                    sums = [sum1, sum2, sum3]
                    maxes = [i for i, x in enumerate(sums) if x == max(sums)]
                    if self.all_negative_numbers(sums):
                        row.append(Tile(i, j, 0))
                    else:
                        li = []
                        for ma in maxes:
                            if ma == 0:
                                li.append((i-1, j-1))
                            elif ma == 1:
                                li.append((i-1, j))
                            elif ma == 2:
                                li.append((i, j-1))

                        row.append(Tile(i, j, max(sums), li))

            board.append(row)
        return board

    #Checks if all numbers in values are negative
    def all_negative_numbers(self, values):
        b = True
        for val in values:
            if val >= 0:
                b = False
        return b

    #gets the score from to characters in th blossum50 matrix
    def get_score_from_matrix(self, char1, char2):
        m = [self.BLOSSUM50_MATRIX[i:i + len(self.rows)] for i in range(0, len(self.BLOSSUM50_MATRIX), len(self.rows))]
        if isinstance(char1, int) and isinstance(char2, int):
            return m[char2][char1]

        return m[self.cols.index(char2)][self.rows.index(char1)]

    #starts at starting_tile_value and traces back and returns a result list with coupled letters, and it's scores
    def traceback(self, board, all_possible_alignments, starting_tile_val):
        results = []
        scores = []

        for li in board:
            for tile in li:

                #makes sure we get all the paths that starts with the tile with the highest value
                if (len(tile.pointers) > 0 and all_possible_alignments) or (starting_tile_val == tile.value and not all_possible_alignments):
                    scores.append(tile.value)
                    current_tile = tile
                    sequencing = [(self.string2[current_tile.x - 1], self.string1[current_tile.y - 1])]

                    #as long as the current tile in the chain has pointers we coninue adding letters to sequencing
                    while len(current_tile.pointers) > 0: #TODO: handle more than one pointer
                        letters = self.get_letters_from_pointer(current_tile, current_tile.pointers[0])
                        if letters:
                            sequencing.append(letters)
                        current_tile = board[current_tile.pointers[0][0]][current_tile.pointers[0][1]]

                    if len(sequencing) > 0:
                        results.append(list(reversed(sequencing)))

        return results, list(reversed(scores))




    #Returns a tuple of two letters based on current tile and pointer index
    def get_letters_from_pointer(self, current_tile, xy_pointer_index):
        if current_tile.x == xy_pointer_index[0]:
            return ("-", self.string2[xy_pointer_index[0] - 1])

        elif current_tile.y == xy_pointer_index[1]:
            return (self.string1[xy_pointer_index[1] - 1], "-")


        elif board[xy_pointer_index[0]][xy_pointer_index[1]].value > 0:
            return (self.string1[xy_pointer_index[1] - 1], self.string2[xy_pointer_index[0] - 1])

        else:
            return None

    #Finds all the optimal alignments
    def find_optimal_local_alignment(self, board):
        optimal_score = 0
        for li in board:
            for tile in li:
                if tile.value > optimal_score:
                    optimal_score = tile.value

        return self.traceback(board, False, optimal_score)

    #dont use
    def find_all_possible_optimal_alignments(self, board):
        return self.traceback(board, True, 0)

def pretty(res, score):
    s1 = ""
    lines = ""
    s2 = ""
    for tup in res:
        s1 += "  " + tup[0] + "  "
        lines += "  |  "
        s2 += "  " + tup[1] + "  "
    lines += "   Score: " + str(score)
    print("Alignment and score:")
    print(s1)
    print(lines)
    print(s2)

def pretty_board(board):
    s = "BOARD:\n"
    for i in range(len(board)):
        if i == 0 or i == len(board):
            s+= "+--------------------+\n"
        else:
            s += "|--+--+--+--+--+--+--|\n"
        for elem in board[i]:
            if len(str(elem)) > 1:
                s += "|" + str(elem)
            else:
                s += "|" + str(elem) + " "
        s += "|\n"
    s += "+--------------------+"
    print(s)


b1 = Board(input("First sequence [ex. WPIWPC]: "), input("Second sequence [ex. IIWPI]: "), int(input("Gap penalty [ex. -4]: ")))
board = b1.makeboard()
pretty_board(board)

res, scores = b1.find_optimal_local_alignment(board)
pretty(res[0], scores[0])
print("#####################################################")
pretty(res[1], scores[0])

#pprint(b1.find_all_possible_optimal_alignments(board))
#pprint(b1.traceback(board, False, 26))


