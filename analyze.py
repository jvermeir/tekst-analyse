import unittest
import os
import glob


class TextAnalysis(object):
    def __init__(self, pathToTextFiles):
        self.pathToTextFiles = pathToTextFiles

    def loadFiles(self):
        # lees alle files in de directory pathToTextFiles en stop ze in
        # een dict. Gebruik de naam van de file als key en de inhoud als value
        files = glob.glob(self.pathToTextFiles)
        fileContents = dict()
        for file in files:
            # lees file in een string, voeg de inhoud van de string toe aan een dict met als sleutel de naam van de file
            # tekst in een dict stoppen: fileContents["myfile"] = "yo"
            # https://docs.python.org/2/tutorial/inputoutput.html#methods-of-file-objects
            pass
        return fileContents

    def splitTextIntoSentences(testText):
        # https://www.tutorialspoint.com/python/string_split.htm
        return []

    def filter(self, sentences):
        # https://stackoverflow.com/questions/3013449/list-filtering-list-comprehension-vs-lambda-filter
        return []


class TextAnalysisTest(unittest.TestCase):
    def testFileIsLoadedFromDisk(self):
        textAnalysis = TextAnalysis("testFiles/loadFromDiskTest/")
        files = textAnalysis.loadFiles()
        self.assertEqual(1, len(files))
        testFile = files["myfile"]
        self.assertEqual("yo", testFile)

    def testTextIsSplitIntoSentences(self):
        testText = "Sentence 1. Sentence, 2."
        textAnalysis = TextAnalysis("dummy")
        sentences = textAnalysis.splitTextIntoSentences(testText)
        self.assertTrue(2, len(sentences))
        self.assertEqual(sentences[0], "Sentence 1.")
        self.assertEqual(sentences[1], "Sentence, 2.")

    def testFilterSentences(self):
        testText = "Sentence 1. Sentence, 2."
        textAnalysis = TextAnalysis("dummy")
        sentences = textAnalysis.splitTextIntoSentences(testText)
        filteredSentences = textAnalysis.filter(sentences)
        self.assertTrue(1, len(filteredSentences))
        self.assertEqual(filteredSentences[0], "Sentence 1.")


if __name__ == '__main__':
    unittest.main()
