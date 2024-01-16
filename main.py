import bibtexparser
import datetime

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
        self.authors = bib_entries['author'].split('and')
        self.title = bib_entries['title'] + ' '
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
            outputString += ','.join(self.authors[0:3]) + 'et al. '
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
    with open(bib_path) as bibtex_file:
        bibtex_database = bibtexparser.load(bibtex_file)
        for entries in bibtex_database.entries:
            bib_entries = BibParser(entries)
            output.append(bib_entries.get_gbt7714())
    return output

def main():
    bib_path = "./ref.bib"
    result = bibtex_to_7714(bib_path)
    print("\n".join(result))
    # save to file
    with open('./ref_bgt7714.txt', 'w') as f:
        for index, item in enumerate(result):
            f.write(f'[{index+1}] {item}\n')

if __name__ == '__main__':
    main()