from dataclasses import dataclass, field


@dataclass(frozen=True)
class FlowControlViz:
    id: str
    depth: int
    expr: str
    highlights: []
    type: str = field(default="flowControl", init=False)
