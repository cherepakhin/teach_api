# import pytest
import unittest
from functools import reduce
from pydash import find


class FunctionalTest(unittest.TestCase):

  def test_map(self):
    name_lengths = map(len, ['Маша', 'Петя', 'Аня'])
    # print name_lengths
    self.assertEqual(list(name_lengths), [4, 4, 3])

    squares = map(lambda x: x * x, [2, 3, 4])
    self.assertEqual(list(squares), [4, 9, 16])

    def func_square(x):
      return x * x

    squares = map(func_square, [2, 3, 4])
    self.assertEqual(list(squares), [4, 9, 16])

  def test_map_multi_var(self):
    a = [2, 3, 4]
    b = [5, 6, 7]

    def func(x, y):
      return x + y
    summa = map(func, a, b)
    self.assertEqual(list(summa), [7, 9, 11])

    summa = map(lambda x, y: x + y, a, b)
    self.assertEqual(list(summa), [7, 9, 11])

  def test_reduce(self):
    summa = reduce(lambda a, x: a + x, [1, 2, 3])
    assert summa == 6

  def test_filter(self):
    more3 = filter(lambda x: x > 2, [1, 2, 3])
    assert list(more3) == [3]

  def test_gen(self):
    a = [1, 2, 3]
    b = [x for x in a]
    self.assertEqual(a, b)
    assert a == b
    assert a is not b

    a = [1, 2, 3]
    b = {x * 2 for x in a}
    self.assertEqual(b, {2, 4, 6})

  def test_gen_if(self):
    a = [1, 2, 3]
    b = [x for x in a if x == 2]
    self.assertEqual(b, [2])

  def test_if(self):
    a = [1, 2, 3]
    b = [x if x == 2 else x * 5 for x in a]
    self.assertEqual(b, [5, 2, 15])

  def test_find(self):
    arr = [
        {
            'employee_name': 'EMPLOYEE1',
            'feature_groups': [],
            'qty_all': 0,
            'qty_ok': 0
        },
        {
            'employee_name': 'EMPLOYEE2',
            'feature_groups': [],
            'qty_all': 0,
            'qty_ok': 0
        },
    ]
    elem = find(arr, {'employee_name': 'EMPLOYEE2'})
    assert elem == arr[1]

    elem = find(arr, {'employee_name': 'EMPLOYEE3'})
    assert elem is None
