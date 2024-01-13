# coding:utf-8
from PyPDF2 import PdfReader, PdfWriter
import os
import re
import subprocess
from platform import system
from pathlib import Path

root_path = Path(__file__).resolve().parent
conf_path = root_path / 'info.conf'


def check_conf_file():
    """检查配置文件是否存在"""
    if os.path.exists(conf_path):
        return True
    from shutil import copyfile
    copyfile(root_path / 'info_sample.conf', conf_path)
    log("ERROR", "似乎还未设置好配置文件")


def log(typ, info, more='', index=None):
    if typ == 'WARN':
        typ = f"\033[1;33m<{typ}>\033[0m"
    elif typ == 'ERROR':
        typ = f"\033[1;31m<{typ}>\033[0m"
    else:
        typ = f"<{typ}>"

    line_info = f"line\033[1;36m{index+1:<4}\033[0m" if index is not None else ""
    print(f"{typ} {info} | {line_info} \033[1;44m{more} \033[0m")


def open_pdf(file_path):
    SYSTEM = system()
    if SYSTEM == 'Darwin':
        cmd = f'open "{file_path}"'
        print(cmd)
        subprocess.call(cmd, shell=True)
    else:
        log('WARN', '目前仅支持在 macOS 自动打开 pdf')


class PDFHandler(object):
    '''
    封装的PDF文件处理类
    '''

    def __init__(self, pdf_file_path, mode='copy'):
        '''
        用一个PDF文件初始化
        :param pdf_file_path: PDF文件路径
        :param mode: 处理PDF文件的模式，默认为PDFHandleMode.COPY模式
        '''
        # 只读的PDF对象
        self.__pdf = PdfReader(pdf_file_path)

        # 获取PDF文件名（不带路径）
        self.file_name = os.path.basename(pdf_file_path)
        #
        self.metadata = self.__pdf.getXmpMetadata()
        #
        self.doc_info = self.__pdf.getDocumentInfo()
        #
        self.pages_num = self.__pdf.getNumPages()

        # 可写的PDF对象，根据不同的模式进行初始化
        self.__writeable_pdf = PdfWriter()
        if mode == 'copy':  # 保留源PDF文件的所有内容和信息，在此基础上修改
            self.__writeable_pdf.cloneDocumentFromReader(self.__pdf)
        elif mode == 'newly':  # 仅保留源PDF文件的页面内容，在此基础上修改
            for idx in range(self.pages_num):
                page = self.__pdf.getPage(idx)
                self.__writeable_pdf.insertPage(page, idx)

    def save(self, new_file_path):
        '''
        将修改后的PDF保存成文件
        :param new_file_name: 新文件名
        :return: None
        '''
        if not isinstance(new_file_path, Path):
            new_file_path = Path(new_file_path)
        # make sure the directory exists
        new_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(new_file_path, 'wb') as f:
            self.__writeable_pdf.write(f)
        print(f'Save to new file: {str(new_file_path)}')

    def add_one_bookmark(self,
                         title,
                         page,
                         parent=None,
                         color=None,
                         fit='/Fit'):
        '''
        往PDF文件中添加单条书签，并且保存为一个新的PDF文件
        :param str title: 书签标题
        :param int page: 书签跳转到的页码，表示的是PDF中的绝对页码，值为1表示第一页
        :paran parent: A reference to a parent bookmark to create nested bookmarks.
        :param tuple color: Color of the bookmark as a red, green, blue tuple from 0.0 to 1.0
        :param list bookmarks: 是一个'(书签标题，页码)'二元组列表，举例：[(u'tag1',1),(u'tag2',5)]，页码为1代表第一页
        :param str fit: 跳转到书签页后的缩放方式
        :return: bookmark
        '''
        bm = self.__writeable_pdf.addBookmark(title,
                                              page - 1,
                                              parent=parent,
                                              color=color,
                                              fit=fit)
        return bm

    def add_bookmarks(self, bookmarks, max_parent):
        '''
        批量添加书签
        :param bookmarks: 书签元组列表，其中的页码表示的是PDF中的绝对页码，值为1表示第一页
        :return: None
        '''
        parents = [None] * (max_parent + 2)
        for title, page, index in bookmarks:
            bm = self.add_one_bookmark(title, page, parent=parents[index])
            parents[index + 1] = bm
        print('add_bookmarks success! add {0} pieces of bookmarks to PDF file'.
              format(len(bookmarks)))

    def read_bookmarks_from_txt(self, txt_file_path, page_offset=0):
        '''
        从文本文件中读取书签列表
        文本文件有若干行，每行一个书签，内容格式为：
        书签标题 页码
        注：中间用空格隔开，页码为1表示第1页
        :param txt_file_path: 书签信息文本文件路径
        :param page_offset: 页码便宜量，为0或正数，即由于封面、目录等页面的存在，在PDF中实际的绝对页码比在目录中写的页码多出的差值
        :return: 书签列表
        '''
        bookmarks = []
        max_parent = 0
        with open(txt_file_path, 'r') as fin:
            for i, line in enumerate(fin):
                line = line.rstrip()
                if not line:
                    continue
                if '@' not in line:
                    log('WARN', "No `@` in line", line, i)
                    continue
                # 以'@'作为标题、页码分隔符
                try:
                    title = line.split('@')[0].rstrip().replace('\t', '    ')
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    log('ERROR', msg, line, i)
                    continue
                # title和page都不为空才添加书签，否则不添加
                if title and page:
                    index = int(len(re.findall(r"^[ ]*", title)[0]) / 4)
                    if index > max_parent:
                        max_parent = index
                    try:
                        page = int(page) + page_offset
                        if title.strip().count(' ') > 1:
                            if re.search(r"[a-zA-z]", line):
                                if title.strip().count(' ') > 2:
                                    log('WARN', 'seems too many blanks', line,
                                        i)
                            else:
                                log('WARN', 'seems too many blanks', line, i)
                        bookmarks.append((title.strip(), page, index))
                    except ValueError as msg:
                        log('ERROR', msg, line, i)
                else:
                    log('WARN', 'skip line', line, i)
        return bookmarks, max_parent

    def add_bookmarks_by_read_txt(self, txt_file_path, page_offset=0):
        '''
        通过读取书签列表信息文本文件，将书签批量添加到PDF文件中
        :param txt_file_path: 书签列表信息文本文件
        :param page_offset: 页码偏移量，为0或正数，即由于封面、目录等页面的存在，在PDF中实际的绝对页码比在目录中写的页码多出的差值
        :return: None
        '''
        bookmarks, max_parent = self.read_bookmarks_from_txt(
            txt_file_path, page_offset)
        self.add_bookmarks(bookmarks, max_parent)
        # print('add_bookmarks_by_read_txt success!')
