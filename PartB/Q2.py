concat_with_space = lambda strings: reduce(lambda x, y: x + ' ' + y, strings)
from functools import reduce

# Example usage:
strings = ["Python", "is", "fun", "and", "powerful"]
result = concat_with_space(strings)
print(result)
