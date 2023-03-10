from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

import pytest

from kentik_api.public.errors import DataFormatError, DeserializationError
from kentik_api.requests_payload.conversions import (
    convert,
    convert_list_or_none,
    convert_or_none,
    dict_from_json,
    enum_to_str,
    from_dict,
    list_from_json,
)


@dataclass
class _TestDataClass:
    name: str
    age: int
    hobby: Optional[str] = None


def test_from_dict_required_and_optional_fields_success() -> None:
    # given
    dic = {"name": "Liz", "age": 42, "hobby": "papercut"}

    # when
    obj = from_dict(data_class=_TestDataClass, data=dic)

    # then
    assert obj is not None
    assert obj.name == "Liz"
    assert obj.age == 42
    assert obj.hobby == "papercut"


def test_from_dict_required_optional_extra_fields_success() -> None:
    """Unexpected dictionary fields should just be ignored"""

    # given
    dic = {"name": "Liz", "age": 42, "hobby": "papercut", "origin": "Sierra Leone"}

    # when
    obj = from_dict(data_class=_TestDataClass, data=dic)

    # then
    assert obj is not None
    assert obj.name == "Liz"
    assert obj.age == 42
    assert obj.hobby == "papercut"


def test_from_dict_only_required_fields_success() -> None:
    # given
    dic = {"name": "Liz", "age": 42}

    # when
    obj = from_dict(data_class=_TestDataClass, data=dic)

    # then
    assert obj is not None
    assert obj.name == "Liz"
    assert obj.age == 42
    assert obj.hobby is None


def test_from_dict_missing_required_field_raises_error() -> None:
    # given
    dic = {"name": "Liz", "hobby": "papercut"}

    # when - then
    with pytest.raises(DeserializationError):
        _ = from_dict(data_class=_TestDataClass, data=dic)


def test_from_dict_different_casing_raises_error() -> None:
    # given
    dic = {"Name": "Liz", "Age": 42}

    # when - then
    with pytest.raises(DeserializationError):
        _ = from_dict(data_class=_TestDataClass, data=dic)


def test_dict_from_json_valid_document_success() -> None:
    # given
    json_string = """{"name": "Liz", "age": 42}"""

    # when
    dic = dict_from_json("TestDataClass", json_string)

    # then
    assert dic["name"] == "Liz"
    assert dic["age"] == 42


def test_dict_from_json_valid_document_with_root_success() -> None:
    # given
    json_string = """{"person":{"name": "Liz", "age": 42}}"""

    # when
    dic = dict_from_json("TestDataClass", json_string, "person")

    # then
    assert dic["name"] == "Liz"
    assert dic["age"] == 42


def test_dict_from_json_invalid_syntax_raises_error() -> None:
    # given
    json_string = """{"name": "Liz" "age": 42}"""  # missing comma between fields

    # when - then
    with pytest.raises(DeserializationError):
        _ = dict_from_json("TestDataClass", json_string)


def test_dict_from_json_invalid_type_raises_error() -> None:
    # given
    json_string = """[1, 2, 3]"""  # list instead of dict

    # when - then
    with pytest.raises(DeserializationError):
        _ = dict_from_json("TestDataClass", json_string)


def test_dict_from_json_missing_root_raises_error() -> None:
    # given
    json_string = """{"name": "Liz", "age": 42}"""  # data not under "person" root

    # when - then
    with pytest.raises(DeserializationError):
        _ = dict_from_json("TestDataClass", json_string, "person")


def test_list_from_json_valid_document_success() -> None:
    # given
    json_string = """[0, 1, 2]"""

    # when
    items = list_from_json("TestDataClass", json_string)

    # then
    assert items[0] == 0
    assert items[1] == 1
    assert items[2] == 2


def test_list_from_json_valid_document_with_root_success() -> None:
    # given
    json_string = """{"numbers":[0, 1, 2]}"""

    # when
    items = list_from_json("TestDataClass", json_string, "numbers")

    # then
    assert items[0] == 0
    assert items[1] == 1
    assert items[2] == 2


def test_list_from_json_invalid_syntax_raises_error() -> None:
    # given
    json_string = """[1 2, 3]"""  # missing comma between fields

    # when - then
    with pytest.raises(DeserializationError):
        _ = list_from_json("TestDataClass", json_string)


def test_list_from_json_invalid_type_raises_error() -> None:
    # given
    json_string = """{"name": "Liz", "age": 42}"""  # dict instead of list

    # when - then
    with pytest.raises(DeserializationError):
        _ = list_from_json("TestDataClass", json_string)


def test_list_from_json_missing_root_raises_error() -> None:
    # given
    json_string = """[1,2,3]"""  # data not under "numbers" root

    # when - then
    with pytest.raises(DeserializationError):
        _ = list_from_json("TestDataClass", json_string, "numbers")


def test_convert_provided_valid_data_format_returns_value() -> None:
    # given
    attr = "128"
    convert_func = int

    # when
    result = convert(attr, convert_func)

    # then
    assert result == 128


def test_convert_provided_invalid_data_format_raises_error() -> None:
    # given
    attr = "0x18"  # cant convert 0x18 to int with base 10
    convert_func = int

    # when - then
    with pytest.raises(DataFormatError):
        _ = convert(attr, convert_func)


def test_convert_or_none_provided_value_returns_value() -> None:
    # given
    attr = "128"
    convert_func = int

    # when
    result = convert_or_none(attr, convert_func)

    # then
    assert result == 128


def test_convert_or_none_provided_none_returns_none() -> None:
    # given
    attr = None
    convert_func = int

    # when
    result = convert_or_none(attr, convert_func)

    # then
    assert result is None


def test_convert_or_none_provided_empty_returns_none() -> None:
    # given
    attr: Dict[str, Any] = {}
    convert_func = dict

    # when
    result = convert_or_none(attr, convert_func)

    # then
    assert result is None


def test_convert_or_none_provided_invalid_data_format_raises_error() -> None:
    # given
    attr = "0x18"  # cant convert 0x18 to int with base 10
    convert_func = int

    # when - then
    with pytest.raises(DataFormatError):
        _ = convert_or_none(attr, convert_func)


def test_convert_list_or_none_provided_list_returns_list() -> None:
    # given
    attrs = ["256", "512"]
    convert_func = int

    # when
    result = convert_list_or_none(attrs, convert_func)

    # then
    assert result is not None
    assert result[0] == 256
    assert result[1] == 512


def test_convert_list_or_none_provided_none_returns_none() -> None:
    # given
    attrs = None
    convert_func = int

    # when
    result = convert_list_or_none(attrs, convert_func)

    # then
    assert result is None


def test_convert_list_or_none_provided_invalid_data_format_raises_error() -> None:
    # given
    attrs = ["17", "0x18"]  # cant convert 0x18 to int with base 10
    convert_func = int

    # when - then
    with pytest.raises(DataFormatError):
        convert_list_or_none(attrs, convert_func)


def test_enum_to_str() -> None:
    # given
    class Colors(Enum):
        red = "RED"
        green = "GREEN"
        blule = "BLUE"

    color = Colors.green

    # when
    color_name = enum_to_str(color)

    # then
    assert color_name == "GREEN"
