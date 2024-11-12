# Lambda Calculus Interpreter

An interactive web-based interpreter for lambda calculus expressions, allowing users to input and evaluate lambda terms through beta reduction.

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

1. Open the interpreter in your web browser
2. Type a lambda calculus expression at the prompt
3. Press Enter to see the result
4. Each reduction step will be displayed automatically

## Common Exercises

Try these exercises to better understand lambda calculus:

1. Implement boolean logic:
   ```
   TRUE = λx.λy.x
   FALSE = λx.λy.y
   AND = λp.λq.p q p
   ```

2. Create number representations (Church numerals):
   ```
   0 = λf.λx.x
   1 = λf.λx.f x
   2 = λf.λx.f (f x)
   ```

3. Experiment with combinators:
   ```
   I = λx.x            (Identity)
   K = λx.λy.x        (Constant)
   S = λx.λy.λz.x z (y z)  (Substitution)
   ```

## Error Messages

The interpreter provides clear feedback for common issues:
- Unmatched parentheses
- Invalid syntax
- Unbound variables
- Infinite recursion detection

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