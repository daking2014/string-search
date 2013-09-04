import csv

#determines user entry type
entry_type =raw_input('Would you like to type a string or use a file?(string or file) ')

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

#search and write function
def find_all_instances(sub_string, string, string_segment, entry_type, hd):
	index = 0
	for i in string:
		string_segment = string[index:(index+len(sub_string))]
		if len(string_segment) == len(sub_string):
			if hamming_distance(sub_string, string_segment) <= int(hd):
				with open(new_file_path, 'ab') as csvfile:
					writer = csv.writer(csvfile, delimiter = ',')
					if entry_type == 'string':
						writer.writerow([sub_string + ' found at index ' + str(index)] + [' ' + string[(int(index) - 5): (int(index) + len(sub_string) + 5)]])
					elif entry_type == 'file':
						writer.writerow([row[0]] + [sub_string + ' found at index ' + str(index)])
		index += 1

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
	string_segment = 0
	find_all_instances(sub_string, string, string_segment, entry_type, hd)

#if a file is to be searched
elif entry_type == 'file':
	
	#file to read from
	file_path = raw_input('Enter file path of file to be searched (.csv): ')
	
	#takes user input
	sub_string = raw_input('Enter search query: ')
	
	#imports data from the file and stores in 'holder'
	holder = []
	with open(file_path, 'r+') as text:
		reader = csv.reader(text)
		for row in reader:
			holder.append(row)
	
	#case sensitive?
	for row in holder:
		if case_sensitive == 'n':
			row[1] = row[1].lower()
			sub_string = sub_string.lower()
		
		#search function
		string = row[1]
		string_segment = 0
		find_all_instances(sub_string, string, string_segment, entry_type, hd)

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

class find_all_instances_tests(unittest.TestCase):
	pass
	
def main():
	unittest.main()
	
if __name__ == '__main__':
	main()