from app.visualize.generator.model.models import ForConditionViz


class ForHighlight:

    @staticmethod
    def get_highlight_attr(condition: ForConditionViz):
        return condition.changed_attr()
