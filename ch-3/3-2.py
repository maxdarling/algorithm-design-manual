# find the longest balanced subsequence 
# assumes strings are parens only
# returns: length of longest balanced subsequence
def longest_balanced_subsequence(s: str) -> int:
    open_count = 0
    closed_count = 0

    # algorithm: greedily take open parens. if they don't end up with a
    # pair, by definition it's fine to remove them at the end

    for idx, char in enumerate(s):
        if char == '(':
            open_count += 1
        elif char == ')':
            closed_count += 1 if open_count > closed_count else 0

    return 2 * min(open_count, closed_count)


assert(longest_balanced_subsequence(")()(())()()))())))(") == 12)
assert(longest_balanced_subsequence("") == 0)

