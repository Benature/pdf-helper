from utils import PDFHandler, PDFHandleMode as mode
from utils import open_pdf
from utils import root_path, check_conf_file, conf_path
import configparser
import os
import re
from pathlib import Path


def main():
    # read config
    cf = configparser.ConfigParser()  # config
    cf.read(conf_path)
    pdf_path = Path(cf.get('add', 'pdf_path'))
    bookmark_file_path = cf.get('add', 'bookmark_file_path')
    page_offset = cf.getint('add', 'page_offset')

    with open(bookmark_file_path, "r") as f:
        bm_meta = re.findall(r"offset\s*=\s*\d+\n", f.read())
        if bm_meta:
            bm_cf = configparser.ConfigParser()  # bookmark config
            bm_cf.read_string(f"[meta]\n{bm_meta[0]}")
            print(f"Read from bookmark meta: {bm_meta[0]}")
            page_offset = bm_cf.getint('meta', 'offset')

    new_pdf_file_path = cf.get('add',
                               'new_pdf_file_name',
                               fallback=root_path / 'output' / pdf_path.name)

    # operate pdf bookmarks
    pdf_handler = PDFHandler(pdf_path, mode=mode.NEWLY)
    pdf_handler.add_bookmarks_by_read_txt(bookmark_file_path,
                                          page_offset=page_offset)
    pdf_handler.save(new_pdf_file_path)

    if cf.getboolean('add', 'auto_open', fallback=False):
        open_pdf(new_pdf_file_path)


if __name__ == '__main__':
    check_conf_file()
    main()
