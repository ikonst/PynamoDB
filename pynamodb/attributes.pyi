from typing import Any, Callable, Dict, Generic, Iterable, List, Mapping, Optional, Text, Type, TypeVar, Union, Set, overload

from datetime import datetime

from pynamodb.expressions.condition import (
    BeginsWith, Between, Comparison, Contains, NotExists, Exists, In
)
from pynamodb.expressions.operand import _ListAppend
from pynamodb.expressions.update import (
    AddAction, DeleteAction, RemoveAction, SetAction
)
from pynamodb.models import Model


_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')
_MT = TypeVar('_MT', bound='MapAttribute')

_A = TypeVar('_A', bound='Attribute')


class Attribute(Generic[_T]):
    attr_name: Optional[Text]
    attr_type: Text
    null: bool
    default: Any
    is_hash_key: bool
    is_range_key: bool
    def __init__(self, hash_key: bool = ..., range_key: bool = ..., null: Optional[bool] = ..., default: Optional[Union[_T, Callable[..., _T]]] = ..., attr_name: Optional[Text] = ...) -> None: ...
    def __set__(self, instance: Any, value: Optional[_T]) -> None: ...
    def serialize(self, value: Any) -> Any: ...
    def deserialize(self, value: Any) -> Any: ...
    def get_value(self, value: Any) -> Any: ...
    def is_type(self) -> Any: ...
    def __eq__(self, other: Any) -> Comparison: ...  # type: ignore
    def __ne__(self, other: Any) -> Comparison: ...  # type: ignore
    def __lt__(self, other: Any) -> Comparison: ...
    def __le__(self, other: Any) -> Comparison: ...
    def __gt__(self, other: Any) -> Comparison: ...
    def __ge__(self, other: Any) -> Comparison: ...
    def between(self, lower: Any, upper: Any) -> Between: ...
    def is_in(self, *values: Any) -> In: ...
    def exists(self) -> Exists: ...
    def does_not_exist(self) -> NotExists: ...
    def startswith(self, prefix: str) -> BeginsWith: ...
    def contains(self, item: Any) -> Contains: ...
    def set(self, value: Any) -> SetAction: ...
    def remove(self) -> RemoveAction: ...
    def add(self, *values: Any) -> AddAction: ...
    def delete(self, *values: Any) -> DeleteAction: ...
    def append(self, other: Any) -> _ListAppend: ...
    def prepend(self, other: Any) -> _ListAppend: ...


class AttributeContainer(object):
    attribute_values: Dict[Text, Any]
    def __init__(**attributes: Attribute) -> None: ...


class SetMixin(object):
    def serialize(self, value): ...
    def deserialize(self, value): ...

class BinaryAttribute(Attribute[bytes]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> bytes: ...

class BinarySetAttribute(SetMixin, Attribute[Set[bytes]]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> Set[bytes]: ...

class UnicodeSetAttribute(SetMixin, Attribute[Set[Text]]):
    def element_serialize(self, value: Any) -> Any: ...
    def element_deserialize(self, value: Any) -> Any: ...
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> Set[Text]: ...

class UnicodeAttribute(Attribute[Text]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> Text: ...

class JSONAttribute(Attribute[Any]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> Any: ...

class LegacyBooleanAttribute(Attribute[bool]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> bool: ...

class BooleanAttribute(Attribute[bool]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> bool: ...

class NumberSetAttribute(SetMixin, Attribute[Set[float]]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> Set[float]: ...

class NumberAttribute(Attribute[float]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> float: ...


class UTCDateTimeAttribute(Attribute[datetime]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> datetime: ...

class NullAttribute(Attribute[None]):
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> None: ...

class MapAttributeMeta(type):
    def __init__(cls, name, bases, attrs) -> None: ...

class MapAttribute(Generic[_KT, _VT], Attribute[Mapping[_KT, _VT]], metaclass=MapAttributeMeta):
    attribute_values: Any
    def __init__(self, hash_key: bool = ..., range_key: bool = ..., null: Optional[bool] = ..., default: Optional[Union[Any, Callable[..., Any]]] = ..., attr_name: Optional[Text] = ..., **attrs) -> None: ...
    def __iter__(self) -> Iterable[_VT]: ...
    def __getattr__(self, attr: str) -> _VT: ...
    def __getitem__(self, item: _KT) -> _VT: ...
    def __set__(self, instance: Any, value: Union[None, MapAttribute[_KT, _VT], Mapping[_KT, _VT]]) -> None: ...
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self: _MT, instance: Any, owner: Any) -> _MT: ...
    def is_type_safe(self, key: Any, value: Any) -> bool: ...
    def validate(self) -> bool: ...

class ListAttribute(Generic[_T], Attribute[List[_T]]):
    element_type: Any
    def __init__(self, hash_key: bool = ..., range_key: bool = ..., null: Optional[bool] = ..., default: Optional[Union[Any, Callable[..., Any]]] = ..., attr_name: Optional[Text] = ..., of: Optional[Type[_T]] = ...) -> None: ...
    @overload
    def __get__(self: _A, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Any, owner: Any) -> List[_T]: ...

class _NullableAttributeWrapper(Generic[_A, _T]):
    @overload
    def __get__(self, instance: None, owner: Any) -> _A: ...
    @overload
    def __get__(self, instance: Model, owner: Any) -> Optional[_T]: ...

DESERIALIZE_CLASS_MAP: Dict[Text, Attribute]
SERIALIZE_CLASS_MAP: Dict[Type, Attribute]
SERIALIZE_KEY_MAP: Dict[Type, Text]


def _get_class_for_serialize(value: Optional[Any]) -> Attribute: ...
