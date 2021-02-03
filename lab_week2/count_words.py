def word_counter(s):
	"""Counts the occurance of each word in a given sentence s
	Note: Assuming ONLY simple sentences"""
	result = dict()
	words = (s.lower()).split(sep=' ')
	words = [w.strip() for w in words if w != ' ']
	for word in words:
		if not word[-1].isalpha():
			word = word[: len(word)-1]

		if word in result:
			result[word] += 1
		else:
 			result[word] = 1

	return result

if __name__ == "__main__":
	s = input("Enter a string: ")
	print(f"Result:\n {word_counter(s)}")