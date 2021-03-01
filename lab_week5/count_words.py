import time
import re
def word_counter(s):
	"""Counts the occurance of each word in a given sentence s
	Note: Assuming ONLY simple sentences"""
	result = dict()
	#words = (s.lower()).split(sep=' ')
	words = re.findall('[a-zA-Z_]+', s)
	words = [w.strip("_") for w in words if w != ' ']
	for word in words:
		if word in result:
			result[word] += 1
		else:
 			result[word] = 1

	return result

def main():
	start_time = time.time()
	filename = input("Enter filename: ")
	with open(filename, 'r') as f:
		line = f.read()
	d = (word_counter(line))
	with open('myfile.txt', 'w') as f:
		print(d, file=f)
	print(f"Execution time: {round(time.time() - start_time, 3)} seconds")

if __name__ == "__main__":
	'''Book Name: The Princess Casamassima
	File Size: 1.2MB'''
	main()
