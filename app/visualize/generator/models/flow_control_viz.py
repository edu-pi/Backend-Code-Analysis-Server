from dataclasses import dataclass, field


@dataclass(frozen=True)
class FlowControlViz:
    id: int
    depth: int
    expr: str
    highlights: []
    code: str
    type: str = field(default="flowControl", init=False)
