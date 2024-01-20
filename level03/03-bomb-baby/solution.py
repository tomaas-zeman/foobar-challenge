def replicate(m, f, gen):
    return [(m + f, f, gen + 1), (m, m + f, gen + 1)]


def solution(m, f):
    mach_bombs_needed = int(m)
    facula_bombs_needed = int(f)

    visited = set()
    stack = [(1, 1, 0)]

    while stack:
        mach_bombs, facula_bombs, generations = stack.pop()

        if mach_bombs == mach_bombs_needed and facula_bombs == facula_bombs_needed:
            return str(generations)

        if mach_bombs > mach_bombs_needed or facula_bombs > facula_bombs_needed:
            continue

        if (mach_bombs, facula_bombs) in visited:
            continue
        else:
            visited.add((mach_bombs, facula_bombs))

        mach_steps_with_current_production = (mach_bombs_needed - mach_bombs) // (
            mach_bombs + facula_bombs
        )
        facula_steps_with_current_production = (facula_bombs_needed - facula_bombs) // (
            mach_bombs + facula_bombs
        )

        if (
            mach_steps_with_current_production * 50
            < facula_steps_with_current_production
        ):
            stack.append(replicate(mach_bombs, facula_bombs, generations)[0])
        elif (
            facula_steps_with_current_production * 50
            < mach_steps_with_current_production
        ):
            stack.append(replicate(mach_bombs, facula_bombs, generations)[1])
        else:
            stack.extend(replicate(mach_bombs, facula_bombs, generations))

    return "impossible"


assert solution("4", "7") == "4"
assert solution("2", "1") == "1"
assert solution("2", "4") == "impossible"
