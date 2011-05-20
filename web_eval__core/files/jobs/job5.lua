fin = io.open("adunare.in", "r");
fout = io.open("adunare.out", "w");
a, b = fin:read("*number", "*number");
fout:write(a + b)
fout:close()

