from functools import reduce
def cumulative_sum_of_squares_even(lst):
    return list(map(
        lambda sublist: reduce(
            lambda acc, x: acc + x,
            map(
                lambda y: y ** 2,
                filter(
                    lambda x: (lambda z: z % 2 == 0)(x),
                    sublist
                )
            ),
            0
        ),
        lst
    ))


input_list = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

print(cumulative_sum_of_squares_even(input_list))
