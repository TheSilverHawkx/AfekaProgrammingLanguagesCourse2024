count_palindromes = lambda input_list: list(map(lambda sublist: len(list(filter(lambda x: x == x[::-1], sublist))), input_list))


count_palindromes([
    ['aa','hello','elle','foo'],
    ['ar','br','cr'],
    ['wow','wow','wow','wow','wow']
])

