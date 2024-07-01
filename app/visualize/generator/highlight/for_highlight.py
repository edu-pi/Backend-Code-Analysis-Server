from app.visualize.generator.model.models import ConditionViz


class ForHighlighter:

    @staticmethod
    def get_highlight_attr(condition: ConditionViz):
        return condition.changed_attr()
