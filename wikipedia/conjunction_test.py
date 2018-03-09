import unittest
import conjunction


class TestConjunction(unittest.TestCase):

    def test_conjunction_is_constructed_from_sentence(self):
        try:
            sentence_contains_conjunction = "Ik neem geen paraplu mee hoewel het regent vandaag."
            c = conjunction.Conjunction(sentence_contains_conjunction, "")
            self.assertEqual("hoewel", c.word)
            self.assertTrue("Ik neem geen paraplu mee", c.left)
            self.assertTrue("het regent vandaag", c.right)
        except Exception as e:
            print (e)

    def test_conjunction_is_constructed_from_2_sentences(self):
        try:
            sentence_starts_with_conjunction = "Daarom neem ik een paraplu mee"
            previous_sentence = "Het regent vandaag."

            c = conjunction.Conjunction(sentence_starts_with_conjunction, previous_sentence)

            self.assertEqual("daarom", c.word)
            self.assertTrue("Het regent vandaag", c.left)
            self.assertTrue("neem ik een paraplu mee", c.right)
        except Exception as e:
            print (e)

    def test_toJson(self):
        cs = [conjunction.Conjunction("deze daarom zonder", "vorige zin")
            , conjunction.Conjunction("deze dus niet", "vorige zin")
            , conjunction.Conjunction("want samen met...", "vorige zin")
              ]
        text = conjunction.Conjunction.toJson(cs)

        self.assertIn('{{"right": "zonder", "word": "daarom", "left": "deze"},{"right": "samen met", "word": "want", "left": "vorige zin"}}', text)


if __name__ == '__main__':
    unittest.main()

# Obsolete? definitions of conjunction_words? Conjunction class now contains a subset

conjunctions_words = {
    "en", "of", "alsof", "maar", "doch", "noch", "dus", "derhalve", "daarom", "doordat", "door",
    "omdat", "aangezien", "want", "daar", "dewijl", "doordien", "naardien", "nademaal", "overmits",
    "terwijl", "indien", "ingeval", "zo", "zodat", "opdat", "sinds", "sedert", "nadat", "dat",
    "vooraleer", "voor", "aleer", "eer", "voordat", "totdat", "toen", "zodra", "als", "zoals",
    "behalve", "al", "alhoewel", "hoewel", "ofschoon", "schoon", "mits", "tenware", "tenzij", "naar",
    "naargelang", "naarmate", "wanneer", "vermits", "wijl"
}
als_dan_pattern = r"als.*?dan"
zonder_dat_pattern = r"zonder.*?dat"
