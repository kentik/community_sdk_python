import json
from typing import TypeVar, Type, Dict, Any, Optional, List, Iterable
import dacite
from kentik_api.public.errors import DeserializationError, DataFormatError

T = TypeVar("T")
Data = Dict[str, Any]


def from_dict(data_class: Type[T], data: Data) -> T:
    """ Wrapper converting dacite errors into kentik library errors """
    try:
        return dacite.from_dict(data_class=data_class, data=data)
    except dacite.DaciteError as err:
        raise DeserializationError(data_class.__name__, str(err))


def from_json(class_name: str, json_string: str, root: str = "") -> Dict[str, Any]:
    """
    Wrapper converting json errors into kentik library errors
    root - use it to extract data that is nested under a root object eg. "interface": {...}
    """

    try:
        return json.loads(json_string) if root == "" else json.loads(json_string)[root]
    except json.JSONDecodeError as err:
        raise DeserializationError(class_name, str(err))
    except KeyError as err:
        raise DeserializationError(class_name, str(err))


def convert_or_none(attr: Any, convert_func) -> Optional[Any]:
    """ Convert if input is not None, else just return None. Convert exceptions to library specific """
    if attr is None or attr == {}:
        return None
    try:
        return convert_func(attr)
    except Exception as err:
        raise DataFormatError(str(err))


def convert_list_or_none(items: Optional[Iterable[Any]], convert_func) -> Optional[List[Any]]:
    """ Convert list if input list is not None, else just return None. Convert exceptions to library specific """
    if items is None:
        return None
    try:
        return [convert_func(item) for item in items]
    except Exception as err:
        raise DataFormatError(str(err))
