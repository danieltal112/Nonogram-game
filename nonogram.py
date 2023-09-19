#############################################################
# file   : nonogram.py
# WRITER : OREN EYAL, oreneyal15 , 318967049
# WRITER : DANIEL TAL, danieltal , 204501712
# EXERCISE : intro2cs1 ex8 2021
# DESCRIPTION : program that solves a nonogram game
#############################################################

BLACK = 1
WHITE = 0
BLANK = -1


###1
def constraint_satisfactions(n, blocks):
    """This function receives a row length and a list of blocks and returns
    all of the options to place the blocks in the row"""
    all_options = []
    constraint_satisfactions_helper(n, blocks[:], [], all_options, )
    return all_options


def constraint_satisfactions_helper(n, blocks, options, all_options):
    """This is a helper function of constraint satisfaction """
    if not blocks and len(options) < n:
        options += [WHITE] * (n - len(options))
        all_options.append(options)
        return
    if not blocks and len(options) == n:
        all_options.append(options)
        return
    if len(options) > n:
        return
    if len(blocks) == 1 and len(options) + blocks[0] == n:
        options += [BLACK] * blocks[0]
        all_options.append(options)
        return
    num = blocks[0]
    constraint_satisfactions_helper(n, blocks[1:],
                                    options + [BLACK] * num + [WHITE],
                                    all_options)
    blocks.insert(0, num)
    constraint_satisfactions_helper(n, blocks[1:], options + [WHITE],
                                    all_options)


###2
def row_variations(row, blocks):
    """This function receives a certain row and a list of blocks and returns
    all the options to fill the row"""
    if blocks == [] and row.count(BLACK) != 0:
        return []
    option_lst = []
    if row.count(WHITE) == len(row) and blocks:
        return []
    if row.count(BLANK) + row.count(BLACK) < sum(blocks):
        return []
    help_row_variation(row, blocks[:], [], option_lst, 0, sum(blocks))
    return option_lst


def help_row_variation(row, blocks, row_option, all_option, i, sum_blocks):
    if i == len(row):
        if row_option.count(BLACK) == sum_blocks:
            all_option.append(row_option)
        return
    if len(blocks) == 0:
        if len(row) == len(row_option):
            if row_option.count(BLACK) == sum_blocks:
                all_option.append(row_option)
        elif len(row_option) < len(row) and BLACK not in row[i:]:
            row_option += [WHITE] * (len(row) - len(row_option))
            if row_option.count(BLACK) == sum_blocks:
                all_option.append(row_option)
        return
    if row[i] == WHITE:
        row_option.append(WHITE)
        help_row_variation(row, blocks, row_option, all_option, i + 1,
                           sum_blocks)
    if len(blocks) > 0:
        if len(row_option) + blocks[0] < len(row):
            if row[i] == BLACK:
                if ok_to_place(row[i:i + blocks[0]], row[i + blocks[0]]):
                    row_option.extend([BLACK] * blocks[0] + [WHITE])
                    help_row_variation(row, blocks[1:], row_option, all_option,
                                       i + blocks[0] + 1, sum_blocks)
                else:
                    return []

            if row[i] == BLANK:
                if ok_to_place(row[i:i + blocks[0]], row[i + blocks[0]]):
                    num = blocks[0]
                    help_row_variation(row, blocks[1:], row_option + (
                            [BLACK] * blocks[0] + [WHITE]), all_option,
                                       i + blocks[0] + 1, sum_blocks)
                    blocks.insert(0, num)
                    help_row_variation(row, blocks[1:], row_option + [WHITE],
                                       all_option, i + 1, sum_blocks)
                else:
                    help_row_variation(row, blocks, row_option + [WHITE],
                                       all_option,
                                       i + 1, sum_blocks)
        if len(row_option) + blocks[0] == len(row):
            if WHITE in row[i:i + blocks[0]]:
                return
            row_option += [BLACK] * blocks[0]
            if row_option.count(BLACK) == sum_blocks:
                all_option.append(row_option)
            return
        if len(blocks) + len(row_option) > len(row):
            return

    return all_option


def ok_to_place(row, next_box):
    """This function checks if it is legal to place a block in a row"""
    return WHITE not in row and (next_box == BLANK or next_box == WHITE)


### 3
def intersection_row(rows):
    """This function receives a list of rows and returns a row that is
     common to all the rows"""
    if len(rows) == 1:
        return rows[0]
    if len(rows) > 0:
        lst = []
        for i in range(len(rows[0])):
            flag = True
            for j in range(len(rows) - 1):
                if rows[j][i] != rows[j + 1][i]:
                    flag = False
            if flag is True:
                lst.append(rows[j][i])
            else:
                lst.append(-1)
        return lst


### 4
def reverse_matrix(mtx):
    """This function receives a nonogram board
    and switches the rows with the column"""
    len_row = len(mtx[0])
    return [[mtx[j][i] for j in range(len(mtx))] for i in range(len_row)]


def solve_easy_nonogram(constraints):
    """This function solves a simple board of nonogram"""
    len_row = len(constraints[1])
    game_board = []
    for i in range(len(constraints[0])):
        row_options = constraint_satisfactions(len_row, constraints[0][i])
        shared_option = intersection_row(row_options)
        game_board.append(shared_option)

    return helper_solve_easy(constraints, game_board)


def helper_solve_easy(constraints, game_board):
    """This is a helper function for solve_easy_nonogram to solve a
    simple nonogram"""
    if not check_if_constraints_legal(constraints):
        return None
    if [] in game_board:
        return
    for i in range(len(constraints[0])):
        if not game_board[i]:
            return
        row_option = row_variations(game_board[i], constraints[0][i])
        if row_option == []:
            return
        shared_option = intersection_row(row_option)
        game_board[i] = shared_option
    mat_reverse = reverse_matrix(game_board)
    for j in range(len(constraints[1])):
        row_options2 = row_variations(mat_reverse[j], constraints[1][j])
        if row_options2 == []:
            return
        shared_option2 = intersection_row(row_options2)
        mat_reverse[j] = shared_option2
    mat_reverse = reverse_matrix(mat_reverse)
    if game_board == mat_reverse:
        return game_board
    elif check_if_solved(mat_reverse):
        return mat_reverse
    return helper_solve_easy(constraints, mat_reverse)


def check_if_constraints_legal(constraints):
    """This function checks if the number of constraints of row is equal to
    the number of column constraints """
    if not constraints[0] or not constraints[1]:
        return False
    row_con = []
    col_con = []
    row_con += [value for con in constraints[0] for value in con]
    col_con += [value for con in constraints[1] for value in con]
    return sum(row_con) == sum(col_con)


def check_if_solved(mat):
    """This function checks if there are no more blanks on the board"""
    for row in mat:
        if BLANK in row:
            return False
    return True


### 5
def solve_nonogram(constraints):
    """This function solves a full game of nonogram and returns all the
    options of solutions"""
    game_mat = solve_easy_nonogram(constraints)
    all_options = []
    solve_nonogram_helper(constraints, game_mat, all_options)
    return all_options


def solve_nonogram_helper(constraints, game_mat, all_solutions):
    """This is a helper function for solve_nonogram that helps to solve
    a full nonogram game"""
    if not game_mat:
        return []
    if check_if_solved(game_mat):
        all_solutions.append(game_mat)
        return
    for i in range(len(constraints[0])):
        if BLANK in game_mat[i]:
            for row in row_variations(game_mat[i], constraints[0][i]):
                game_mat[i], save_row = row, game_mat[i]
                game_mat2 = helper_solve_easy(constraints, game_mat)
                game_mat[i] = save_row
                solve_nonogram_helper(constraints, game_mat2, all_solutions)
            return
