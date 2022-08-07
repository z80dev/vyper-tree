from vyper_tree import main
from vyper.compiler import phases
from rich.console import Console
from rich import pretty
import sys

pretty.install()

console = Console(color_system="truecolor", force_terminal=True)
src = ""

for line in sys.stdin:
    src += line

ast = phases.generate_ast(src, 0, "")

tree = main.ast_to_rich_tree(ast)
console.print(tree)
