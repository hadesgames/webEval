filein = open('99bottles.in', 'r')
fileout = open('99bottles.out', 'w')

n = int(filein.readline())

while n:
	print >> fileout, "%d bottles of vodka on the wall" % n
	print >> fileout, "%d bottles of russian vodka" % n
	print >> fileout, "Take on down, pass it around"
	print >> fileout, "%d bottles of vodka on the wall" % (n - 1)
	print >> fileout, ""
	n -= 1
