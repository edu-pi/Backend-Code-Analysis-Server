from unittest.mock import MagicMock

import pytest

from app.visualize.analysis.element_manager import CodeElementManager


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.get_variable_value.return_value = 10
    return mock
