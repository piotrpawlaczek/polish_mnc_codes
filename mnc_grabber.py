import warnings
import cStringIO
import zipfile
import urllib2
import collections

from lxml import etree

# DONOR CODES FROM POLISH OFFICE OF ELECTRONIC COMMUNICATIONS
UKE_URL = 'http://www.uke.gov.pl/tablice/xml/T11-MNC.xml.zip'
FILENAME = 'T11-MNC.xml'


class MNCCodes(collections.MutableMapping):

    _store = {}

    def __init__(self, source=UKE_URL, filename=FILENAME):
        remotefile = urllib2.urlopen(source)
        content_type = remotefile.info()['Content-Type']
        _memory = cStringIO.StringIO()

        if not content_type.endswith('zip'):
            raise TypeError('Wrong source type')

        _memory.write(remotefile.read())
        z = zipfile.ZipFile(_memory)

        for name in z.namelist():
            if name != filename:
                warnings.warn('Filename is changed, keep an eye on that!')
            try:
                with z.open(name) as f:
                    self.parse(etree.fromstring(f.read()))
            except:
                # Avoid mem leak
                _memory.close()
                raise
            finally:
                break

        _memory.close()

    def parse(self, tree):

        for tbl in tree:
            for mnc in tbl:
                operator, code, blocked = None, None, None
                for child in mnc:
                    if child.tag == 'operator':
                        operator = child.text
                    if child.tag == 'kod':
                        code = child.text
                    if child.tag == 'blokada':
                        if child.text == 'true':
                            blocked = True
                if operator and code:
                    self._store.update({code: operator})

    def __keytransform__(self, key):
        return key

    def __getitem__(self, key):
        return self._store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return repr(self._store)
