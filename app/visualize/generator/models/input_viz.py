from dataclasses import dataclass, field


@dataclass(frozen=True)
class InputViz:
    id: int
    depth: int
    expr: str
    console: str | None
    code: str
    type: str = field(default="input", init=False)
