import requests
import re
import time

start_op_text_line_pattern = r"<p id=\"mw\w\w\">(.*?)"
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
sub_pattern = r"<sub id=.*?>(.*?)</sub>"
headers = {
    'User-Agent': 'jvermeir@hotmail.com',
}

replace_patterns = [start_op_text_line_pattern, bold_pattern, link_pattern, i_pattern, sub_pattern]
remove_patterns = [span_pattern, script_pattern, slash_p_pattern, sup_pattern, end_of_span_pattern, p_pattern, link_rel_pattern]

def read_wikipedia_page():
    r = requests.get('https://nl.wikipedia.org/api/rest_v1/page/random/html', headers, allow_redirects=True)
    return r.text.splitlines()

def apply_replace_pattern(pattern, line):
    m = re.search(pattern, line)
    while m:
        match = m.group(1)
        line = re.sub(pattern,match,line)
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


def main():
    for i in range(0, 10):
        data = read_wikipedia_page()
        plain_text = get_plain_text_from_wikipedia(data)
        print(plain_text)
        time.sleep(1)


if __name__ == "__main__":
    main()

