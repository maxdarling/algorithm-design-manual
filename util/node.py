class Node:
    def __init__(self, val: int, next_node: 'Node' = None):
        self.val = val
        self.next = next_node

    def to_list(self):
        if not self:
            return []
        if not self.next:
            return [self.val]
        return [self.val] + self.next.to_list()

