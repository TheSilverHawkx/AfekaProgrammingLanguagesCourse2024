
# Testing

The project includes a comprehensive set of unit tests and end-to-end tests to ensure the correctness of the interpreter.

## Unit Tests

Unit tests are provided for each component of the interpreter:
- **Lexer Tests**: Tests for tokenizing input text.
- **Parser Tests**: Tests for constructing the AST from tokens.
- **Semantic Analyzer Tests**: Tests for validating the semantics of the AST.
- **Interpreter Tests**: Tests for executing the AST and producing the correct results.

## End-to-End Tests

End-to-end tests cover the entire process from tokenization to execution. These tests use sample input programs and verify that the output is as expected.

To run the tests, use:

```bash
pytest
```

