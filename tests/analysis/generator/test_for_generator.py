from unittest.mock import MagicMock, patch

import ast
import pytest

from app.analysis.generator.for_generator import ForGenerator
from app.analysis.generator.parser.call_parser import NameParser
from app.analysis.element_manager import CodeElementManager
from tests.analysis.generator.parser.test_data.for_generator_data import data__get_identifier


@pytest.fixture
def elem_manager():
    mock = MagicMock(spec=CodeElementManager)
    mock.return_value.get_call_id.return_value = 5
    return mock


@pytest.fixture
def for_generator(elem_manager):
    # ForGenerator 인스턴스를 생성하는 함수를 반환
    def _create_generator(node):
        return ForGenerator(node, elem_manager)

    return _create_generator


@pytest.mark.parametrize("node, expect", data__get_identifier())
def test___get_identifiers(for_generator, node, expect):

    generator = for_generator(node)
    with patch.object(NameParser, 'parse', return_value=ast.Name(id='a', value=5, expressions=['a', '5'])):
        actual = generator._ForGenerator__get_identifiers()

        assert actual == expect

