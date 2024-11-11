from dataclasses import dataclass


@dataclass(frozen=True)
class InputViz:
    id: int
    depth: int
    expr: str
    console: str | None
    code: str
    type: str
