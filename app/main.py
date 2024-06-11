import ast

from fastapi import FastAPI

from app.analysis.code_analyzer import CodeAnalyzer
from app.analysis.element_manager import CodeElementManager
from app.utils import *
app = FastAPI()


@app.get("/")
def read_root():
    source_code = '''
d = 10
a = b, c = d + 10,  24
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
d = 10
a = b, c = d + 10,  24
        '''
    code_analyzer = CodeAnalyzer(CodeElementManager())

    parsed_ast = ast.parse(source_code)
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)

    return code_analyzer.visualize_code(parsed_ast)


if __name__ == "__main__":
    print(nodes_to_json(main()))
