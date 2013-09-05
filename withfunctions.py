import csv

#determines user entry type
entry_type = raw_input('Would you like to type a string or use a file?(string or file) ')

#file to write to
new_file_path = raw_input('Enter path of file to be written to (.csv): ')

#ask if search will be case sensitive
case_sensitive = raw_input('Case sensitive search? (y/n) ')

#user input hamming distance
hd = raw_input('How many differences should be allowed between sub-string and match(hamming distance)? (enter an integer) ')

#hamming distance function
def hamming_distance(sub_string, string_segment):
	distance = 0
	if len(sub_string) == len(string_segment):
		for i in range(len(sub_string)):
			if not sub_string[i] == string_segment[i]:
				distance += 1
		return distance

#search function to return a dictionary with all instances found
def find_all_instances(sub_string, string, string_segment, entry_type, hd, file_path, case_sensitive, row):
	instances_dict = {}
	if entry_type == 'file':
		
		#takes in text to search
		holder = []
		with open(file_path, 'r+') as text:
			reader = csv.reader(text)
			for row in reader:
				holder.append(row)
		
		#searches each row and adds results to the instances_dict dictionary
		for row in holder:
			if case_sensitive == 'n':
				row[1] = row[1].lower()
				sub_string = sub_string.lower()
			
			string = row[1]
			string_segment = 0
		
		
			index = 0
			for i in string:
				string_segment = string[index:(index+len(sub_string))]
				if len(string_segment) == len(sub_string):
					if hamming_distance(sub_string, string_segment) <= int(hd):
						instances_dict.setdefault(row[0], []).append('index ' + str(index))
				index += 1
		return instances_dict
	
	elif entry_type == 'string':
		index = 0
		for i in string:
			string_segment = string[index:(index+len(sub_string))]
			if len(string_segment) == len(sub_string):
				if hamming_distance(sub_string, string_segment) <= int(hd):
					instances_dict.setdefault('string1', []).append('index ' + str(index))
			index += 1
		return instances_dict

#if a string is to be searched
if entry_type == 'string':
	
	#takes user input
	string = raw_input('Enter string to be searched: ')
	sub_string = raw_input('Enter search query: ')
	
	#case sensitive?
	if case_sensitive == 'n':
		sub_string = sub_string.lower()
		string = string.lower()
		
	#search function
	found_entrytypestring = find_all_instances(sub_string, string, 0, entry_type, hd, 0, case_sensitive, 0)
	
	for key in found_entrytypestring:
		with open(new_file_path, 'ab') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow([key] + [found_entrytypestring[key]])

#if a file is to be searched
elif entry_type == 'file':
	
	#file to read from
	file_path = raw_input('Enter file path of file to be searched (.csv): ')
	
	#takes user input
	sub_string = raw_input('Enter search query: ')
	
	#creates a usable output from the function (for writing to a new csv file)
	found = find_all_instances(sub_string, 0, 0, entry_type, hd, file_path, case_sensitive, 0)

	for key in found:
		with open(new_file_path, 'ab') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow([key] + [found[key]])
			
#if input is neither 'string' nor 'file'
else:
	print 'Incorrect input.'

#----------------------------------------tests--------------------------------------------------------------------------
import unittest

class hamming_distance_tests(unittest.TestCase):

	def test0(self):
		self.assertEqual(hamming_distance('acgt', 'acgt'), 0)
		
	def test1(self):
		self.assertEqual(hamming_distance('acgt','tcgt'), 1)
		
	def test2(self):
		self.assertEqual(hamming_distance('acgt','tggt'), 2)
		
	def test3(self):
		self.assertEqual(hamming_distance('acgt','tgct'), 3)
		
	def test4(self):
		self.assertEqual(hamming_distance('acgt','tgca'), 4)

class instances_dict_tests(unittest.TestCase):
	
	
	if entry_type == 'file':
		
		"""relies on searching a specific file for "GGGG". This is the text of that specific csv file:
		string1,AAAAAAAAAAAAAGGGAAAAAAAAAAAAAAAAAAGGGAAA
		string2,GGGGAAAAAAAGGGGAAAA
		string3,AAAAAAAAAAAAAAGGGGAAAAAAAAAAAAAAAAAAGGGGAAAA"""
		
		def teststring1(self):
			self.assertEqual(found['string1'], ['index 12', 'index 13', 'index 33', 'index 34'])
			
		def teststring2(self):
			self.assertEqual(found['string2'], ['index 0', 'index 1', 'index 10', 'index 11', 'index 12'])
			
		def teststring3(self):
			self.assertEqual(found['string3'], ['index 13', 'index 14', 'index 15', 'index 35', 'index 36', 'index 37'])
		
	elif entry_type == 'string':
		
		"""relies on searching a specific string for "GGGG". The string is:
		AAAAGGGGAAAAGGGGAAAA """
		
		def teststring_entrytypestring4(self):
			self.assertEqual(found_entrytypestring['string1'], ['index 3', 'index 4', 'index 5', 'index 11', 'index 12', 'index 13'])

def main():
	unittest.main()
	
if __name__ == '__main__':
	main()
