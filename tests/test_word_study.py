from unittest import TestCase
from core.word_study import WordStudy


class TestWordStudy(TestCase):
    def setUp(self) -> None:
        self.word_study = WordStudy()
        self.words = self.word_study.words

    def test_get_word(self):
        self.assertEqual(self.word_study.get_next_word(), self.words[0])
        self.assertEqual(self.word_study.get_next_word(), self.words[1])
        self.word_study.get_next_word()
        self.assertEqual(self.word_study.get_pre_word(), self.words[1])
        self.assertEqual(self.word_study.get_pre_word(), self.words[0])