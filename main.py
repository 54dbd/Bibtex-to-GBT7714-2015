import sys
import os

import bibtexparser
import datetime
import string
import re

NOW = datetime.datetime.now().strftime('%Y-%m-%d')

BOOK_TYPE = {'article': 'J',
             'book': 'M',
             'booklet': 'M',
             'conference': 'C',
             'inbook': 'M',
             'incollection': 'M',
             'inproceedings': 'C',
             'manual': 'R',
             'misc': 'Z',
             'mastersthesis': 'D ',
             'phdthesis': 'D',
             'proceedings': 'C',
             'techreport': 'R',
             'unpublished': 'C',
             'collection': 'G',
             'newspaper': 'N',
             'standard': 'S',
             'patent': 'P',
             'database': 'DB',
             'software': 'CP',
             'online': 'EB',
             'archive': 'A',
             'map': 'CM',
             'dataset': 'DS'
             }


class BibParser:
    """
    Parse a bib entry
    """

    def __init__(self, bib_entries):
        self.entries = bib_entries
        if 'primaryclass' in bib_entries:
            # For arxiv exclusively
            self.primaryclass = bib_entries['primaryclass']
            self.archivePrefix = bib_entries['archiveprefix']
            self.journal = 'arXiv:' + self.primaryclass + ', '
            self.number = '1'
            self.volume = bib_entries['eprint']
            self.eprint = bib_entries['eprint']
            self.url = 'https://arxiv.org/abs/' + self.eprint + '. '
            self.ENTRYTYPE = '[EB/OL]. '

        else:
            self.ENTRYTYPE = '[' + BOOK_TYPE[bib_entries['ENTRYTYPE']] + ']. '
            self.journal = bib_entries['journal'] + ', ' if 'journal' in bib_entries else ''
            self.volume = bib_entries['volume'] if 'volume' in bib_entries else ''
            self.number = '(' + bib_entries['number'] + '):' if 'number' in bib_entries else ''
            if 'url' in bib_entries:
                self.url = bib_entries['url'] + '. '
            else:
                self.url = ''

        self.year = bib_entries['year'] + ','
        self.authors = self.authors = [author.strip() for author in re.split(r'\band\b', bib_entries['author'])]  # and 的全词匹配
        self.authors = [author.strip().upper() for author in self.authors]
        print(self.authors)
        self.title = bib_entries['title'] + ' '
        self.title = self.title[0].upper() + self.title[1:]
        self.ID = bib_entries['ID']
        self.doi = bib_entries['doi'] + '. ' if 'doi' in bib_entries else ''
        self.pages = bib_entries['pages'] if 'pages' in bib_entries else ''

    def get_gbt7714(self) -> str:
        """
        return a reference in gbt7714 format
        :return: reference in gbt7714 format
        """
        outputString = ''
        if len(self.authors) > 3:
            outputString += ','.join(self.authors[0:3]) + ',et al. '
        else:
            outputString += self.authors[0] + '. '
        outputString += self.title
        outputString += self.ENTRYTYPE
        outputString += self.journal
        outputString += self.year
        outputString += self.volume + self.number + self.pages + '[' + NOW + ']. '
        outputString += self.url
        outputString += self.doi

        return outputString


def bibtex_to_7714(bib_path) -> list[str]:
    """
    Convert a bibtex file to gbt7714 format
    :param bib_path: the path of the bibtex file
    :return: list of references in gbt7714 format
    """
    output = []
    encodings = ['utf-8', 'gbk', 'gb2312']
    if not os.path.exists(bib_path):
        raise FileNotFoundError(f"文件 '{bib_path}' 不存在。")
    for encoding in encodings:
        try:
            with open(bib_path, 'r', encoding=encoding) as bibtex_file:
                bibtex_database = bibtexparser.load(bibtex_file)
                for entries in bibtex_database.entries:
                    bib_entries = BibParser(entries)
                    output.append(bib_entries.get_gbt7714())
                print(f"使用'{encoding}'编码转换成功")
                return output  # 成功读取后返回结果
        except UnicodeDecodeError as e:
            print(f"编码方式 '{encoding}' 无法解码文件，尝试下一个编码方式")
            continue  # 如果解码失败，尝试下一个编码方式

    # 如果所有编码方式都失败，抛出异常
    raise Exception(f"无法使用任何编码方式解码文件 '{bib_path}'")


def main():
    if len(sys.argv) > 1:
        bib_path = sys.argv[1]
    else:
        bib_path = "./ref.bib"
    result = bibtex_to_7714(bib_path)
    # save to file
    with open(f'{os.path.splitext(os.path.basename(bib_path))[0]}_bgt7714.txt', 'w') as f:
        for index, item in enumerate(result):
            f.write(f'[{index + 1}] {item}\n')



if __name__ == '__main__':
    main()
