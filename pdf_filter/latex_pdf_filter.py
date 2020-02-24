from PyPDF2 import PdfFileReader, PdfFileWriter
import sys

# 两种使用方法
if sys.argv:
    filename = sys.argv[0]  # 命令行敲`python3 latex_pdf_filter.py ./chp11.pdf`即可
else:
    filename = "./chp11.pdf"  # 自己改相应的文件名


def getPdfIndex(filename):
    pdf = PdfFileReader(open(filename, "rb"))
    indexs = []
    pages = []
    now = ""
    for i in range(0, pdf.getNumPages()):
        pageObj = pdf.getPage(i)
        content = pageObj.extractText()
        index = content.split("\n")[-2]
        if now != index:
            pages.append(i-1)
            now = index
        indexs.append(index)
        # return content.encode("ascii", "ignore")
    pageCount = pdf.getNumPages()
    pages.remove(-1)
    pages.append(pageCount-1)
    return indexs, pages


def splitPdf(filename, pages):
    assert filename[-4:] == '.pdf'
    output = PdfFileWriter()
    pdf_file = PdfFileReader(open(filename, "rb"))
    # pdf_pages_len = pdf_file.getNumPages()
    for i in pages:
        output.addPage(pdf_file.getPage(i))
    filename = filename.replace('\\', '/').split('/')[-1]
    outputStream = open("[Splited] "+filename, "wb")
    output.write(outputStream)


if __name__ == '__main__':
    print("split target: " + filename)
    indexs, pages = getPdfIndex(filename)
    splitPdf(filename, pages)
