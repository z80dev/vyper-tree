# @version ^0.3.5

# Create a string variable that can store maximum 100 characters
greet: public(String[100])

@external
def __init__():
    self.greet = "Hello World"

@external
def foo(x: uint256) -> uint256:
    val: uint256 = 0
    for i in range(100000):
        val += 1
        if not val < x:
            break
    return val
