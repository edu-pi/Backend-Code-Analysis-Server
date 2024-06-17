from msilib.schema import Condition


def for_highlight(condition: Condition):
    return condition.changed_attr()
