"""Min stack."""

class Stack:
    """Min stack."""

    def __init__(self):
        self.stack = []
        # maintain a stack of the min elements encountered. top of stack is the
        # overall min element. when that element is popped from the main stack,
        # pop it from the min_stack as well. and sub-recursive case begins...
        self.min_stack = []

    def push(self, x: int):
        """Push an element to top of the stack."""
        if len(self.stack) == 0 or x < self.min_stack[-1]:
            self.min_stack.append(x)

        self.stack.append(x)

    def pop(self) -> int:
        """Remove and return the top stack element."""
        if len(self.stack) > 0:
            if self.stack[-1] == self.min_stack[-1]:
                self.min_stack.pop()

            return self.stack.pop()

        return None

    def find_min(self) -> int:
        """Return the minimum element."""
        if len(self.stack) > 0:
            return self.min_stack[-1]
        return None

class FancyMinStack:
    """
    Stack supporting a O(1) min operation using O(1) extra space! (Note: only works for integers).

    This uses a tricky approach!
    - Maintain a stack
    - Maintain the minimum value seen so far in a variable
    - When the stack is empty, push its value normally
    - For pushes when the stack is non-empty:
        - if the value is not a new min, push its value normally
        - if it's a new min, push (2*newMin - oldMin) and update the min variable normally.
            - note 1: this expr is always less than the new min. You can see this if you rewrite
            to newMin + (newMin - oldMin) and show that the value of the paren expr is always negative.
            - note 2: assuming that we have the value of newMin on hand when we pop this value at some point
            in the future, note that we'll be able to recover the value of 'oldMin'

    - For pops:
        - if the value is greater or equal to the current min, pop it normally
        - if the value is less than the current min (an impossibility under normal circumstances), we
        know it's one of our special values from the push step. the actual value is the min we're storing
        in our variable. recover the 'oldMin' and set it as our new min: for popped value V and newMin < oldMin,
        the expression is oldMin = -V + 2*newMin. (Names are a bit confusing - remember "new" here means it was *pushed*
        later. When popping values off the stack, this notion gets flipped, beware.).

    Summary:
    This is tricky but let's summarize why this works. We've used an insight that when you're maintaining a min variable
    normally, you will never see a value less than the min when not adding new values (i.e. popping/peeking in a stack).
    Being optimizing computer scientists, we take advantage of that. Knowing that this can't happen naturally, we
    realize that if we push such values ourselves, when we check back on them later and see that they violate the min
    principle, we'll know it must have been us who did this. We can think of these values as "special". And we can do
    this without penatly as long as we are able to later transform the modified value back to it's true form. So we have
    just gained the ability to mark values as special with no cost. That's an extra free bit of information!

    The simplest scheme or "transformation" that violates the min rule is x_trans = f(x) = x - 1. It violates the min rule,
    check. And it is also always possible to recover the value - we just add 1 to the value, i.e. x = x_trans + 1. Note
    that not all transformations are invertible - e.g. x_trans = |x|. when we attempt to recover the value of x later from
    x_trans, we have no way of knowing if x = x_trans or x = -x_trans. This is the same thing as funtion inverses -
    i.e. f(x) = |x| has no inverse because it fails the horizontal line test.

    So, now we've seen that:
    1. encountering a value smaller than the min won't happen naturally, so when it happens we'll know it was us who
    must've done this specially when the value was pushed
    2. transformations that decrease their input values will violate the min constraint. and we want ones that are
    invertible - we want to be able to transform our input variable initially and then recover it later from the
    transformed value.

    Combining the above points, we have something cool: with a good transformation function, we can make values violate
    the min constraint at will, and the true values will always be recoverable. In practice, this means that we now have
    the ability to push either "special" values or normal values. That's an entire extra bit of information we've just
    gained for each element in our stack! That's great! And the price to pay is just a litle extra work of transforming
    and un-transforming the "special" elements.

    With that understood, there's not much left to it.

    The last insight is that if we're maintaining a min variable, whenever we push a new min, it feels redundant
    to store that value in the min variable and also push that value onto the stack. Instead, we'll opt to make this
    a "special" value since it's a min. Remember we can make values special at will "for free". In general, whenever we
    are pushing a value and see that it's a new min, we'll make it special. And hand waiving the transformation
    for a moment, what value would we like to store? Well, lets store the prev/old min. We're overwriting the old min
    with the new min, but we don't want to lose that information about what the old min was, because otherwise when this
    value eventually gets popped, we wouldn't know what the next min is.

    This turns out to be all we need in order to know the min at any given point. As we push values, if we encounter a
    min, we mark them and store the prevMin in them, and of course update the min variable. As we pop values, we check
    whether it's special. If it was, we know it's our current min and is encoding the value of the previous min. We know
    its value because our min variable is storing it. We un-transform to get the old min, update the min variable,
    and pop the value. Now we're back where we started: our min variable is correctly storing the current min.

    For another framing: consider the naive solution attempt of keeping a normal stack and a min variable. As you
    push values the min variable works great. But when you eventually pop the min, you have no idea where the previous
    min is in among all the values behind you in the stack. As a solution, you could imagine pushing 2 values instead of 1:
    the value and a "pointer" to the previous min, so that when you popped the min, you'd look at you pointer to the
    previous min. This works, but requires 2N memory.

    Now think back to our solution. It just uses N + 1 memory, a single stack and a variable. In the stack, normal values
    are pushed normally. Min values are *marked*. And the marking is "free", as we saw earlier. This is key. If a min is marked,
    and we're maintaining a min variable, this means whenever we encounted a marked min var, we can read it's value from the
    min variable instead of the element itself in the stack. This frees up all the min variables for us in the stack - we can
    store whatever we want in there. And what will we use that free slot for? To store the value of the previous min var. This
    is the "pointer" from the naive solution above. With that, we know the values of normal values, we know the values of our marked
    mins because the min var holds it, and every min var points back to the previous min. That's a complete solution!

    Okay, I hand-waived on the trasformation earlier but now here it is. Assume we are pushing a new min
    'newMin' and our previous min stored in the min var is 'oldMin'. Then we need a transformation that:
    1. T(oldMin) < newMin (violates min constraint, i.e. its "markable")
    2. T^-1(T(oldMin)) = oldMin (i.e. T is invertible, so that 'oldMin' can be decoded from the transformed value)

    With that, the simplest and most commonly used T is:
        2*newMin - oldMin

    When I first saw this problem, I was discouraged because I was doubtful that I'd be able to derive this on my own.
    However, I also hadn't understood the critical insight at all either. If you have made the critical insight, you'll
    arrive at the two constraints above, and then you're just a few minutes of fiddling away from solving the transform.
    The insight is really the hard part: realizing that you can use the min constraint violation to your advantage to
    "mark" values, with then lets you stretch your dollar on the min variable and avoid having to store the min values
    in the stack.
    """
    def __init__(self) -> None:
        self.stack = []
        self.min = None

    def push(self, x: int):
        if len(self.stack) == 0:
            self.stack.append(x)
            self.min = x
            return

        if x < self.min:
            # new min. mark and push old min
            self.stack.append(2*x - self.min)
            self.min = x
        else:
            self.stack.append(x)

    def pop(self) -> int:
        if len(self.stack) == 0:
            return None
        if self.stack[-1] >= self.min:
            return self.stack.pop()

        # min. decode to get prev min.
        ret = self.min
        self.min = -self.stack[-1] + 2*self.min
        self.stack.pop()
        return ret

    def find_min(self) -> int:
        if len(self.stack) > 0:
            return self.min
        return None


def test(s):
    test_input = [5,2,3,7,1,5,4]
    print("growing!")
    for x in test_input:
        s.push(x)
        print(f's: {s.stack}, min: {s.find_min()}')
    print("shrinking!")
    for _ in range(len(s.stack) + 1):
        s.pop()
        print(f's: {s.stack}, min: {s.find_min()}')

print("testing normal stack")
s = Stack()
test(s)
print("testing fancy stack")
s = FancyMinStack()
test(s)
