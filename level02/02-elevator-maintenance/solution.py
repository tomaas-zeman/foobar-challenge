def solution(versions):
    return sorted(versions, key=lambda x: [int(i) for i in x.split(".")])


assert solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]) == [
    "0.1",
    "1.1.1",
    "1.2",
    "1.2.1",
    "1.11",
    "2",
    "2.0",
    "2.0.0",
]
assert solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]) == ["1.0", "1.0.2", "1.0.12", "1.1.2", "1.3.3"]
