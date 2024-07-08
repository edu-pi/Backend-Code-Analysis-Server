from dataclasses import dataclass


@dataclass(frozen=True)
class AssignViz:
    variables: list
    type: str = "assignViz"


"""
    @ list: Variable 리스트
    @ type: 타입````
"""
