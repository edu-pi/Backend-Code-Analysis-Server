from dataclasses import dataclass, field


@dataclass(frozen=True)
class PrintViz:
    id: int
    depth: int
    expr: str
    highlights: []
    console: str | None
    code: str
    type: str = field(default="print", init=False)
