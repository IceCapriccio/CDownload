import random as rd
import hashlib

for i in range(100):
	m = hashlib.md5()
	m.update(str(i + 12345).encode())
	print(m.hexdigest())
