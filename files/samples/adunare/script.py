#!/usr/bin/python2

import random

for i in xrange(0, 10):
	a = random.randint(0, 10000000)
	b = random.randint(0, 10000000)

	filein = open("%d-adunare.in" % i, "w")
	fileout = open("%d-adunare.ok" % i, "w")

	print >> filein, "%d\n%d\n" % (a, b)
	print >> fileout, "%d" % (a + b)
	filein.close()
	fileout.close()
