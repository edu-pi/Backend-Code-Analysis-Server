import ast
from typing import Union

from fastapi import FastAPI

from app.analysis import code_analyzer, element_manager
from app.analysis.parser import g_elem_manager

app = FastAPI()


@app.get("/")
def read_root():
    source_code = '''
a = 20
for i in range(0, a, 2):
    print("*" * (i+1))
            '''
    parsed_ast = ast.parse(source_code)
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)
    code_analyzer.visualize_code(parsed_ast)
    return g_elem_manager.get_all_step()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def test():
    source_code = '''
a = 20
for i in range(0, a, 2):
    print("*" * (i+1))
    '''
    parsed_ast = ast.parse(source_code)
    print("AST 구조:")
    code_analyzer.print_ast(parsed_ast)
    code_analyzer.visualize_code(parsed_ast)
    return g_elem_manager.get_all_step()


if __name__ == "__main__":
    print(test())
