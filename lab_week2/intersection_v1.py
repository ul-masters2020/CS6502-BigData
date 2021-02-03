def intersection_v1(L1, L2):
	'''This function finds the intersection between 
	L1 and L2 list using in-built methods '''
	s1 = set(L1)
	s2 = set(L2)

	result = list(s1 & s2)
	return result

if __name__ == "__main__":
	L1 = [1,3,6,78,35,55]
	L2 = [12,24,35,24,88,120,155]
	result = intersection_v1(L1, L2)
	print(f"Intersection elements: {result}")
