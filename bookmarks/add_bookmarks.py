from utils import PDFHandler, open_pdf, check_conf_file
from utils import root_path, conf_path
import configparser
import re
from pathlib import Path
from shutil import copyfile


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
                               fallback=pdf_path.parent /
                               f"{pdf_path.stem}-TOC.pdf")

    # operate pdf bookmarks
    pdf_handler = PDFHandler(pdf_path, 'newly')
    pdf_handler.add_bookmarks_by_read_txt(bookmark_file_path,
                                          page_offset=page_offset)
    pdf_handler.save(new_pdf_file_path)

    save_history(pdf_path, bookmark_file_path, new_pdf_file_path)

    if cf.getboolean('add', 'auto_open', fallback=False):
        open_pdf(new_pdf_file_path)


def save_history(pdf_path, bookmark_file_path, new_pdf_file_path):
    history_dir = root_path / 'history'
    history_dir.mkdir(parents=True, exist_ok=True)
    copyfile(bookmark_file_path, history_dir / f"{pdf_path.stem}.txt")
    copyfile(new_pdf_file_path, history_dir / f"{pdf_path.stem}-TOC.pdf")


if __name__ == '__main__':
    check_conf_file()
    main()
