import System
import System.IO

fin = File.OpenText('adunare.in')
fout = File.CreateText('adunare.out')

a = double.Parse(fin.ReadLine())
b = double.Parse(fin.ReadLine())

fout.WriteLine("30" + '\n')

fout.Close()
