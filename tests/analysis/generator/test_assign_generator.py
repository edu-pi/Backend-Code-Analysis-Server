import ast
from unittest.mock import patch

import pytest

from app.analysis.element_manager import CodeElementManager
from app.analysis.generator.assign_generator import AssignGenerator
from tests.analysis.generator.data.test_assign_generator_data import create_param, create__parse_target_name_param, \
    create__calculate_node_param, create__create_assign_viz_steps_param


@pytest.fixture
def create_ast_assign():
    def _create_ast_assign(targets, value):
        return ast.Assign(targets=targets, value=value)

    return _create_ast_assign


"""
case1: a = 1
case2: a, b = 1, 2
case3: a = b = 1 + 2
"""


@pytest.mark.parametrize(
    "targets, value, expected_targets, expected_value, expected_expressions, expected_saved_variables",
    create_param())
def test_generate(create_ast_assign, targets, value, expected_targets, expected_value,
                  expected_expressions, expected_saved_variables):
    with patch.object(AssignGenerator, '_AssignGenerator__parse_target_names', return_value=expected_targets), \
            patch.object(AssignGenerator, '_AssignGenerator__calculate_node', return_value={"value": expected_value,
                                                                                            "expressions": expected_expressions}):
        elem_manager = CodeElementManager()
        AssignGenerator.generate(create_ast_assign(targets=targets, value=value), elem_manager)

    assert elem_manager.variables_value == expected_saved_variables


@pytest.mark.parametrize(
    "targets, value, expected_targets", create__parse_target_name_param())
def test__parse_target_names(create_ast_assign, elem_manager, targets, value, expected_targets):
    ast_assign = create_ast_assign(targets=targets, value=value)
    assign_generator = AssignGenerator(ast_assign, elem_manager)

    result = assign_generator._AssignGenerator__parse_target_names()

    assert result == expected_targets


@pytest.mark.parametrize("targets, value, expected_value, expected_expressions", create__calculate_node_param())
def test__calculate_node(create_ast_assign, elem_manager, targets, value, expected_value, expected_expressions):
    ast_assign = create_ast_assign(targets=targets, value=value)
    assign_generator = AssignGenerator(ast_assign, elem_manager)

    result = assign_generator._AssignGenerator__calculate_node()

    assert result == {"value": expected_value, "expressions": expected_expressions}


@pytest.mark.parametrize(
    "targets, value, expected_targets, expected_expressions, expected_viz",
    create__create_assign_viz_steps_param())
def test__create_assign_viz_steps(create_ast_assign, elem_manager, targets, value, expected_targets,
                                  expected_expressions, expected_viz):
    elem_manager.get_depth.return_value = 1
    ast_assign = create_ast_assign(targets=targets, value=value)
    assign_generator = AssignGenerator(ast_assign, elem_manager)

    result = assign_generator._AssignGenerator__create_assign_viz_steps(expected_targets, expected_expressions)

    assert result == expected_viz
