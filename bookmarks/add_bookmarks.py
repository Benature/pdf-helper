from utils import path_split, MyPDFHandler, PDFHandleMode as mode
import configparser


def main():
    cf = configparser.ConfigParser()  # 从配置文件中读取配置信息

    # ATTENTION: 您可能需要修改这里的路径
    cf.read('./bookmarks/0_info.conf')

    # read config
    pdf_path = cf.get('add', 'pdf_path')
    bookmark_file_path = cf.get('add', 'bookmark_file_path')
    page_offset = cf.getint('add', 'page_offset')
    new_pdf_file_name = cf.get('add', 'bookmark_file_path',
                               fallback=path_split(pdf_path)[1])

    # operate pdf bookmarks
    pdf_handler = MyPDFHandler(pdf_path, mode=mode.NEWLY)
    pdf_handler.add_bookmarks_by_read_txt(
        bookmark_file_path, page_offset=page_offset)
    pdf_handler.save2file(new_pdf_file_name)


if __name__ == '__main__':
    main()
