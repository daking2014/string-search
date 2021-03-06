import csv
from optparse import OptionParser
from string import maketrans

#options
parser = OptionParser()
parser.add_option('-a', '--inputfile',
					dest='filename', 
					help='The file to be searched (.csv)')
parser.add_option('-o', '--outputfile',
					dest='newfilename',
					help='The file to be written to (.csv)')
parser.add_option('-k', '--casesensitive',
					action='store_true', dest='casesensitive', default=False,
					help='If the search should be case sensitive')
parser.add_option('-d', '--hammingdistance',
					type='int', dest='hammingdistance', default=1,
					help='The desired hamming distance for the search')
parser.add_option('-s', '--substring',
					dest='substring',
					help='The substring that is being searched for')
parser.add_option('-c', '--complement',
					action='store_true', dest='complement', default=False,
					help='If the search should be for the search query\'s complement')
parser.add_option('-r', '--rna',
					action='store_true', dest='rna', default=False,
					help='If the string to be searched is an RNA strand, and the search is for the complement')					
(options, args) = parser.parse_args()

#setting options variables
file_path = options.filename
new_file_path = options.newfilename
case_sensitive = options.casesensitive
hd = options.hammingdistance
sub_string = options.substring
complement = options.complement
rna = options.rna

#complement function
def create_DNA_complement(string_segment):
	if rna:
		pairs = {'A':'U', 'U':'A', 'G':'C', 'C':'G'}
	else:
		complement = ''
		pairs = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
		for b in string_segment:
			b = pairs[b]
			complement += b
	print complement
	return complement

#hamming distance function
def hamming_distance(sub_string, string_segment):
	distance = 0
	if len(sub_string) == len(string_segment):
		for i in range(len(sub_string)):
			if not sub_string[i] == string_segment[i]:
				distance += 1
		return distance

#search function to return a dictionary with all instances found
def find_all_instances(file_path, sub_string, hd, case_sensitve):
	hd = int(hd)
	instances_dict = {}
		
	#takes in text to search
	strings_for_searching = {}
	with open(file_path, 'r+') as searchfile:
		text = list(searchfile)
		for line in text:
			#title of each string
			splitUp = line.strip().split(',')
			#print splitUp
			strings_for_searching[splitUp[0]] = splitUp[1]
	
	#print strings_for_searching
			
	#searches each row and adds results to the instances_dict dictionary
	#variable for attaching the right title to the right search results
	for name in strings_for_searching:
		string = strings_for_searching[name]
		if case_sensitive:
			string = string.lower()
			sub_string = sub_string.lower()
	
		for index in range(len(string)):
			string_segment = string[index:(index+len(sub_string))]
			if complement:
				string_segment = create_DNA_complement(string_segment)
			if len(string_segment) == len(sub_string):
				if hamming_distance(sub_string, string_segment) <= hd:
					if not name in instances_dict:
						instances_dict[name] = []
					instances_dict[name].append(str(index))
	#print instance_dict
	return instances_dict

#creates a usable output from the function (for writing to a new csv file)
found = find_all_instances(file_path, sub_string, hd, case_sensitive)

#write to file
with open(new_file_path, 'ab') as csvfile:
	csvfile.write('sequence,location(s)\n')
	for key in found:
		entry = str(key) + ',' + ';'.join([str(i) for i in found[key]]) + '\n'
		csvfile.write(entry)
	
#----------------------------------------tests--------------------------------------------------------------------------
"""import unittest

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
	
		
	""""""relies on searching a specific file for "GGGG". This is the text of that specific csv file:
	string1,AAAAAAAAAAAAAGGGAAAAAAAAAAAAAAAAAAGGGAAA
	string2,GGGGAAAAAAAGGGGAAAA
	string3,AAAAAAAAAAAAAAGGGGAAAAAAAAAAAAAAAAAAGGGGAAAA""""""
	
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
"""
