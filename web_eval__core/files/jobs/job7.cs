using System;
using System.IO;
public class adun
{
    public static void Main()
    {
        int a,b;
		FileStream fin = new FileStream("adunare.in", FileMode.OpenOrCreate, FileAccess.Read);
		FileStream fout = new FileStream("adunare.out",FileMode.Create,FileAccess.Write);
		StreamReader SwIn = new StreamReader(fin);
		StreamWriter SwOut = new StreamWriter(fout);
		a = int.Parse(SwIn.ReadLine());
		b = int.Parse(SwIn.ReadLine());
		SwOut.WriteLine(a+b);
		SwOut.Close();
		SwIn.Close();
	}
} 

