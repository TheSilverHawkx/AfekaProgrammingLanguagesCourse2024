
# Examples

This section provides examples of code written in the custom language, along with explanations of what each example does.

## Example 1: Lambda Expression

```
>>> (Lambd x . (x + 2))
```

This defines a lambda function that takes one argument `x` and returns the result of `x + 2`.

## Example 2: Function Definition

```
>>> Defun {'name': 'add', 'arguments': (x, y)}
... (x + y)
>>> add(5,7)
12
```

This defines a function `add` that takes two arguments `x` and `y` and returns their sum. It then calls this function

## Example 3: Arithmetics

```
>>> 1*2*3
6
>>> 2/3
0
```

This performs arithmetics operations following *PEMDAS*.

Note: the language includes integers only so every number will be rounded down.
