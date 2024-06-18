import ast


def create_ast_node(code):
    # 코드를 ast 노드로 변환하는 함수를 반환
    return ast.parse(code).body[0]


def data__get_identifier():
    node = [create_ast_node('''
for i in range(3):
    pass
    '''),
            create_ast_node('''
for i in range(1,5,2):
    pass
        '''),
            create_ast_node('''
for i in range(1,a):
    pass
            '''),
            ]

    expected = [[3], [1, 5, 2], [1, 5]]

    return list(zip(node, expected))


def data_parse_test():
    node = create_ast_node('''
for i in range(3):
    i = i + 1
    ''')

    expected = [
        {
            "id": 1,
            "depth": 1,
            "condition": {
                "target": "i",
                "cur": 0,
                "start": 0,
                "end": 3,
                "step": 1
            },
            "highlight": [
                "target",
                "cur",
                "start",
                "end",
                "step"
            ],
            "type": "for"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "i + 1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "0 + 1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "id": 1,
            "depth": 1,
            "condition": {
                "target": "i",
                "cur": 1,
                "start": 0,
                "end": 3,
                "step": 1
            },
            "highlight": [
                "cur"
            ],
            "type": "for"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "i + 1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "1 + 1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "2",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "id": 1,
            "depth": 1,
            "condition": {
                "target": "i",
                "cur": 2,
                "start": 0,
                "end": 3,
                "step": 1
            },
            "highlight": [
                "cur"
            ],
            "type": "for"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "i + 1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "2 + 1",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        },
        {
            "variables": [
                {
                    "depth": 2,
                    "expr": "3",
                    "name": "i"
                }
            ],
            "type": "assignViz"
        }
    ]

    return node, expected
