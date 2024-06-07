import ast

from fastapi import FastAPI

from app.analysis.code_analyzer import CodeAnalyzer
from app.analysis.element_manager import CodeElementManager
from app.utils import *
app = FastAPI()


@app.get("/")
def read_root():
    source_code = '''
a = 10
b = a + 10
c = a + b + 10
            '''
    parsed_ast = ast.parse(source_code)
    analyzer = CodeAnalyzer()
    print("AST 구조:")
    analyzer.print_ast(parsed_ast)

    g_elem_manager = CodeElementManager()
    analyzer.visualize_code(parsed_ast, g_elem_manager)
    return g_elem_manager.get_all_step()


code = '''
a=5
for i in range (2) :
    print('*'* (i+1))
    for j in range (100, 102) :
        print('*'* (i+1))
'''


def main():
    analyzer = CodeAnalyzer()
    source_code = '''
a = 10
b = a + 10
c = a + b + 10
        '''
    parsed_ast = ast.parse(code)
    print("AST 구조:")
    analyzer.print_ast(parsed_ast)

    g_elem_manager = CodeElementManager()
    analyzer.visualize_code(parsed_ast, g_elem_manager)
    return g_elem_manager.get_all_step()


if __name__ == "__main__":
    print(nodes_to_json(main()))
