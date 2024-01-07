from PyPDF2 import PdfFileReader
import configparser
import os
import sys
from pathlib import Path

from utils import check_conf_file, conf_path


def bookmark_dict(bookmark_list):
    '''return dict of bookmarks
    ref: https://stackoverflow.com/questions/54303318/read-all-bookmarks-from-a-pdf-document-and-create-a-dictionary-with-pagenumber-a
    '''
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            result.update(bookmark_dict(item))
        else:
            result[reader.getDestinationPageNumber(item)] = item.title
    return result


def write_bookmark(bookmarks):
    content = ''
    for page, title in bookmarks.items():
        content += f"{title} @{page}\n"
    return content


if __name__ == '__main__':
    if len(sys.argv) == 1:
        check_conf_file()
        cf = configparser.ConfigParser()
        cf.read(conf_path)
        file_path = cf.get('get', 'pdf_path')
    else:
        file_path = sys.argv[1]

    file_path = Path(file_path)
    reader = PdfFileReader(file_path)
    bookmarks = bookmark_dict(reader.getOutlines())

    with open(Path('history', f'{file_path.stem}.txt'), 'w') as f:
        f.write(write_bookmark(bookmarks))
