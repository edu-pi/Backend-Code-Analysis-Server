from app.analysis.models import ConditionViz


def get_highlight_attr(condition: ConditionViz):
    return condition.changed_attr()
