from app.visualize.generator.model.for_viz import ForConditionViz


class ForHighlight:

    @staticmethod
    def get_highlight_attr(condition: ForConditionViz):
        return condition.changed_attr()
