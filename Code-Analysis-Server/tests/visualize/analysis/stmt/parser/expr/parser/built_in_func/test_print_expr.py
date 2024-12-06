import pytest

from app.visualize.analysis.stmt.parser.expr.models.expr_obj import ConstantObj, BinopObj, PrintObj, ExprObj
from app.visualize.analysis.stmt.parser.expr.parser.built_in_func.print_expr import PrintExpr


@pytest.mark.parametrize(
    "args, keyword_arg_dict, expected",
    [
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",))],
            {},
            PrintObj(value="abc\n", expressions=("'abc'",)),
            id="print('abc'): success case",
        ),
        pytest.param(
            [BinopObj(value="'****'", expressions=("'*' * 4", "'****'"))],
            {},
            PrintObj(value="****\n", expressions=("'*' * 4", "'****'")),
            id="print('*' * 4): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",))],
            {"end": " "},
            PrintObj(value="abc ", expressions=("'abc'",)),
            id="print('abc', end=' '): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",)), ConstantObj(value="def", expressions=("'def'",))],
            {},
            PrintObj(value="abc def\n", expressions=("'abc' 'def'",)),
            id="print('abc', 'def'): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",)), ConstantObj(value="def", expressions=("'def'",))],
            {"sep": "-"},
            PrintObj(value="abc-def\n", expressions=("'abc'-'def'",)),
            id="print('abc', 'def', sep='-'): success case",
        ),
    ],
)
def test_parse(mocker, args: list[ExprObj], keyword_arg_dict: dict, expected: PrintObj):
    expected_key_word = {"sep": keyword_arg_dict.get("sep", " "), "end": keyword_arg_dict.get("end", "\n")}
    print(expected_key_word)

    mock_create_keywords = mocker.patch.object(PrintExpr, "_create_keywords", return_value=expected_key_word)
    mock_get_value = mocker.patch.object(PrintExpr, "_get_value", return_value=expected.value)
    mock_create_expressions = mocker.patch.object(PrintExpr, "_create_expressions", return_value=expected.expressions)

    result = PrintExpr.parse(args, keyword_arg_dict)

    assert isinstance(result, PrintObj)
    mock_create_keywords.assert_called_once_with(keyword_arg_dict)
    mock_get_value.assert_called_once_with(args, expected_key_word)
    mock_create_expressions.assert_called_once_with(args, expected_key_word)


@pytest.mark.parametrize(
    "keyword_arg_dict, expected",
    [
        pytest.param(
            {},
            {"sep": " ", "end": "\n"},
            id="default keyword: success case",
        ),
        pytest.param(
            {"sep": "-"},
            {"sep": "-", "end": "\n"},
            id="sep='-': success case",
        ),
        pytest.param(
            {"end": " "},
            {"sep": " ", "end": " "},
            id="end=' ': success case",
        ),
        pytest.param(
            {"sep": "-", "end": " "},
            {"sep": "-", "end": " "},
            id="sep='-', end=' ': success case",
        ),
    ],
)
def test_create_keywords(keyword_arg_dict: dict, expected: PrintObj):
    result = PrintExpr._create_keywords(keyword_arg_dict)

    assert isinstance(result, dict)
    assert result == expected


@pytest.mark.parametrize(
    "args, keyword_arg_dict, expected",
    [
        pytest.param(
            [ConstantObj(value="abc", expressions=("abc",))],
            {"sep": " ", "end": "\n"},
            ("abc",),
            id="print('abc'): success case",
        ),
        pytest.param(
            [BinopObj(value="'****'", expressions=("'*' * 4", "'****'"))],
            {"sep": " ", "end": "\n"},
            ("'*' * 4", "'****'"),
            id="print('*' * 4): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("abc",))],
            {"sep": " ", "end": " "},
            ("abc",),
            id="print('abc', end=' '): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("abc",)), ConstantObj(value="def", expressions=("def",))],
            {"sep": " ", "end": "\n"},
            ("abc def",),
            id="print('abc', 'def'): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("abc",)), ConstantObj(value="def", expressions=("def",))],
            {"sep": "-", "end": "\n"},
            ("abc-def",),
            id="print('abc', 'def', sep='-'): success case",
        ),
    ],
)
def test_create_expressions(args: list[ExprObj], keyword_arg_dict: dict, expected: tuple[str]):
    result = PrintExpr._create_expressions(args, keyword_arg_dict)

    assert result == expected


@pytest.mark.parametrize(
    "args, keyword_arg_dict, expected",
    [
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",))],
            {"sep": " ", "end": "\n"},
            "abc\n",
            id="print('abc'): success case",
        ),
        pytest.param(
            [BinopObj(value="'****'", expressions=("'*' * 4", "'****'"))],
            {"sep": " ", "end": "\n"},
            "'****'\n",
            id="print('*' * 4): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",))],
            {"sep": " ", "end": " "},
            "abc ",
            id="print('abc', end=' '): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",)), ConstantObj(value="def", expressions=("'def'",))],
            {"sep": " ", "end": "\n"},
            "abc def\n",
            id="print('abc', 'def'): success case",
        ),
        pytest.param(
            [ConstantObj(value="abc", expressions=("'abc'",)), ConstantObj(value="def", expressions=("'def'",))],
            {"sep": "-", "end": "\n"},
            "abc-def\n",
            id="print('abc', 'def', sep='-'): success case",
        ),
    ],
)
def test_get_value(args: list[ExprObj], keyword_arg_dict: dict, expected: PrintObj):
    PrintExpr._get_value(args, keyword_arg_dict)
