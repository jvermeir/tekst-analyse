#
# Representation of a conjunction

import re
import json

class Conjunction():

    conjunction_words = {"want", "omdat", "daarom", "daardoor", "doordat", "ookal", "hoewel", "maar" }


    def __init__(self, sentence, previous_sentence):
        self.word = ""
        self.left = ""
        self.right = ""
        self.url = ""

        sentence = sentence.lower()
        previous_sentence = previous_sentence.lower()
        stripped_words = map(lambda word: re.sub('[ \n\t,.!?><&()]', '', word), sentence.split())
        conjunctions = set(stripped_words).intersection(self.conjunction_words)
        if len(conjunctions) > 0:
            self.word = next(iter(conjunctions))
            if stripped_words[0] == self.word:
                self.left = previous_sentence
                self.right = ' '.join(stripped_words[1:])
            else:
                parts = ' '.join(stripped_words).split(self.word)
                if len(parts) == 2:
                    self.left = parts[0].strip(' ')
                    self.right = parts[1].strip(' ')
                else:
                    self.right = parts[0].strip(' ')

    @classmethod
    def toJson(cls, conjunctions):
        text = "["
        for c in conjunctions:
            if len(c.word) > 0:
                text = text + json.dumps(c.__dict__) + ","
        return text[:len(text) - 1] + "]"


    @classmethod
    def toCSV(cls, conjunctions):
        text = ""
        for c in conjunctions:
            if len(c.word) > 0:
                text = text + '"' + c.left + '","' + c.word + '","' + c.right + '"\n'
        return text