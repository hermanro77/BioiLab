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
                    #Diagonal score
                    sum1 = self.get_score_from_matrix(self.string1[j-1], self.string2[i-1]) + board[i-1][j-1].value
                    #Top score
                    sum2 = board[i-1][j].value + self.gap_pen
                    #Left score
                    sum3 = row[j-1].value + self.gap_pen

                    sums = [sum1, sum2, sum3]
                    maxes = [i for i, x in enumerate(sums) if x == max(sums)] #creates list with index of
                                                                            #the highest sum(s). Can be multiple

                    #Adds a zero Tile with no pointers if all sums are negative
                    if self.all_negative_numbers(sums):
                        row.append(Tile(i, j, 0))

                    #goes through the list of all max values and appends the indexes to pointers list
                    else:
                        pointers = []
                        for max_value_index in maxes:
                            if max_value_index == 0:
                                pointers.append((i-1, j-1))
                            elif max_value_index == 1:
                                pointers.append((i-1, j))
                            elif max_value_index == 2:
                                pointers.append((i, j-1))

                        #Adds the Tile with pointers to the row in the score board
                        row.append(Tile(i, j, max(sums), pointers))

            #full row with tiles and their pointers added to baord
            board.append(row)
        return board

    #Checks if all numbers in values list are negative
    def all_negative_numbers(self, values):
        b = True
        for val in values:
            if val >= 0:
                b = False
        return b

    #gets the score from characters in the blossum50 matrix
    def get_score_from_matrix(self, char1, char2):
        m = [self.BLOSSUM50_MATRIX[i:i + len(self.rows)] for i in range(0, len(self.BLOSSUM50_MATRIX), len(self.rows))]
        if isinstance(char1, int) and isinstance(char2, int):
            return m[char2][char1]
        return m[self.cols.index(char2)][self.rows.index(char1)]


    def traceback_with_depthfirst_search(self, board, starting_tile_val):
        tile_indexes = self.find_all_tiles_with_value(board, starting_tile_val)
        results = []

        #For every starting index perform depth first search
        for index in tile_indexes:
            results.extend(list(self.dfs_paths(board, index[0], index[1])))
        return results, starting_tile_val

    def find_all_tiles_with_value(self, board, val):
        indexes = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].value == val:
                    indexes.append((i, j))
        return indexes

    #does dfs on board with tiles from index (x, y) and returns list of lists with paths from tile at (x, y) to a tile with
    #value 0
    def dfs_paths(self, board, x, y):
        start_node = board[x][y]
        stack = [(start_node, [start_node])]
        while stack:
            (tile, path) = stack.pop()
            for index in tile.pointers:
                next = board[index[0]][index[1]]
                if next.value == 0:
                    yield path
                else:
                    stack.append((next, path + [next]))


    #Finds the optimal alignments
    def find_optimal_local_alignments(self, board):
        optimal_score = 0
        for li in board:
            for tile in li:
                if tile.value > optimal_score:
                    optimal_score = tile.value

        return self.traceback_with_depthfirst_search(board, optimal_score)


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

    def create_sequence_from_tile_path(self, path):
        seq = [(self.string2[path[0].x - 1], self.string1[path[0].y - 1])]
        for i in range(len(path)-1):
            seq.append(self.get_letters_from_pointer(path[i], (path[i+1].x, path[i+1].y)))
        return seq


def pretty_seq(res, score):
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
optimal_paths, highest_score = b1.find_optimal_local_alignments(board)
for path in optimal_paths:
    pretty_seq(b1.create_sequence_from_tile_path(path), highest_score)


