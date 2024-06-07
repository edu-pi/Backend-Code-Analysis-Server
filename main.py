import ast
from typing import Union

from fastapi import FastAPI

from app.analysis import code_analyzer
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
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)

    code_analyzer.visualize_code(parsed_ast)
    return CodeElementManager.get_all_step()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


code = '''
a=5
for i in range (a) :
    print('*'* (i+1))
'''


def test():
    source_code = '''
a = 10
b = a + 10
c = a + b + 10
        '''
    parsed_ast = ast.parse(code)
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)

    code_analyzer.visualize_code(parsed_ast)
    return CodeElementManager.get_all_step()


if __name__ == "__main__":
    print(nodes_to_json(test()))
