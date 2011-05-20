#!/usr/bin/env python

import random

users = [
	{'initial_rating' : 2200, 'score' : 300},
	{'initial_rating' : 2610, 'score' : 300},
	{'initial_rating' : 1512, 'score' : 100},
	{'initial_rating' : 1650, 'score' : 250},
	{'initial_rating' : 1813, 'score' : 10},
	{'initial_rating' : 1590, 'score' : 30},
	{'initial_rating' : 1800, 'score' : 300},
	{'initial_rating' : 1720, 'score' : 130},
	{'initial_rating' : 1670, 'score' : 230},
	{'initial_rating' : 1567, 'score' : 100},
	{'initial_rating' : 1565, 'score' : 10},
	{'initial_rating' : 1545, 'score' : 0},
	{'initial_rating' : 700, 'score' : 0},
	{'initial_rating' : 890, 'score' : 30},
	{'initial_rating' : 1200, 'score' : 40},
	{'initial_rating' : 1200, 'score' : 300},
	{'initial_rating' : 1200, 'score' : 140},
	{'initial_rating' : 1200, 'score' : 80},
	{'initial_rating' : 1200, 'score' : 20},
	{'initial_rating' : 1200, 'score' : 30},
	{'initial_rating' : 1120, 'score' : 150},
	{'initial_rating' : 910, 'score' : 45},
	{'initial_rating' : 829, 'score' : 30},
]
	
N = len(users)
M = N * (N - 1) / 2

users.sort(key=lambda user: user['score'])

users[N - 1]['id'] = N

for u1 in xrange(N - 2, -1, -1):
	if users[u1 + 1]['score'] == users[u1]['score']:
		users[u1]['id'] = users[u1 + 1]['id']
	else:
		users[u1]['id'] = u1 + 1
		
for u1 in xrange(N):
	_u1 = users[u1]
	_u1['e'] = 0
	_u1['s'] = 0
	_u1['k'] = 256 if _u1['initial_rating'] != 1200 and random.choice([0, 1]) == 1 else 512
	
	print "Rating: %.4d, score: %.3d" % (users[u1]['initial_rating'], users[u1]['score']),
	for u2 in xrange(N):
		_u2 = users[u2]
		if u1 == u2:
			continue
		_u1['e'] += 1.00 / (1 + 10**(1.00 * (_u2['initial_rating'] - _u1['initial_rating']) / 400))
		#print _u1['e']
	
	_u1['e'] /= M
	_u1['s'] = 1.00 * (_u1['id']) / M
	print _u1['e'],
	print "K: ", _u1['k'],
	print _u1['s'],'    ',
	
	
	_u1['new_rating'] = _u1['initial_rating'] + _u1['k'] * N * (_u1['s'] - _u1['e'])
	print int(_u1['new_rating'])

	
