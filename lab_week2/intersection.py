def intersection(L1, L2):
	'''This function finds the intersection between 
	L1 and L2 list without using in-built methods '''
	result = []
	for element in L1:
		if element in L2:
			result.append(element)
		else:
			continue
	return result

if __name__ == "__main__":
	L1 = [1,3,6,78,35,55]
	L2 = [12,24,35,24,88,120,155]
	result = intersection(L1, L2)
	print(f"Intersection elements: {result}")
