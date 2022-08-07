#!/usr/bin/env python

from rich.tree import Tree
from rich.syntax import Syntax
from rich.console import Group, Console

from argparse import ArgumentParser

from vyper_tree import main
from vyper.compiler import phases
from rich import pretty
import sys

parser = ArgumentParser(description='print vyper ASTs')
parser.add_argument('--force-terminal', action="store_true", help="pass `force_terminal=True` to rich's console constructor. Use for overriding terminal detection and including colorized output even for file outputs.", dest='term')
parser.add_argument('--fold', action="store_true", help="export folded AST")

def node_printer(node):
    match node.ast_type:
        case 'Module':
            return f"Contract {node.name}"
        case 'FunctionDef':
            # return Group(f"Function {node.name}", Syntax("\n".join(["@" + l.node_source_code for l in node.decorator_list]) + "\n" + node.node_source_code, "python", theme="monokai", line_numbers=False))
            return f"Function {node.name}"
        case 'Name':
            return node.id
        case 'arguments':
            return f"Arguments (count: {len(node.args)})"
        case 'arg':
            return f"{node.arg}"
        case 'Int':
            return f"Int: {node.value}"
        case 'Str':
            return '"' + node.value + '"'
        case 'Attribute':
            return node.attr
        case 'Call':
            # inspect(node)
            return node.ast_type
        # case 'While':
            # return node.body
        case _:
            return node.ast_type

def ast_to_rich_tree(node, rich_tree=None):
    if rich_tree is None:
        rich_tree = Tree(node_printer(node))
    else:
        rich_tree = rich_tree.add(node_printer(node))

    for child_node in node.get_children():
        ast_to_rich_tree(child_node, rich_tree)
    return rich_tree

def main():
    pretty.install()

    args = parser.parse_args()

    console = Console(color_system="truecolor", force_terminal=args.term)
    src = ""

    for line in sys.stdin:
        src += line

    ast = phases.generate_ast(src, 0, "")
    if args.fold:
        (ast, _) = phases.generate_folded_ast(ast, None)

    tree = ast_to_rich_tree(ast)
    console.print(tree)

if __name__ == "__main__":
    main()
