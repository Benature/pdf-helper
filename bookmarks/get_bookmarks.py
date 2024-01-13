from PyPDF2 import PdfReader
import configparser
import os
import sys
from pathlib import Path
import argparse

from utils import check_conf_file, conf_path


def bookmark_dict(bookmark_list, level=1):
    '''return dict of bookmarks
    ref: https://stackoverflow.com/questions/54303318/read-all-bookmarks-from-a-pdf-document-and-create-a-dictionary-with-pagenumber-a
    '''
    result = []
    for item in bookmark_list:
        if isinstance(item, list):
            result += bookmark_dict(item, level + 1)
        else:
            page_num = 1 + reader.getDestinationPageNumber(item)
            result.append((item.title, page_num, level))
    return result


def gen_bookmark_content(bookmarks, sep="", md=False, depth=-1, min_level=1):
    max_level = min_level + depth if depth > 0 else -1
    sep = eval(f'"{sep}"')

    content = ''
    for title, page, level in bookmarks:
        if md:
            if level >= min_level and (max_level == -1 or level <= max_level):
                content += f"{'#'*(level-min_level+1)} {title}{sep}\n"
        else:
            content += f"{title} @{page}{sep}\n"

    return content


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', action="store_true")
    parser.add_argument('--depth', '-d', type=int, default=-1)
    parser.add_argument('--min', '-m', type=int, default=1)
    parser.add_argument('--sep', '-s', type=str, default="")
    parser.add_argument('--quiet', '-q', action="store_true")
    if len(sys.argv) == 1:
        check_conf_file()
        cf = configparser.ConfigParser()
        cf.read(conf_path)
        file_path = cf.get('get', 'pdf_path')
    else:
        parser.add_argument('path', type=str)
        args = parser.parse_args()
        file_path = args.path

    file_path = Path(file_path)
    reader = PdfReader(file_path)
    bookmarks = bookmark_dict(reader.getOutlines())

    bm_content = gen_bookmark_content(bookmarks, args.sep, args.md, args.depth,
                                      args.min)

    with open(Path('history', f'{file_path.stem}.txt'), 'w') as f:
        f.write(bm_content)

    if not args.quiet:
        print(bm_content)
        import richxerox
        richxerox.copy(text=bm_content)
