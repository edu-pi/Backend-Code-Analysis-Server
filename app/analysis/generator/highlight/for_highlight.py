from msilib.schema import Condition


def get_highlight_attr(condition: Condition):
    return condition.changed_attr()
