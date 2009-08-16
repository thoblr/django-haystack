from django.test import TestCase
from haystack.utils import Highlighter


class HighlighterTestCase(TestCase):
    def test_find_highlightable_words(self):
        document_1 = "This is a test of the highlightable words detection. This is only a test. Were this an actual emergency, your text would have exploded in mid-air."
        
        highlighter = Highlighter('this test')
        highlighter.text_block = document_1
        self.assertEqual(highlighter.find_highlightable_words())