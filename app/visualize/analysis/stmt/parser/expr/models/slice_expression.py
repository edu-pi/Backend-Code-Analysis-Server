from dataclasses import dataclass


@dataclass(frozen=True)
class SliceExpression:
    upper: str | None = None
    lower: str | None = None
    step: str | None = None

    def __str__(self):
        if self.step is None:
            return f"[{self.lower or ''}:{self.upper or ''}]"
        else:
            return f"[{self.lower or ''}:{self.upper or ''}:{self.step or ''}]"
