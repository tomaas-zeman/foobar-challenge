from math import sqrt

ID_LENGTH = 5


def generate_primes(n):
    numbers = [True] * n
    for i in range(2, int(sqrt(n))):
        if numbers[i]:
            for j in range(i ** 2, n, i):
                numbers[j] = False
    return [str(i) for i, value in enumerate(numbers) if value and i > 1]


def solution(i):
    # 20233 is precomputed number that gives us the string length enough
    # to work with our 10000 minions
    return "".join(generate_primes(20233))[i: i + ID_LENGTH]


assert solution(0) == "23571"
assert solution(3) == "71113"
