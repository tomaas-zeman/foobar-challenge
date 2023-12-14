from itertools import combinations


def solution(digits):
    digits.sort(reverse=True)
    for i in range(len(digits), 0, -1):
        for combination in combinations(digits, i):
            if sum(combination) % 3 == 0:
                return int("".join(map(str, combination)))
    return 0


assert solution([3, 1, 4, 1]) == 4311
assert solution([3, 1, 4, 1, 5, 9]) == 94311
