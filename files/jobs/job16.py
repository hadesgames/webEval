#!/usr/bin/env python
filein = open('adunare.in', 'r')
fileout = open('adunare.out', 'w')

a = int(filein.readline())
b = int(filein.readline())
fileout.writelines(str(a + b))
