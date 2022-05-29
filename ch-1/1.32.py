#1-32. [5] Write a function to perform integer division without using either the / or * operators. Find a fast way to do it.


def integer_div(x, y):
    ''' 
    div(x, y) = 1 + div(x-y, y) if x >= y

              = 0 if x < y #discard remainder
    '''
    if (x < y):
        return 0
    else:
        return 1 + integer_div(x-y, y)

