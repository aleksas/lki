from zipfile import ZipFile
from io import TextIOWrapper
import re

datasets = [
	('./datasets/dlkz.zip', 'utf-8'),
	('./datasets/hist-loc-names.zip', 'utf-8'),
	('./datasets/last-names.zip', 'utf-8'),
	('./datasets/lt-lv.zip', 'utf-8')
]

def get_dataset_json_files():
	for archive_filename, encoding in datasets:
		with ZipFile(archive_filename, 'r') as zip_ref:
			for filename in zip_ref.namelist():
				with zip_ref.open(filename, 'r') as fp:
					with TextIOWrapper(fp, encoding=encoding) as text_fp:
						yield text_fp
