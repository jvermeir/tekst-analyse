import requests
import re
import codecs
import time
import json
import page_data
import result

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
headers = {
    'User-Agent': 'jvermeir@hotmail.com',
}
roll_over_file_size = 10*1024*1024


replace_patterns = [start_of_text_line_pattern, bold_pattern, link_pattern, i_pattern, sub_pattern]
remove_patterns = [span_pattern, script_pattern, slash_p_pattern, sup_pattern, end_of_span_pattern, p_pattern, link_rel_pattern, br_pattern]

history = set()

def check_if_page_is_new(url):
    if url in history:
        return False
    return True


def read_wikipedia_page_from_url(url):
    response = requests.get(url)
    history.add (response.url)
    return response.text.splitlines()


def read_wikipedia_page():
    response = requests.get('https://nl.wikipedia.org/api/rest_v1/page/random/html', headers, allow_redirects=True)
    article_url = response.url.replace('https://nl.wikipedia.org/api/rest_v1/page/html/','')
    while check_if_page_is_new(article_url) == False:
        response = requests.get('https://nl.wikipedia.org/api/rest_v1/page/random/html', headers, allow_redirects=True)
        article_url = response.url.replace('https://nl.wikipedia.org/api/rest_v1/page/html/','')
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
    if results.data_size > roll_over_file_size:
        json.dump(results.pages, results.data_file)
        results = result.Result.reset()
    return results


def main():
    read_history("data/history.txt")

    results = result.Result.reset()
    for i in range(0, 20):
        wiki_page = read_wikipedia_page()
        print(wiki_page.page_name)
        lines = get_plain_text_from_wikipedia(wiki_page.lines)
        sentences = get_sentences(lines)
        results = store_results(wiki_page, sentences, results)

        time.sleep(0.5)

    json.dump(results.pages, results.data_file)

    with codecs.open("data/history.txt", "w", encoding='utf-8') as history_file:
        history_file.writelines( "%s\n" % line for line in history )


if __name__ == "__main__":
    main()

