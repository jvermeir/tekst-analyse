import requests
import re
import codecs
import time
import json
import page_data
import result
import sys

start_of_text_line_pattern = r"<p id=\"mw\w\w\">(.*?)"
bold_pattern = r"<b id=\"mw.*?\">(.*?)</b>"
link_pattern = r"<a rel=.*?>(.*?)</a>"
sup_pattern = r"<sup .*?</sup>"
i_pattern = r"<i id=\"mw.*?\">(.*?)</i>"
span_pattern = r"<span.*?</span>"
script_pattern = r"<script .*?</script>"
slash_p_pattern = r"</[p|b]>"
end_of_span_pattern = r"</a></span>"
p_pattern = r"<p id=\"mw.*?\">"
link_rel_pattern = r"<link rel=.*?/>"
br_pattern = r"<br id=\"mw.*?\"/>"
sub_pattern = r"<sub id=.*?>(.*?)</sub>"
figure_pattern = r"<figure class=.*?</figure>"
headers = {
    'User-Agent': 'jvermeir@hotmail.com',
}
roll_over_file_size = 10*1024


replace_patterns = [start_of_text_line_pattern, bold_pattern, link_pattern, i_pattern, sub_pattern]
remove_patterns = [span_pattern, script_pattern, slash_p_pattern, sup_pattern, end_of_span_pattern, p_pattern, link_rel_pattern, br_pattern, figure_pattern]

history = set()

def check_if_page_is_new(url):
    if url in history:
        print ("*** skip " + url)
        return False
    return True


def read_wikipedia_page_from_url(url):
    response = requests.get(url)
    history.add (response.url)
    return response.text.splitlines()


def read_wikipedia_page():
    new_page = False
    while not new_page:
        response = requests.get('https://nl.wikipedia.org/api/rest_v1/page/random/html', headers, allow_redirects=True)
        article_url = response.url.replace('https://nl.wikipedia.org/api/rest_v1/page/html/','')
        new_page = check_if_page_is_new(article_url)
    history.add (article_url)
    return page_data.PageData(article_url, response.text.splitlines())


def apply_replace_pattern(pattern, line):
    m = re.search(pattern, line)
    while m:
        match = m.group(1)
        line = re.sub(pattern,match,line,1)
        m = re.search(pattern, line)
    return line


def apply_all_patterns(replace_patterns, remove_patterns, line):
    for p in replace_patterns:
        line = apply_replace_pattern(p, line)
    for p in remove_patterns:
        line = re.sub(p,'', line)
    return line


def get_plain_text_from_wikipedia(data):
    content_lines = filter(lambda x: "<p id=\"mw" in x, data)
    plain_text = map(lambda x: apply_all_patterns(replace_patterns, remove_patterns, x), content_lines)
    return plain_text


def read_history(file_name):
    try:
        with open(file_name, "r") as history_file:
            for line in history_file.readlines():
                history.add(line.rstrip())
    except:
        pass


def split_in_sentences(text):
    sentences = text.split('.')
    stripped_sentences = map(lambda x: x.strip(), sentences)
    return filter(lambda sentence: len(sentence) > 0, stripped_sentences)

def cleanup_sentence(line):
    return line.strip("\n\t,.!?><&\"'=+-_\)\(*&^%$#@~/")


def get_sentences(plain_text_lines):
    lines = []
    for line in plain_text_lines:
        sentences = split_in_sentences(line)
        for sentence in sentences:
            clean_sentence = cleanup_sentence(sentence)
            lines.append(clean_sentence)
    return lines


def add_page_data_to_dict(wiki_page, sentences, results):
    results.addPage(wiki_page.page_name, sentences)


def store_results(wiki_page, sentences, results):
    results.addPage(wiki_page, sentences)
    print (results.data_size)
    if results.data_size > roll_over_file_size:
        print ("***  storing results in ")
        print (results.data_file_name)
        json.dump(results.pages, results.data_file)
        results = result.Result.reset()
    return results


def main():
    commandline_arguments = getopts(sys.argv)
    if '-c' not in commandline_arguments:
        sys.exit("Usage: python wiki_text_collector.py -c <number of pages to read from Wikipedia>")
    number_of_pages_to_read = int(commandline_arguments.get('-c'))
    print ("*** Reading " + str(number_of_pages_to_read) + " pages")

    read_history("data/history.txt")
    results = result.Result.reset()
    for i in range(0, number_of_pages_to_read):
        try:
            wiki_page = read_wikipedia_page()
            print(wiki_page.page_name)
            lines = get_plain_text_from_wikipedia(wiki_page.lines)
            sentences = get_sentences(lines)
            results = store_results(wiki_page, sentences, results)
            time.sleep(0.5)

        except Exception as e:
            print(e)
            print ("*** exception, writing results ")
            print (results.data_file_name)
            json.dump(results.pages, results.data_file)

    with codecs.open("data/history.txt", "w", encoding='utf-8') as history_file:
        history_file.writelines( "%s\n" % line for line in history )


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

if __name__ == "__main__":
    main()

