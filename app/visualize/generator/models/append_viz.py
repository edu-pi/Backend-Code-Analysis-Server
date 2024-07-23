from dataclasses import dataclass, field

from app.visualize.generator.models.variable_vlz import Variable


@dataclass(frozen=True)
class AppendViz:
    variable: Variable
    type: str = field(default="append", init=False)
