#!/usr/bin/env python3

from datetime import datetime
import random

ENTITY = 'data/entity'
PROPERTY = 'data/property'
LINK = 'data/link'

FIRST_ID = 0
TYPE = 'type_{}'
REGION = 'region_{}'
SIZE = 20

MIN_SIZE = 1
MAX_SIZE = 10
MIN_AGE = 9
MAX_AGE = 100


def create_entity():
	with open(ENTITY, 'w') as f:
		for id in range(FIRST_ID,SIZE - 5):
			t = datetime.now().microsecond
			f.write('{}\t{}\t{}\t{}\n'.format(id,0,t,TYPE.format(id)))

		for id in range(SIZE-5, SIZE):
			t = datetime.now().microsecond
			f.write('{}\t{}\t{}\t{}\n'.format(id,1,t,REGION.format(id)))

def create_property():
	with open(PROPERTY,'w') as f:
		for id in range(FIRST_ID,SIZE - 5):
			f.write('{}\t{}\t{}\n'.format(id,0, random.randint(MIN_SIZE, MAX_SIZE)))
			f.write('{}\t{}\t{}\n'.format(id,1, random.randint(MIN_AGE, MAX_AGE)))

		for id in range(SIZE-5, SIZE):
			f.write('{}\t{}\t{}\n'.format(id,0, random.randint(MIN_SIZE, MAX_SIZE)))
			f.write('{}\t{}\t{}\n'.format(id,1, random.randint(0, 3)))
			f.write('{}\t{}\t{}\n'.format(id,2, random.randint(0, 1)))


def create_link():
	with open(LINK, 'w') as f:
		for id in range(FIRST_ID, SIZE - 5):
			t = datetime.now().microsecond
			r = random.randint(SIZE-5,SIZE - 3)
			f.write('{}\t{}\t{}\t{}\n'.format(id, r, t, random.randint(0,5)))
			f.write('{}\t{}\t{}\t{}\n'.format(id, r + 1, t, random.randint(0,5)))
			f.write('{}\t{}\t{}\t{}\n'.format(id, r + 2, t, random.randint(0,5)))

create_entity()
create_property()
create_link()
