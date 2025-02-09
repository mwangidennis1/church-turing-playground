# Lambda Calculus Interpreter
This project was developed as part of SFE 4015: Software Configuration Management

It is an  interactive web-based interpreter for lambda calculus expressions, allowing users to input and evaluate lambda terms through beta reduction plus a simple simulation of the Turing machine

The project is intended to showcase basic foundations of the church-turing hypotheses

## Overview

This interpreter provides a simple interface to experiment with lambda calculus, the foundational mathematical framework for functional programming. It supports:
- Pure lambda calculus expressions
- Step-by-step beta reductions
- Standard lambda calculus notation (λ symbol or 'lambda' keyword)

## Examples

Here are some example expressions you can try:

```
> (λx.x)(λy.y)
(λy.y)                    # Identity function applied to identity function

> (λa. (λb. b a) a) (λz. z) (λw. w)
(λw.w)                    # Complex nested application

> (λx.λy.x y)(λz.z)
λy.(λz.z) y              # Function application with multiple arguments
```

## Notation Guide

- `λ` or `lambda`: Introduces a function abstraction
- `.` (dot): Separates the bound variable from the function body
- `()` (parentheses): Group expressions and indicate function application
- Variables: Any alphabetic character (traditionally starting with x, y, z for bound variables)

## Why Use Lambda Calculus?

Lambda calculus serves several important purposes:

1. **Theoretical Foundation**
   - Understand the core concepts of functional programming
   - Study computation and programming language theory
   - Explore function composition and application

2. **Educational Tool**
   - Learn about variable binding and scope
   - Understand function evaluation and reduction strategies
   - Practice formal reasoning about programs

3. **Practical Applications**
   - Design and analyze functional programming patterns
   - Verify program correctness
   - Study type systems and program optimization

## Features

- Interactive terminal-style interface
- Real-time expression evaluation
- Step-by-step reduction visualization
- Support for complex nested expressions
- Clear error messages for invalid syntax

## Usage Tips

1. **Basic Functions**
   - Identity function: `λx.x`
   - Constant function: `λx.λy.x`
   - Self-application: `λx.x x`

2. **Common Patterns**
   - Function composition
   - Curried functions
   - Higher-order functions

3. **Best Practices**
   - Use parentheses to clarify expression grouping
   - Break down complex expressions into smaller steps
   - Pay attention to variable scope and binding

## Technical Details

The interpreter implements:
- Alpha conversion to handle variable naming conflicts
- Beta reduction for function application
- Normal order reduction strategy
- Parser for lambda calculus syntax

## Getting Started

1. Open the interpreter in your web browser by executing the run.sh file
   ```
    git clone https://github.com/mwangidennis1/church-turing-playground.git
    cd church-turing-playground
    chmod +x run.sh
    source run.sh # activates shell environment
    python __init__.py # entry point of the program
    ```
2. Type a lambda calculus expression at the prompt
3. Press Enter to see the result
4. Each reduction step will be displayed automatically




## Contributing

Interested in contributing? Here are some areas where you can help:
- Add new reduction strategies
- Improve error messages
- Enhance the user interface
- Write additional documentation
- Add test cases

## References

For more information about lambda calculus:
- Alonzo Church's original papers
- Barendregt's "The Lambda Calculus: Its Syntax and Semantics"
- Pierce's "Types and Programming Languages"