class Util:

    @staticmethod
    def get_var_type(var_value):
        if isinstance(var_value, list):
            return "list"

        return "variable"
