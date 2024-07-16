from dataclasses import dataclass

from app.visualize.generator.models.variable_vlz import Variable


@dataclass(frozen=True)
class AppendViz:
    variable: Variable
    type: str = "appendViz"
