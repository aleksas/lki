from zipfile import ZipFile
from parsers import modern_lt_vocabulary_words, historic_location_names, last_names, lt_lv_dict
import chars
import re

datasets = [
	('./datasets/207-dlkz.zip', 'utf-8', modern_lt_vocabulary_words),
	('./datasets/1001-location-names.zip', 'utf-8', historic_location_names),
	('./datasets/1101-last-names.zip', 'utf-8', last_names),
	('./datasets/105-lt-lv-dict.zip', 'utf-8', lt_lv_dict)
]

def get_words():
	for archive_filename, encoding, parser in datasets:
		with ZipFile(archive_filename, 'r') as zip_ref:
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
