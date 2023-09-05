from collections import ChainMap
from unittest import TestCase

from conf_parsers.items import absolute_url


class TestModels(TestCase):
    def test_relative_to_absolute_url_no_context(self):
        context = ChainMap({'response': None, 'selector': None, 'item': {}}, {})
        with self.assertRaises(ValueError):
            absolute_url('111', context)
