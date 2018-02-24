#
# Store results while loading pages and retrieving text

import codecs
import sys
import time

class Result:
    file_name_prefix="data/"

    def __init__(self, data_file_name, data_file, data_size, pages):
        self.data_file_name = data_file_name
        self.data_file = data_file
        self.data_size = data_size
        self.pages = pages

    @classmethod
    def reset(cls):
        data_file_name = Result.get_new_data_file_name()
        data_file = codecs.open(data_file_name, "w", encoding='utf-8')
        return cls(data_file, data_file, 0, {})

    @classmethod
    def get_new_data_file_name(cls):
        return Result.file_name_prefix + time.strftime("%Y%m%d%H%M%S") +".json"

    def addPage(self, page, sentences):
        self.pages[page.page_name] = sentences
        self.data_size = self.data_size + sys.getsizeof(sentences)
