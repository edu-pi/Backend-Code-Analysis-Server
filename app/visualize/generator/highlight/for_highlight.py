from app.visualize.generator.model.models import ConditionViz


class ForHighlight:

    @staticmethod
    def get_highlight_attr(condition: ConditionViz):
        return condition.changed_attr()
