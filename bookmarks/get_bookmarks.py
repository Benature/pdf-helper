from PyPDF2 import PdfReader
import configparser
import os
import sys
from pathlib import Path
import argparse

from utils import check_conf_file, conf_path


def bookmark_dict(bookmark_list, level=1, idx=None):
    '''return dict of bookmarks
    ref: https://stackoverflow.com/questions/54303318/read-all-bookmarks-from-a-pdf-document-and-create-a-dictionary-with-pagenumber-a
    '''
    idx = [] if idx is None else idx
    result = []
    i = 1
    for item in bookmark_list:
        idx_tmp = idx + [str(i)]
        if isinstance(item, list):
            result += bookmark_dict(item, level + 1, idx_tmp)
        else:
            # idx_tmp = idx + [str(i + 1)]
            page_num = 1 + reader.get_destination_page_number(item)
            result.append((item.title, page_num, level, idx_tmp))
            i += 1
    return result


def gen_bookmark_content(bookmarks, sep="", md=False, depth=-1, min_level=1):
    max_level = min_level + depth - 1 if depth > 0 else -1
    sep = eval(f'"{sep}"')

    content = ''
    for title, page, level, idx_list in bookmarks:
        if md:
            if level >= min_level and (max_level == -1 or level <= max_level):
                idx = ".".join(idx_list[min_level - 1:])
                content += f"{'#'*(level-min_level+1)} {idx} {title}{sep}\n"
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
        # 设置默认参数
        args = argparse.Namespace(md=False, depth=-1, min=1, sep="", quiet=False)
    else:
        parser.add_argument('path', type=str)
        args = parser.parse_args()
        file_path = args.path

    file_path = Path(file_path)
    reader = PdfReader(file_path)
    bookmarks = bookmark_dict(reader.outline)
    bm_content = gen_bookmark_content(bookmarks, args.sep, args.md, args.depth,
                                      args.min)

    output_path = Path('history', f'{file_path.stem}.txt')
    with open(output_path, 'w') as f:
        f.write(bm_content)

    if not args.quiet:
        print(bm_content)
        try:
            import richxerox
            richxerox.copy(text=bm_content)
        except:
            pass
    print("Writing file to", str(output_path.resolve()))
