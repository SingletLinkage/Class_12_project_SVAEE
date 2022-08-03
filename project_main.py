# Class 12 SVAEE 
# Informatics Practices Project

# Participants:
# Version:

import functools

test = functools.reduce(lambda a,b: a+b, [i**2 for i in range(1,11)])

print(f'Test value is{test}')
