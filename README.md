
# Custom Programming Language Interpreter

This project is the final submission for a course on Programming Languages. The goal of this project was to build an interpreter for a custom language designed by our professor. The interpreter includes a lexer, parser, semantic analyzer, and interpreter to execute programs written in this language.

## Project Overview

This interpreter processes a custom programming language, parsing input code through multiple stages:
- **Lexer**: Converts input text into tokens.
- **Parser**: Parses tokens into an Abstract Syntax Tree (AST) based on the language's BNF grammar.
- **Semantic Analyzer**: Performs semantic checks on the AST to ensure correctness.
- **Interpreter**: Executes the validated AST, managing scope and function calls.

The language itself is simple yet expressive, supporting features like lambda expressions and functions.

## Setup Instructions

To set up the project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.12 installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can run the interpreter using cli.py in two modes:

1. **Parse Mode**: Parses a file and performs syntax and semantic analysis.
   ```bash
   python3 src/cli.py parse -f /path/to/file
   ```

2. **Prompt Mode**: Opens an interactive REPL session where you can type and execute commands.
   ```bash
   python3 src/cli.py prompt
   ```

### Example

The `1.lambda` file contains an example of the custom language. You can parse and execute this file as follows:

```bash
python src/cli.py parse -f examples/1.lambda
```

### Additional Examples

Additional examples can be found in the documentation or generated based on the provided BNF grammar.

## Project Structure

- **src**: Contains the source code for the interpreter.
  - **cli.py**: Command-line interface for the interpreter.
  - **interpreter**: Core components of the interpreter.
    - `lexer.py`: The lexer module.
    - `parser.py`: The parser module.
    - `analyzer.py`: The semantic analyzer.
    - `interpreter.py`: The main interpreter module.
    - Additional modules for token management, symbol tables, etc.
- **tests**: Contains unit tests for the lexer, parser, analyzer, and interpreter, as well as end-to-end tests.
- **examples**: Example programs written in the custom language.

## Testing

To run the tests, use the following command:

```bash
pytest
```

This will run all unit tests and end-to-end tests to ensure the interpreter works correctly.

## Credits

This project was developed as a final project for the Programming Languages course. Special thanks to our professor for designing the custom language and guiding us through the process.
