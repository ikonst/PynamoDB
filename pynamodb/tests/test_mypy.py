"""
Note: The expected error strings may change in a future version of mypy.
      Please update as needed.
"""
import pytest

pytest.importorskip('mypy')  # we only install mypy in python>=3.6 tests
pytest.register_assert_rewrite('pynamodb.tests.mypy_helpers')
from .mypy_helpers import assert_mypy_output  # noqa


def test_model_query():
    assert_mypy_output("""
    from pynamodb.attributes import NumberAttribute
    from pynamodb.models import Model

    class MyModel(Model):
        my_attr = NumberAttribute()

    # test hash key types
    MyModel.query(123)
    MyModel.query('123')
    MyModel.query(12.3)
    MyModel.query(b'123')
    MyModel.query((1, 2, 3))
    MyModel.query({'1': '2'})  # E: Argument 1 to "query" of "Model" has incompatible type "Dict[str, str]"; expected "Union[str, bytes, float, Tuple[Any, ...]]"

    # test conditions
    MyModel.query(123, range_key_condition=(MyModel.my_attr == 5), filter_condition=(MyModel.my_attr == 5))

    # test conditions are optional
    MyModel.query(123, range_key_condition=None, filter_condition=None)
    """)  # noqa: E501


def test_number_attribute():
    assert_mypy_output("""
    from pynamodb.attributes import NumberAttribute
    from pynamodb.models import Model

    class MyModel(Model):
        my_attr = NumberAttribute()

    reveal_type(MyModel.my_attr)  # E: Revealed type is 'pynamodb.attributes.NumberAttribute*'
    reveal_type(MyModel().my_attr)  # E: Revealed type is 'builtins.float'
    """)


def test_unicode_attribute():
    assert_mypy_output("""
    from pynamodb.attributes import UnicodeAttribute
    from pynamodb.models import Model

    class MyModel(Model):
        my_attr = UnicodeAttribute()

    reveal_type(MyModel.my_attr)  # E: Revealed type is 'pynamodb.attributes.UnicodeAttribute*'
    reveal_type(MyModel().my_attr)  # E: Revealed type is 'builtins.str'
    """)


def test_map_attribute():
    assert_mypy_output("""
    from pynamodb.attributes import MapAttribute, UnicodeAttribute
    from pynamodb.models import Model

    class MySubMap(MapAttribute):
        s = UnicodeAttribute()

    class MyMap(MapAttribute):
        m2 = MySubMap()

    class MyModel(Model):
        m1 = MyMap()

    reveal_type(MyModel.m1)  # E: Revealed type is '__main__.MyMap'
    reveal_type(MyModel().m1)  # E: Revealed type is '__main__.MyMap'
    reveal_type(MyModel.m1.m2)  # E: Revealed type is '__main__.MySubMap'
    reveal_type(MyModel().m1.m2)  # E: Revealed type is '__main__.MySubMap'
    reveal_type(MyModel.m1.m2.s)  # E: Revealed type is 'builtins.str'
    reveal_type(MyModel().m1.m2.s)  # E: Revealed type is 'builtins.str'

    reveal_type(MyMap.m2)  # E: Revealed type is '__main__.MySubMap'
    reveal_type(MyMap().m2)  # E: Revealed type is '__main__.MySubMap'

    reveal_type(MySubMap.s)  # E: Revealed type is 'pynamodb.attributes.UnicodeAttribute*'
    reveal_type(MySubMap().s)  # E: Revealed type is 'builtins.str'
    """)


def test_list_attribute():
    assert_mypy_output("""
    from pynamodb.attributes import ListAttribute, MapAttribute, UnicodeAttribute
    from pynamodb.models import Model

    class MyMap(MapAttribute):
        my_sub_attr = UnicodeAttribute()

    class MyModel(Model):
        my_list = ListAttribute(of=MyMap)

    reveal_type(MyModel.my_list)  # E: Revealed type is 'pynamodb.attributes.ListAttribute[__main__.MyMap]'
    reveal_type(MyModel().my_list)  # E: Revealed type is 'builtins.list[__main__.MyMap*]'
    reveal_type(MyModel.my_list[0])  # E: Revealed type is 'Any'  # E: Value of type "ListAttribute[MyMap]" is not indexable
    reveal_type(MyModel().my_list[0].my_sub_attr)  # E: Revealed type is 'builtins.str'
    """)
