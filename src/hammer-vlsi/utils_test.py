#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Utility tests for hammer-vlsi.
#
#  See LICENSE for licence details.

from typing import Dict, Tuple, List, Optional, Union

from hammer_utils import topological_sort, get_or_else, optional_map, assert_function_type

import unittest


class UtilsTest(unittest.TestCase):
    def test_topological_sort(self) -> None:
        """
        Test that topological sort works properly.
        """

        # tuple convention: (outgoing, incoming)
        graph = {
            "1": (["4"], []),
            "2": (["4"], []),
            "3": (["5", "6"], []),
            "4": (["7", "5"], ["1", "2"]),
            "5": (["8"], ["4", "3"]),
            "6": ([], ["3"]),
            "7": (["8"], ["4"]),
            "8": ([], ["7", "5"])
        }  # type: Dict[str, Tuple[List[str], List[str]]]

        self.assertEqual(topological_sort(graph, ["1", "2", "3"]), ["1", "2", "3", "4", "6", "7", "5", "8"])

    def test_get_or_else(self) -> None:
        self.assertEqual(get_or_else(None, "default"), "default")
        self.assertEqual(get_or_else(None, ""), "")
        self.assertEqual(get_or_else("Hello World", "default"), "Hello World")
        self.assertEqual(get_or_else("Hello World", ""), "Hello World")

    def test_optional_map(self) -> None:
        num_to_str = lambda x: str(x) + "_str"
        str_to_num = lambda x: int(x) * 10
        self.assertEqual(optional_map(None, num_to_str), None)
        self.assertEqual(optional_map(10, num_to_str), "10_str")
        self.assertEqual(optional_map(0, num_to_str), "0_str")
        self.assertEqual(optional_map(None, str_to_num), None)
        self.assertEqual(optional_map("88", str_to_num), 880)
        self.assertNotEqual(optional_map("88", str_to_num), "880")
        self.assertEqual(optional_map("42", str_to_num), 420)

    def test_check_function_type(self) -> None:
        def test1(x: int) -> str:
            return str(x + 5)

        assert_function_type(test1, [int], str)

        def test2(a: int, b: float) -> None:
            print("{a}{b}".format(a=a, b=b))

        assert_function_type(test2, [int, float], None)  # type: ignore

        def test3(a: int, b: int) -> List[int]:
            return [a, b]

        assert_function_type(test3, [int, int], List[int])

        def test4(a: int, b: int) -> List[int]:
            return [a, b]

        assert_function_type(test4, [int, int], List[int])

        # Check that dict == typing.Dict, etc.
        def test5(a: int) -> dict:
            return {"a": a}

        assert_function_type(test5, [int], Dict)

        # Check that dict == typing.Dict, etc.
        def test6(a: int) -> Optional[dict]:
            return {"a": a}

        assert_function_type(test6, [int], Optional[Dict])

        # Check that Union types get handled properly.
        def test7(a: Union[int, float]) -> Union[bool, str]:
            return str(a)

        assert_function_type(test7, [Union[int, float]], Union[bool, str])

        # Check that stringly-typed annotations work.
        def test8(a: "int") -> "list":
            return [a + a]

        assert_function_type(test8, ["int"], "list")  # type: ignore
        assert_function_type(test8, ["int"], list)  # type: ignore
        assert_function_type(test8, [int], "list")  # type: ignore
        assert_function_type(test8, [int], list)

        with self.assertRaises(TypeError):
            # Different # of arguments
            assert_function_type(test1, [int, int], str)
        with self.assertRaises(TypeError):
            # Different return type
            assert_function_type(test1, [int], bool)
        with self.assertRaises(TypeError):
            # Different argument type
            assert_function_type(test1, [str], str)
        with self.assertRaises(TypeError):
            # Different # of arguments and different return type
            assert_function_type(test3, [int], bool)
        with self.assertRaises(TypeError):
            # Entirely different
            assert_function_type(test3, [], dict)


if __name__ == '__main__':
     unittest.main()
