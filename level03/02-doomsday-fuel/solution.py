from fractions import Fraction


def reorder_cols(matrix, column_mapping):
    result_matrix = [
        [matrix[row][col] for col in range(len(matrix[0]))]
        for row in range(len(matrix))
    ]

    tmp = {}

    for col1, col2 in column_mapping.items():
        if col2 not in tmp:
            tmp[col2] = [matrix[row][col2] for row in range(len(matrix))]

        if col1 not in tmp:
            for row in range(len(matrix)):
                result_matrix[row][col2] = matrix[row][col1]
        else:
            for row in range(len(matrix)):
                result_matrix[row][col2] = tmp[col1][row]

    return result_matrix


def create_new_mapping(terminal_rows, transition_rows):
    new_mapping = {}

    for i in range(len(transition_rows)):
        new_mapping[transition_rows[i]] = i
    for i in range(len(terminal_rows)):
        real_i = i + len(transition_rows)
        new_mapping[terminal_rows[i]] = real_i

    return new_mapping


def reorder_rows(matrix, new_mapping):
    return [
        matrix[original_row]
        for original_row, _ in sorted(new_mapping.items(), key=lambda item: item[1])
    ]


def reorder_matrix(matrix):
    terminal_rows = [
        row for row in range(len(matrix)) if all(col == 0 for col in matrix[row])
    ]
    transition_rows = [
        row for row in range(len(matrix)) if any(col != 0 for col in matrix[row])
    ]

    new_mapping = create_new_mapping(terminal_rows, transition_rows)
    return reorder_cols(reorder_rows(matrix, new_mapping), new_mapping)


def transform_to_probabilities(matrix):
    for row in range(len(matrix)):
        total = sum(matrix[row])
        if total != 0:
            for col in range(len(matrix[0])):
                matrix[row][col] = Fraction(matrix[row][col], total)
    return matrix


def get_terminal_index(matrix):
    for row in range(len(matrix)):
        if all(col == 0 for col in matrix[row]):
            return row


def get_identity_matrix(size):
    matrix = [[] for _ in range(size)]
    for row in range(size):
        for col in range(size):
            matrix[row].append(1 if row == col else 0)
    return matrix


def gauss_jordan_elimination(matrix):
    def eliminate(row1, row2, col, target=0):
        fac = (row2[col] - target) / row1[col]
        for col2 in range(len(row2)):
            row2[col2] -= fac * row1[col2]

    for row in range(len(matrix)):
        if matrix[row][row] == 0:
            for col in range(row + 1, len(matrix)):
                if matrix[row][col] != 0:
                    matrix[row], matrix[col] = matrix[col], matrix[row]
                    break

        for col in range(row + 1, len(matrix)):
            eliminate(matrix[row], matrix[col], row)

    for row in range(len(matrix) - 1, -1, -1):
        for col in range(row - 1, -1, -1):
            eliminate(matrix[row], matrix[col], row)

    for row in range(len(matrix)):
        eliminate(matrix[row], matrix[row], row, target=1)

    return matrix


def invert_matrix(matrix):
    inverted = [[] for _ in matrix]
    for i, row in enumerate(matrix):
        assert len(row) == len(matrix)
        inverted[i].extend(row + [0] * i + [1] + [0] * (len(matrix) - i - 1))
    gauss_jordan_elimination(inverted)
    return [inverted[i][len(inverted[i]) // 2 :] for i in range(len(inverted))]


def slice_matrix(matrix, row_slice, col_slice):
    sliced = []
    for row in range(*row_slice):
        new_row = []
        for col in range(*col_slice):
            new_row.append(matrix[row][col])

        sliced.append(new_row)
    return sliced


def subtract_matrices(matrix1, matrix2):
    matrix = [[0] * len(matrix1[0]) for _ in range(len(matrix1))]
    for row in range(len(matrix1)):
        for col in range(len(matrix1[0])):
            matrix[row][col] = matrix1[row][col] - matrix2[row][col]
    return matrix


def multiply_matrices(matrix1, matrix2):
    matrix = [[0] * (len(matrix2[0])) for _ in range(len(matrix1))]
    for row1 in range(len(matrix1)):
        for col2 in range(len(matrix2[0])):
            for row2 in range(len(matrix2)):
                matrix[row1][col2] += matrix1[row1][row2] * matrix2[row2][col2]
    return matrix


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(numbers):
    result = 1
    for n in numbers:
        result = result * n // gcd(result, n)
    return result


def solution(matrix):
    if all(c == 0 for c in matrix[0]):
        return [1] + [0] * (len(matrix[0]) - 1) + [1]

    matrix = transform_to_probabilities(reorder_matrix(matrix))
    terminal_index = get_terminal_index(matrix)

    # https://en.wikipedia.org/wiki/Absorbing_Markov_chain
    Q = slice_matrix(matrix, (0, terminal_index), (0, terminal_index))
    R = slice_matrix(matrix, (0, terminal_index), (terminal_index, len(matrix[0])))
    I = get_identity_matrix(terminal_index)

    # Fundamental Matrix: N = (I - Q)^(-1)
    N = invert_matrix(subtract_matrices(I, Q))

    # Probabilities: B = N * R
    probabilities = multiply_matrices(N, R)
    common_denominator = lcm([p.denominator for p in probabilities[0]])
    return list(
        map(
            int,
            [
                (common_denominator / p.denominator) * p.numerator
                for p in probabilities[0]
            ]
            + [common_denominator],
        )
    )


assert solution(
    [
        [0, 0, 0, 2, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 3, 4, 0, 0],
        [0, 0, 0, 0, 0],
    ]
) == [6, 8, 7, 21]
assert solution(
    [
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
) == [7, 6, 8, 21]
assert solution(
    [
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
) == [0, 3, 2, 9, 14]
assert solution(
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
) == [1, 0, 0, 0, 1]
