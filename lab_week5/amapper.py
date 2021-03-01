#!/usr/bin/python3

import sys

def read_input(file):
	for line in file:
		#Split the line into words
		yield line.split()

def main(separator='\t'):
	data = read_input(sys.stdin)
	#Input from STDIN
	for words in data:
		for word in words:
			print(f"{word} {separator} {1}")

if __name__ == '__main__':
	main()