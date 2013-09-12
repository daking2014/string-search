import csv
from optparse import OptionParser

#options
parser = OptionParser()
parser.add_option('-a', '--inputfile',
					dest='filename', 
					help='The file to be searched (.csv)')
parser.add_option('-o', '--outputfile',
					dest='newfilename',
					help='The file to be written to (.csv)')
parser.add_option('-c', '--casesensitive',
					action='store_true', dest='casesensitive', default=False,
					help='If the search should be case sensitive')
parser.add_option('-d', '--hammingdistance',
					type='int', dest='hammingdistance', default=1,
					help='The desired hamming distance for the search')
parser.add_option('-s', '--substring',
					dest='substring',
					help='The substring that is being searched for')
(options, args) = parser.parse_args()

#setting options variables
file_path = options.filename
new_file_path = options.newfilename
case_sensitive = options.casesensitive
hd = options.hammingdistance
sub_string = options.substring

#hamming distance function
def hamming_distance(sub_string, string_segment):
	distance = 0
	if len(sub_string) == len(string_segment):
		for i in range(len(sub_string)):
			if not sub_string[i] == string_segment[i]:
				distance += 1
		return distance

#search function to return a dictionary with all instances found
def find_all_instances(sub_string, string, string_segment, hd, file_path, case_sensitive, row):
	instances_dict = {}
		
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

#creates a usable output from the function (for writing to a new csv file)
found = find_all_instances(sub_string, 0, 0, hd, file_path, case_sensitive, 0)

for key in found:
	with open(new_file_path, 'ab') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',')
		writer.writerow([key] + [found[key]])

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
	
def main():
	unittest.main()
	
if __name__ == '__main__':
	main()
