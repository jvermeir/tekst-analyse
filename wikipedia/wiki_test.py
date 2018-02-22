import unittest
import wiki

class TestStringMethods(unittest.TestCase):

    def test_x_html_contains_11_text_lines(self):
        with open('sample_data.html', 'r') as myfile:
            data=myfile.readlines()
            plain_text = wiki.get_plain_text_from_wikipedia(data)
            self.assertEqual(11, len(plain_text))

    def test_multiple_html_tags_are_removed(self):
        data = ["  <p id=\"mwMw\">starters <b id=\"mwCA\">inside b</b>in <b id=\"mwCQ\">drieteenskink</b>between<a rel=\"mw:WikiLink\" href=\"./Charles_Seeberger\" title=\"Charles Seeberger\" id=\"mwEQ\" class=\"new\">Charles Seeberger</a>final<p id=\"mwAQI\"> words</p>"
            ,"<p id=\"mwMw\"> start <i id=\"mwxy\">text)</i> more text"
            ,"<p id=\"mwMw\"> start <link rel=\"mw:PageProp/Category\" href=\"./Categorie:Wikipedia:Artikel_mist_referentie_sinds_september_2016\" about=\"#mwt8\" id=\"mw8g\"/> more text"
            ,"<p id=\"mwMw\"> start <sup some sup</sup> more text"
            ,"<p id=\"mwMw\"> start (C<sub id=\"mwFA\">7</sub>H<sub id=\"mwFQ\">11</sub>) more text"]
        dirty_data = ' '.join(data)
        self.assertTrue("<b id=" in dirty_data, "<b id not found")
        self.assertTrue("<a rel" in dirty_data, "<a rel not found")
        self.assertTrue("<i id" in dirty_data, "<i id not found")
        self.assertTrue("<sup" in dirty_data, "<sup not found")
        self.assertTrue("<p id=\"mwAQI\">" in dirty_data, "<p id= (long version) not found")
        self.assertTrue("<link rel" in dirty_data, "<link rel not found")
        self.assertTrue("<sub id" in dirty_data, "<sub id not found")

        plain_text = wiki.get_plain_text_from_wikipedia(data)

        result = ' '.join(plain_text)
        self.assertTrue("<b id=" not in result, "mvCa found")
        self.assertTrue("<a rel" not in result, "<a rel found")
        self.assertTrue("<i id" not in result, "<i id found")
        self.assertTrue("<sup" not in result, "<sup found")
        self.assertTrue("<p id=\"mwAQI\">" not in result, "<p id= found")
        self.assertTrue("<link rel" not in result, "<link rel found")
        self.assertTrue("<sub id" not in result, "<sub id found")

    def test_a_re_tag_is_removed(self):
        data = ['<p id=\"mw">  <a rel=\"mw:WikiLink\" href=\"./Charles_Seeberger\" title=\"Charles Seeberger\" id=\"mwEQ\" class=\"new\">Charles Seeberger</a>']
        plain_text = wiki.get_plain_text_from_wikipedia(data)
        self.assertEqual(1, len(plain_text))
        result = ' '.join(plain_text)
        self.assertTrue("<a rel=" not in result, "<a rel= found")
        self.assertEqual("Charles Seeberger", result.strip())

    def test_p_id_tag_is_removed(self):
        data = [' <p id="mwAw">Triesenberg (Alemannisch: Trisab\xe4rg) is de, qua oppervlakte, grootste en ook hoogstgelegen (884 meter) gemeente in Alemannisch. Triesenberg is een verzameling van vele kleine kernen (in het Duits: Weiler), zoals Rotaboda, \xdcenaboda, Wangerb\xe4rg, Steinord/Lavadina, Masescha en Silum.']
        plain_text = wiki.get_plain_text_from_wikipedia(data)
        self.assertEqual(1, len(plain_text))
        result = ' '.join(plain_text)
        self.assertTrue("<p id=" not in result, "<p id= found")

    def test_span_is_removed(self):
        data = ['<p id=\"mwMw\">start<span class="mw-reflink-text">[3]</span> De betekenis uit']
        plain_text = wiki.get_plain_text_from_wikipedia(data)
        result = ' '.join(plain_text)
        self.assertEqual("start De betekenis uit", result)


    def test_script_is_removed(self):
        data = ['<p id=\"mwMw\">start<script src="//nl.wikipedia.org/w/load.php?modules=html5shiv&amp;only=scripts&amp;skin=vector&amp;sync=1"></script> De betekenis uit']
        plain_text = wiki.get_plain_text_from_wikipedia(data)
        result = ' '.join(plain_text)
        self.assertEqual("start De betekenis uit", result)


    def test_sup_is_removed(self):
        data = ['<p id=\"mwMw\">start<sup about="#mwt8" class="mw-ref" id="cite_ref-1" rel="dc:references" typeof="mw:Extension/ref" data-mw=\'{"name":"ref","body":{"id":"mw-reference-text-cite_note-1"},"attrs":{}}\'><a href="./Clepsis_clemensiana#cite_note-1" style="counter-reset: mw-Ref 1;"></a></sup> De betekenis uit']
        plain_text = wiki.get_plain_text_from_wikipedia(data)
        result = ' '.join(plain_text)
        self.assertEqual("start De betekenis uit", result)


    def test_split_text_in_sentences(self):
        self.assertEqual(['s1', 's2'], wiki.split_in_sentences('s1. s2'))
        self.assertEqual(['s3', 's4'], wiki.split_in_sentences('s3. s4.'))

    def test_grafton_case(self):
        data = wiki.read_wikipedia_page_from_url("https://nl.wikipedia.org/api/rest_v1/page/html/Grafton_(Cheshire)")
        plain_text = wiki.get_plain_text_from_wikipedia(data)
        result = ' '.join(plain_text)
        self.assertEqual('Grafton is een plaats en civil parish in het bestuurlijke gebied Cheshire West and Chester, in het Engelse graafschap Cheshire.', result)

    def test_is_maar_want_sentence_returns_sentence_with_key_words_only(self):
        want_sentence = 'this is a, want sentence'
        maar_sentence = 'this is a maar, sentence'
        should_not_appear_sentence = 'this should not appear in result'
        partial_match_should_not_appear = 'met zijn verwant, de (noordelijke)'
        self.assertTrue(wiki.is_maar_want_sentence(want_sentence), 'want sentence should be in result')
        self.assertTrue(wiki.is_maar_want_sentence(maar_sentence), 'maar sentence should be in result')
        self.assertFalse(wiki.is_maar_want_sentence(should_not_appear_sentence), 'should not appear sentence should not be in result')
        self.assertFalse(wiki.is_maar_want_sentence(partial_match_should_not_appear), 'partial match should not be in result')


if __name__ == '__main__':
    unittest.main()