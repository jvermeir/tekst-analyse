import sys
import text_analyzer as text
import codecs
import conjunction

def main():
    commandline_arguments = getopts(sys.argv)
    if '-f' not in commandline_arguments:
        sys.exit("Usage: python analyze_a_text.py -f <conjunction file name>")
    file_name = commandline_arguments.get('-f')
    conjunctions = text.collect_conjunctions_from_file(file_name)
    with codecs.open("conjunctions/" + file_name + "_output.json", "w", encoding='utf-8') as output_file:
        output_file.write(conjunction.Conjunction.toJson(conjunctions))


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

if __name__ == "__main__":
    main()

