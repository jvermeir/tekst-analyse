import unittest
import text_analyzer

class TestTextAnalyzer(unittest.TestCase):
    def test_is_maar_want_sentence_returns_sentence_with_key_words_only(self):
        want_sentence = 'this is a, want sentence'
        maar_sentence = 'this is a maar, sentence'
        should_not_appear_sentence = 'this should not appear in result'
        partial_match_should_not_appear = 'met zijn verwant, de (noordelijke)'
        als_dan_sentence = 'this is a als, some more words, dan sentecne'
        zonder_dat_sentence = 'this is a zonder, some more words, dat sentecne'


        self.assertTrue(text_analyzer.is_conjunction_sentence(want_sentence), 'want sentence should be in result')
        self.assertTrue(text_analyzer.is_conjunction_sentence(maar_sentence), 'maar sentence should be in result')
        self.assertFalse(text_analyzer.is_conjunction_sentence(should_not_appear_sentence), 'should not appear sentence should not be in result')
        self.assertFalse(text_analyzer.is_conjunction_sentence(partial_match_should_not_appear), 'partial match should not be in result')
        self.assertTrue(text_analyzer.is_conjunction_sentence(als_dan_sentence), 'als dan sentence should be in result')
        self.assertTrue(text_analyzer.is_conjunction_sentence(zonder_dat_sentence), 'zonder dat sentence should be in result')

if __name__ == '__main__':
    unittest.main()
