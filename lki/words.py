import re
import os
import urllib.request
from tqdm import tqdm
from zipfile import ZipFile

import chars
from parsers import modern_lt_vocabulary_words, historic_location_names, last_names, lt_lv_dict

datasets = [
	('207-dlkz.zip', 'utf-8', modern_lt_vocabulary_words),
	('1001-location-names.zip', 'utf-8', historic_location_names),
	('1101-last-names.zip', 'utf-8', last_names),
	('105-lt-lv-dict.zip', 'utf-8', lt_lv_dict)
]

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download(filename, base_url='https://github.com/aleksas/lki/releases/download', tag='0.0.1', directory='.', force=False):		
	path = os.path.join(directory, filename)

	os.makedirs(directory, exist_ok=True)

	if force or not os.path.exists(path):
		url = '/'.join([base_url, tag, filename])
		with DownloadProgressBar(unit='B', unit_scale=True,miniters=1, desc=filename) as t:
			urllib.request.urlretrieve(url, filename=path, reporthook=t.update_to)

	return path

def get_words(directory='./datasets'):
	for archive_filename, encoding, parser in datasets:
		archive_path = download(archive_filename, directory=directory)
		with ZipFile(archive_path, 'r') as zip_ref:
			for filename in zip_ref.namelist():
				with zip_ref.open(filename, 'r') as fp:
					content = fp.read().decode(encoding)
					for word in parser(content):
						yield word

def get_word_pairs(words):
	char_str = ''.join(chars.utf8_stress_map.values())
	chars_re = re.compile('[' + char_str + ']')

	word_set = set([])
	for word in words:
		word_lower = word.lower()
		if word_lower in word_set:
			continue
		word_set.add(word_lower)

		destressed_word_lower = chars_re.sub('', word_lower)
		if destressed_word_lower != word_lower:
			yield word_lower, destressed_word_lower	

if __name__ == '__main__':
	for word, destressed_word in get_word_pairs(get_words()):
		print(word, destressed_word)
