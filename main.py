import csv
import datetime
import logging
import os
import re
import sys

logger = logging.getLogger(__name__)

import bibtexparser

NOW = datetime.datetime.now().strftime('%Y-%m-%d')
with open("data/Chinese_surname.csv", "r") as f:
    reader = csv.reader(f)
    CHINESE_SURNAME = [str(row[0]).upper() for row in reader]
# logger.info(f"Chinese surname: {CHINESE_SURNAME}")

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
        bib_entries = {k.lower(): v for k, v in bib_entries.items()}
        self.entries = bib_entries
        try:
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
                self.ENTRYTYPE = '[' + BOOK_TYPE[bib_entries['entrytype']] + ']. '
                self.journal = bib_entries['journal'] + ', ' if 'journal' in bib_entries else ''
                self.volume = bib_entries['volume'] if 'volume' in bib_entries else ''
                self.number = '(' + bib_entries['number'] + '):' if 'number' in bib_entries else ''
                if 'url' in bib_entries:
                    self.url = bib_entries['url'] + '. '
                else:
                    self.url = ''

            self.year = bib_entries['year'] + ','
            self.authors = [author.strip() for author in re.split(r'\band\b', bib_entries['author'])]  # and 的全词匹配
            self.normal_name()
            # logger.info(self.authors)
            self.title = bib_entries['title'] + ' '
            self.title = self.title[0].upper() + self.title[1:]
            self.ID = bib_entries['id']
            self.doi = bib_entries['doi'] + '. ' if 'doi' in bib_entries else ''
            self.pages = bib_entries['pages'] if 'pages' in bib_entries else ''
        except KeyError as e:
            raise KeyError(f"KeyError: {e}。"
                           f" 请检查 bib 文件是否包含必要的字段。"
                           f" {bib_entries}")

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

    def normal_name(self):
        global CHINESE_SURNAME
        normal_authors = []
        for author_name in self.authors:
            if ',' in author_name:  # 有逗号的话前面是姓
                surname = author_name.split(',')[0].upper().strip()  # 姓氏要求全部大写
                g_name = author_name.split(',')[1].lower().strip()  # 名暂时全部小写，后面处理
            else:  # 没有逗号的话后面是姓
                surname = ' '.join(author_name.strip().split(' ')[1:]).upper().replace('.',
                                                                                       '')  # 姓氏要求全部大写，有可能存在中间名，也提成姓，去掉姓的 '.'
                g_name = author_name.strip().split(' ')[0].lower()  # 名暂时全部小写，后面处理
                # logger.info(f"Warning: surname '{surname}' , gname:{g_name}。")
            if surname.upper() in CHINESE_SURNAME:  # 如果是中文姓氏，名完整保留，首字母大写
                # logger.info(f"Chinese surname: {surname}")
                g_name = g_name.capitalize()
            else:  # 非中文姓氏
                g_name = [name.replace('.', '').capitalize() for name in g_name.split(' ')]  # 去掉 ".", 首字母大写
                g_name = " ".join([name[0] for name in g_name])  # 仅保留首字母
            full_name = surname + ' ' + g_name
            normal_authors.append(full_name)
        self.authors = normal_authors


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
            bibtex_database = bibtexparser.parse_file(bib_path)
            for entries in bibtex_database.entries:
                # logger.info(entries)
                bib_entries = BibParser(entries)
                output.append(bib_entries.get_gbt7714())
            logger.info(f"使用'{encoding}'编码转换成功")
            return output  # 成功读取后返回结果
        except UnicodeDecodeError as e:
            logger.info(f"编码方式 '{encoding}' 无法解码文件，尝试下一个编码方式")
            continue  # 如果解码失败，尝试下一个编码方式

    # 如果所有编码方式都失败，抛出异常
    raise Exception(f"无法使用任何编码方式解码文件 '{bib_path}'")


def main():
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        bib_path = sys.argv[1]
    else:
        bib_path = "data/ref.bib"
    result = bibtex_to_7714(bib_path)
    folder = os.path.dirname(bib_path)
    file_name = os.path.basename(bib_path).split('.')[0]
    # save to file
    with open(f'{folder}/{file_name}_bgt7714.txt', 'w') as f:
        for index, item in enumerate(result):
            f.write(f'[{index + 1}] {item}\n')


if __name__ == '__main__':
    main()
