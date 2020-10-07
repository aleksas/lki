from archive_iterator import get_dataset_json_files
import json
import re
import chars

def get_entries():
	for fp in get_dataset_json_files():
		dataset = json.load(fp)
		for entry in dataset:
			yield entry
	
def get_entry_records(entry):
	return entry['root']['record']

def has_homonyms(record):
	for subrecord in record['el'][:-1]:
		if subrecord['@name'] == 'homonym':
			return True
	return False

def has_titleword(record):
	for subrecord in record['el']:
		if subrecord['@name'] == 'AntrastinisZodis':
			return True

def get_titleword(record):
	for subrecord in record['el']:
		if subrecord['@name'] == 'AntrastinisZodis':
			return subrecord['@value'].split(',')[0]

def has_surname(record):
	for subrecord in record['el']:
		if subrecord['@name'] == 'mainSurname':
			return True

def get_surname(record):
	for subrecord in record['el']:
		if subrecord['@name'] == 'mainSurname':
			return subrecord['@value']

def has_location_accented(record):
	for subrecord in record['el']:
		if subrecord['@name'] == 'CurrentLocation':
			return True

def get_location_accented(record):
	for subrecord in record['el']:
		if subrecord['@name'] == 'CurrentLocationAccented' and subrecord['@value'] != '-':
			value = subrecord['@value']
			m = re.search(r'^([^(\\]+?)\s*((\(|\\\\|\/\/).+)?$', value)
			if m:
				return m.group(1)

def get_homonyms(record):
	entryfulltext = record['el'][-1]
	if entryfulltext['@name'] not in ['entryfulltext', 'link']:
		raise Exception()
	if '@value' in entryfulltext:
		entryfulltext = entryfulltext['@value']
	else:
		entryfulltext = None

	homonyms = []
	for homonym in record['el'][:-1]:
		if homonym['@name'] != 'homonym' or homonym['@value'] not in ['', '1', '2', '3', '4', '5']:
			raise Exception()
		homonym = homonym['el']

		extra_forms = None
		if isinstance(homonym, list):
			extra_forms = homonym[1:]
			homonym = homonym[0]
			
			homonyms.append(homonym)

	yield homonyms, process_extra_forms(extra_forms), entryfulltext

def get_words(homonym):
	if homonym['@name'] != 'words' or homonym['@value'] != '':
		raise Exception()

	for word in homonym['el']:
		if word['@name'] in ['chap', 'idiom', 'abs', 'prl']:
			continue
		if word['@name'] != 'word':
			raise Exception()

		yield word['@value'], (word['el'] if 'el' in word else None)

def process_word_details(word_details):
	if not word_details:
		return

	if 'el' in word_details:
		raise Exception()

	if isinstance(word_details, dict) and word_details['@name'] in ['gram', 'wordtag']:
		return

	result = {}
	if isinstance(word_details, dict):
		word_details = [word_details]
	for detail in word_details:
		name = detail['@name']
		if name in ['gram', 'wordtag']:
			continue

		value = detail['@value']
		
		if name in result:
			if not isinstance(result[name], list):
				result[name] = [result[name]]
				
			result[name].append(value)
		else:
			result[name] = value
 

	return result

def process_extra_forms(extra_forms):
	if not extra_forms:
		return

	for extra_form in extra_forms:
		if 'el' not in extra_form or extra_form['@name'] != 'words' or extra_form['@value'] != '':
			raise Exception()

		if extra_form['@name'] in ['gram', 'wordtag']:
			raise Exception()

		if isinstance(extra_form['el'], dict):
			extra_form['el'] = [extra_form['el']]

		for word in extra_form['el']:
			name = word['@name']

			if name in ['chap', 'idiom']:
				continue
			
			if name != 'word':
				raise Exception()

			value = word['@value']
			
			if value.startswith('~'):
				yield 'form', value

def get_combined_words(word, processed_word_details, extra_forms):
	if processed_word_details and len(processed_word_details) > 0:
		for details in [processed_word_details.items(), extra_forms]:
			for name, value in details:
				if name == 'ending':
					if '~' in value:
						value = value[1:]

					yield word + value
				elif name == 'form':
					if not isinstance(value, list):
						value = [value]
					for form in value:
						if form.startswith('~'):
							yield word + form[1:]
						else:
							yield form
				else:
					raise Exception()			
	else:
		yield word

def iterate_all():
	for entry in get_entries():
		record = get_entry_records(entry)
		if has_homonyms(record):
			for homonyms, extra_forms, entryfulltext in get_homonyms(record):			
				for homonym in homonyms:
					for word, word_details in get_words(homonym):
						processed_word_details = process_word_details(word_details)
						for combined_word in get_combined_words(word, processed_word_details, extra_forms):
							yield combined_word
		elif has_location_accented(record):
			location_accented = get_location_accented(record)
			if location_accented:
				yield location_accented
		elif has_surname(record):
			surname = get_surname(record)
			yield surname
		elif has_titleword(record):
			titleword = get_titleword(record)
			yield titleword
		else:
			raise Exception()

if __name__ == '__main__':
	char_str = ''.join(chars.utf8_stress_map.values())
	chars_re = re.compile('[' + char_str + ']')

	word_set = set([])
	for each in iterate_all():
		if '‿' in each:
			each = each.split('‿')[0]
		word_set.add(each.lower())
	
	words = list(word_set)
	sorted(words)
	
	print(len(word_set))


	for word in word_set:
		destressed_word = chars_re.sub('', each)
		if destressed_word != word:
			print (each, destressed_word)
