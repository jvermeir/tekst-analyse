#
# List all sentences that contain a conjunction

import json
import os
import codecs
import conjunction


def collect_conjunctions_from_file(file_name):
    print ("file: " + file_name)
    result = []
    try:
        json_data = json.load(open("data/" + file_name, "r"))
        for key in json_data.keys():
            lines = json_data.get(key)
            previous_line = ""
            for line in lines:
                line = line.replace("ook al", "ookal")
                c = conjunction.Conjunction(line, previous_line)
                previous_line = line
                if len(c.word) > 0:
                    c.url = key
                    result.append(c)
    except Exception as e:
        print(e)
        print ("*** skip " + file_name)

    return result


def main():
    conjunctions = []
    counter = 0
    try:
        os.mkdir("conjunctions")
    except:
        pass

    for f in os.listdir("data"):
        result = collect_conjunctions_from_file(f)
        conjunctions = conjunctions + result
        if len(conjunctions) > 1000:
            if len(conjunctions) > 0:
                with codecs.open("conjunctions/conjunctions" + str(counter) + ".json", "w",
                                 encoding='utf-8') as output_file:
                    output_file.write(conjunction.Conjunction.toJson(conjunctions))
            counter = counter + 1
            conjunctions = []


if __name__ == "__main__":
    main()
