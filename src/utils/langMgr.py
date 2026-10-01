from tokenize import TokenInfo
from collections.abc import Generator
from typing import LiteralString
from ast import Module
from tokenize import generate_tokens, COMMENT, untokenize
from io import StringIO
from ast import parse, walk, Import, ImportFrom

def RemoveComments(context: str) -> str:
    # generate_tokens() expects a file-like object, not a string, so StringIO(context) wraps the string in a fake in-memory file
    # Read "file" line by line and splits into tokens e.g. names, operators, numbers, and comments
    # The result is a stream of TokenInfo objects, one per token
    tokens: Generator[TokenInfo] = generate_tokens(StringIO(context).readline)

    # Generator expression that will lazily produce the filtered token
    filtered_tokens: Generator[TokenInfo] = (
        token for token in tokens
        if token.type != COMMENT
    )

    # Assign the lazy generator (no tokens are processed yet) to filtered_tokens
    # Rebuild Python source code from the filtered tokens, preserving the code
    return untokenize(filtered_tokens)

def GetImports(content: str) -> list [str]:
    imports: list[str] = []

    # Parse the source content into an abstract syntax tree;
    # `tree` is type-annotated as a `Module` (the AST's root node).
    try:
        tree: Module = parse(content)
    except SyntaxError as error:
            raise ValueError(f"Source is not valid Python: {error}") from error

    for node in walk(tree):
        if isinstance(node, Import):# Handle: import module1, module2
            for alias in node.names:
                if alias.name not in imports:
                    imports.append(alias.name)

        elif isinstance(node, ImportFrom):
            if node.module:
                if node.level > 0:
                    # Relative import (from .module or from ..module)
                    relative_prefix: LiteralString = '.' * node.level
                    imports.append(f"{relative_prefix}{node.module}")
                else:
                    # Absolute import
                    imports.append(node.module)
            elif node.level > 0:
                # Handle cases like: from . import something
                relative_prefix: LiteralString = '.' * node.level
                imports.append(relative_prefix)

    return imports
