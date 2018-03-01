#
# List all sentences that contain a conjunction
# List of conjunction words taken from: https://nl.wikipedia.org/wiki/Voegwoord

import re
import json
import os
import codecs

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


def is_conjunction_sentence(sentence):
    try:
        words = sentence.split()
        stripped_words = map(lambda word: re.sub('[ \n\t,.!?><&()]', '',word), words)
        conjunction_found = any(word in stripped_words for word in conjunctions_words)
        if not conjunction_found:
            normalized_sentence = ' '.join(stripped_words)
            return (re.search(normalized_sentence, als_dan_pattern) is not None) or (re.search(normalized_sentence, zonder_dat_pattern) is not None)
        return True
    except Exception as e:
        print (e)
    return False

def collect_conjunctions_from_file(file_name):
    print ("file: " + file_name)
    result = {}
    try:
        json_data = json.load(open("data/" + file_name, "r"))
        for key in json_data.keys():
            lines = json_data.get(key)
            result[key] = filter(lambda line: is_conjunction_sentence(line), lines)
    except Exception as e:
        print(e)
        print ("*** skip " + file_name)

    return result


def main():
    conjunctions = {}
    counter = 0;
    try:
        os.mkdir("conjunctions")
    except:
        pass

    for f in os.listdir("data"):
        result = collect_conjunctions_from_file(f)
        conjunctions.update(result)
        if len(conjunctions) > 1000:
            json.dump(conjunctions, codecs.open("conjunctions/conjunctions" + str(counter)+ ".json", "w", encoding='utf-8'))
            counter = counter + 1
            conjunctions = {}

if __name__ == "__main__":
    main()

