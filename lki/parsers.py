import re
import os
import json
from io import TextIOWrapper
from xml.etree import ElementTree as ET 

from . import chars

def modern_lt_vocabulary(content):
	alt_re = re.compile('\(([^()]+)\)')

	def expand_altirnatives(words):
		for word in words:
			m = alt_re.search(word)
			if m:
				yield alt_re.sub('', word)
				yield alt_re.sub(r'\1', word)
			else:
				yield word

	def parse_word_elements(words_el, word_cache):
		for word_el in words_el.findall('el[@name="word"]'):
			ending_el = word_el.find('el[@name="ending"]')	
			form_el = word_el.find('el[@name="form"]')

			if ending_el != None or form_el != None:
				word = word_el.get('value')
				if ending_el != None:
					yield word + ending_el.get('value').lstrip('~')
				if form_el != None:
					form = form_el.get('value')
					if form.startswith('~'):
						yield word_el.get('value') + form[1:]
					else:
						yield form
				
				if not word_cache[0]:
					word_cache[0] = word
			elif word_cache[0]:
				if word_el.get('value').startswith('~'):
					yield word_cache[0] + word_el.get('value')[1:]
				else:
					yield word_el.get('value')
			else:
				yield word_el.get('value')

	entry = ET.fromstring(content)
	for homonym in entry.iterfind('record/el[@name="homonym"]'):
		word_cache = [None]
		for words_el in homonym.findall('.//el[@name="words"]'):
			explanation_el = words_el.find('.//el[@name="valexpl"]')
			explanation = explanation_el.get('value') if explanation_el != None else None
			example_el = words_el.find('.//el[@name="valex"]')
			example = example_el.get('value') if example_el != None else None

			yield {
				'words': expand_altirnatives(parse_word_elements(words_el, word_cache)),
				'example': example,
				'explanation': explanation
			}

def modern_lt_vocabulary_words(content):
	for each in modern_lt_vocabulary(content):
		for word in each['words']:
			yield word

def historic_location_names(content):
	name_re = re.compile(r'^([^(\\]+?)\s*((\(|\\\\|\/\/).+)?$')
	entry = ET.fromstring(content)
	for location_accented_el in entry.iterfind('.//el[@name="CurrentLocationAccented"]'):
		location_accented = location_accented_el.get('value')
		if location_accented == '-':
			continue
		
		m = name_re.search(location_accented)
		if m:
			name = m.group(1)
			for each in name.split('arba'):
				yield each.strip()

def last_names(content):
	entry = ET.fromstring(content)
	for surname_el in entry.iterfind('.//el[@name="mainSurname"]'):
		yield surname_el.get('value').strip()

def lt_lv_dict(content):
	entry = ET.fromstring(content)
	for surname_el in entry.iterfind('.//el[@name="AntrastinisZodis"]'):
		yield surname_el.get('value').split(',')[0].split('‿')[0].strip()
		