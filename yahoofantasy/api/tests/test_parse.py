from pathlib import Path
from unittest import TestCase
from yahoofantasy.api.parse import (
    parse_response,
    get_value,
    as_list,
    from_response_object,
)


class TestParse(TestCase):
    def test_get_value(self):
        """get_value turns XML response into attribute objects"""
        resp_file = Path(__file__).parent / "sample_data" / "example.xml"
        parsed = parse_response(resp_file.read_text())
        values = get_value(parsed)
        root = values.fantasy_content.root

        self.assertEqual(root.individual_item, "item value")
        self.assertEqual(root.list_of_items.item_object[0].name, "Item 1")

    def test_as_list(self):
        self.assertEqual(as_list(5), [5])
        self.assertEqual(as_list([5]), [5])

    def test_from_response_object(self):
        class Obj(object):
            @property
            def protected_prop(self):
                """Don't set existing properties/methods"""
                return 4

            def protected_method(self):
                """Don't set existing properties/methods"""
                return 5

        obj = Obj()
        from_response_object(
            obj,
            {
                "key1": "value1",
                "nested": {
                    "key2": "value2",
                },
                "protected_prop": "ignored",
                "protected_method": "ignored",
            },
        )
        self.assertEqual(obj.key1, "value1")
        self.assertEqual(obj.nested.key2, "value2")
        self.assertEqual(obj.protected_prop, 4)
        self.assertEqual(obj.protected_method(), 5)
