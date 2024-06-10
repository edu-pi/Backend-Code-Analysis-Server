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
    code_analyzer = CodeAnalyzer(CodeElementManager())

    parsed_ast = ast.parse(source_code)
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)

    return code_analyzer.visualize_code(parsed_ast)


code = '''
a=5
for i in range (a) :
    print('*'* (i+1))
'''


def main():
    source_code = '''
a = 10
b = a
c = b + 10
d = e = c + 100

        '''
    code_analyzer = CodeAnalyzer(CodeElementManager())

    parsed_ast = ast.parse(source_code)
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)

    return code_analyzer.visualize_code(parsed_ast)


if __name__ == "__main__":
    print(nodes_to_json(main()))
