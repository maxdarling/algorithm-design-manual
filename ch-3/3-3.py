from util.node import Node

'''
reverse a linked list by modifying it. returns the head of the new list.
'''
def reverse_list(head: Node) -> Node:
    if not head or not head.next:
        return head

    curr = head
    prev = None
    while curr:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp

    return prev


# tests
a = Node(5)
b = Node(4, a)
c = Node(3, b)
revlist = reverse_list(c)
assert(revlist.val == 5)
assert(revlist.next.val == 4)
assert(revlist.next.next.val == 3)
