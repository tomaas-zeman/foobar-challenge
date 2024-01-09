from collections import deque


def solution(n):
    n = int(n)

    visited = set()

    queue = deque([(n, 0)])
    while len(queue) > 0:
        number, step = queue.pop()

        if (number, step) in visited:
            continue
        visited.add((number, step))

        if number == 1:
            return step

        if number % 2 == 0:
            queue.appendleft((number // 2, step + 1))
        else:
            queue.appendleft((number - 1, step + 1))
            queue.appendleft((number + 1, step + 1))


assert solution("15") == 5
assert solution("4") == 2
