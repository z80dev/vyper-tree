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
parser.add_argument('--fold', action="store_true", help="print folded AST")
parser.add_argument('--deployment-ir', action="store_true", help="print deployment IR", dest="deployment_ir")
parser.add_argument('--runtime-ir', action="store_true", help="print runtime IR", dest="runtime_ir")

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

def print_ast(src, console):
    ast = phases.generate_ast(src, 0, "")
    ast = phases.generate_unfolded_ast(ast, None)
    tree = ast_to_rich_tree(ast)
    console.print(tree)

def print_folded_ast(src, console):
    ast = phases.generate_ast(src, 0, "")
    folded_ast = phases.generate_folded_ast(ast, None)
    tree = ast_to_rich_tree(ast)
    console.print(tree)

def print_deployment_ir(src, console):
    ast = phases.generate_ast(src, 0, "")
    (folded_ast, _) = phases.generate_folded_ast(ast, None)
    gctx = phases.generate_global_context(folded_ast, None)
    depl_ir, runtime_ir, funcsigs = phases.generate_ir_nodes(gctx, None)
    print(depl_ir)

def print_ir(src, console):
    ast = phases.generate_ast(src, 0, "")
    (folded_ast, _) = phases.generate_folded_ast(ast, None)
    gctx = phases.generate_global_context(folded_ast, None)
    depl_ir, runtime_ir, funcsigs = phases.generate_ir_nodes(gctx, None)
    print(runtime_ir)

def main():
    pretty.install()

    args = parser.parse_args()

    console = Console(color_system="truecolor", force_terminal=args.term)
    src = ""

    for line in sys.stdin:
        src += line

    if args.runtime_ir:
        print_ir(src, console)
        return
    if args.deployment_ir:
        print_deployment_ir(src, console)
        return
    if args.fold:
        print_folded_ast(src, console)
        return
    else:
        print_unfolded_ast(src, console)

if __name__ == "__main__":
    main()
