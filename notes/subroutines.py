'''
Subroutines
-----------

Like simple functions.
* No function arguments.
* No return values.

When we call a function:
    * PUSH the return address on the stack
    * Set the PC to the function address

When we return:
    * POP the return address off the stack, store it in the PC
'''


def bar():
    print("Hello again")
    return


def foo():
    print("hi there")
    bar()
    print("and we're back")
    bar()
    print("and we're back again")
    return


foo()

print("Done!")  # addr_1

# Stack top ->
