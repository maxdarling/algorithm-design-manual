# balanced parentheses.

# determines if the input string 's' has balanced open/close "braces" (can be any token) 
# returns (is_balanced, offending_idx). -1 if no offending idx
def is_balanced(s: str, open_brace: str, closed_brace: str) -> (bool, int):
    num_open = 0 # number of open braces.
    for idx, char in enumerate(s):
        if char == open_brace:
            num_open += 1
        elif char == closed_brace and num_open == 0:
            return (False, idx)
        elif char == closed_brace and num_open > 0:
            num_open -= 1

    return (True, -1) if num_open == 0 else (False, len(s))

assert(is_balanced("{{}}", "{", "}")[0])
assert(not is_balanced("{{}", "{", "}")[0])
assert(is_balanced("{{}", "{", "}")[1] == 3)
assert(is_balanced("", "{", "}")[0])
