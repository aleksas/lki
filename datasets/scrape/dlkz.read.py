from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree

def get_ets(filename):
    with ZipFile(filename, 'r') as zf:
        for name in zf.namelist():
            with BytesIO(zf.read(name)) as bf:
                yield ElementTree.parse(bf)

for element_tree in get_ets('datasets/scrape/dlkz.zip'):
    print (element_tree.getroot())
