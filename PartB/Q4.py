def cumulative_operation(operation):
    def apply_operation(sequence):
        result = sequence[0]
        for element in sequence[1:]:
            result = operation(result, element)
        return result
    return apply_operation

# Factorial function using the cumulative_operation function
def factorial(n):
    if n == 0:
        return 1
    return cumulative_operation(lambda x, y: x * y)(range(1, n + 1))

# Exponentiation function using the cumulative_operation function
def exponentiation(base, exponent):
    if exponent == 0:
        return 1
    return cumulative_operation(lambda x, y: x * y)([base] * exponent)

# Testing the functions
print(factorial(5))  # Output: 120
print(exponentiation(2, 3))  # Output: 8
