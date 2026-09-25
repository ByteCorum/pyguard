from tokenize import generate_tokens, COMMENT, untokenize
from io import StringIO
from ast import parse, walk, Import, ImportFrom

def RemoveComments(context):
    tokens = generate_tokens(StringIO(context).readline)
    filtered_tokens = (
        token for token in tokens
        if token.type != COMMENT
    )
    return untokenize(filtered_tokens)

def GetImports(content):
    imports = []
    tree = parse(content)

    for node in walk(tree):
        if isinstance(node, Import):# Handle: import module1, module2
            for alias in node.names:
                if alias.name not in imports:
                    imports.append(alias.name)

        elif isinstance(node, ImportFrom):
            if node.module:
                if node.level > 0:
                    # Relative import (from .module or from ..module)
                    relative_prefix = '.' * node.level
                    imports.append(f"{relative_prefix}{node.module}")
                else:
                    # Absolute import
                    imports.append(node.module)
            elif node.level > 0:
                # Handle cases like: from . import something
                relative_prefix = '.' * node.level
                imports.append(relative_prefix)

    return imports