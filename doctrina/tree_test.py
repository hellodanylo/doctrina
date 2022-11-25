from unittest import TestCase

from doctrina.tree import implode_tree, explode_tree

separator = "__"
tree_examples = [
    {"exploded": {"a": 1, "b": 2}, "imploded": {"a": 1, "b": 2}},
    {
        "exploded": {"a": {"b": 1}, "c": {"d": {"e": 2}}},
        "imploded": {"a__b": 1, "c__d__e": 2},
    },
]


class ExplodeImplodeTest(TestCase):
    def test_explode(self):
        for example in tree_examples:
            expected = example["exploded"]
            actual = explode_tree(example["imploded"], separator)
            self.assertEqual(expected, actual)

    def test_implode(self):
        for example in tree_examples:
            expected = example["imploded"]
            actual = implode_tree(example["exploded"], separator)
            self.assertEqual(expected, actual)

    def test_explode_implode_consistent(self):
        for example in tree_examples:
            expected = example["imploded"]
            actual = implode_tree(
                explode_tree(example["imploded"], separator), separator
            )
            self.assertEqual(expected, actual)

    def test_implode_explode_consistent(self):
        for example in tree_examples:
            expected = example["exploded"]
            actual = explode_tree(
                implode_tree(example["exploded"], separator), separator
            )
            self.assertEqual(expected, actual)