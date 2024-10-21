from dataclasses import dataclass, field


@dataclass(frozen=True)
class AssignViz:
    variables: list
    callStackName: str
    type: str = field(default="assign", init=False)


"""
    @ list: Variable 리스트
    @ type: 타입````
"""
