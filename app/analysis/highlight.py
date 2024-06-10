from app.analysis.models import Condition


def for_highlight(condition: Condition):
    return condition.changed_attr()
