class Util:

    @staticmethod
    def get_var_type(var_value, obj_type: str):
        if obj_type in ("binop", "constant"):
            return "variable"

        elif obj_type == "name":
            if isinstance(var_value, list):
                return "list"

            else:
                return "variable"

        elif obj_type == "list":
            return "list"

        else:
            return obj_type
