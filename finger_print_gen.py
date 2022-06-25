"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""

import random
import string

finger_print_var = []
finger_print_var_read = []


def randStr(chars=string.ascii_uppercase + string.digits, N=32):
	return ''.join(random.choice(chars) for _ in range(N))


def iter_rand():
	x = randStr(chars=string.ascii_lowercase + string.ascii_uppercase + string.punctuation)
	finger_print_var.append(x)


i = 0
while i < 32:
	iter_rand()
	i += 1

with open('./dev_key_sp.txt', 'w') as fo:
	for _ in finger_print_var:
		print(_)
		fo.write(_ + '\n')
fo.close()

